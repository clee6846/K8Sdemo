#!/usr/bin/python

import os
import argparse
import logging
import boto3
import salt.config
import salt.loader
from json import loads
from subprocess import call
from time import sleep, time
from socket import gethostname
from math import ceil
from smtplib import SMTP
from email.mime.text import MIMEText
from yaml import load
from sys import exit as sys_exit

def _configure_logging():
  logging.basicConfig(filename = '/data02/logs/restart.log',
                      level = logging.INFO,
                      format = '{"@timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')

def _parse_command_line():
  parser = argparse.ArgumentParser(description='Safely restart services')
  parser.add_argument('action', type=str.lower, choices=['restart', 'cancel', 'clear'], help='Restart service or clear hostname from restart queue and list')
  parser.add_argument('service', type=str.lower, choices=['certain_app', 'external_services', 'internal_services'], help='Service to restart')
  parser.add_argument('-f', dest="config_file", default='/usr/local/etc/rq.yml', help='Specify config file')
  return parser.parse_args()

def _parse_config(config_file):
  with open(config_file) as f:
    config = load(f.read())
  return config

class restart_queue:
  '''Interface for the script'''

  def __init__(self, service = None, config = None):
    if config == None:
      logging.critical('No config specifed')
      sys_exit(1)
    self.hostname = gethostname()
    if 'service' in config['services'][service]:
      self.service = config['services'][service]['service'] 
    else:
      self.service = service
    self.region = self.hostname.split('.')[3]
    self.environment = self.hostname.split('.')[2]
    self.pod = self.hostname.split('.')[1]
    self.role = self.hostname.split('.')[0][:-3]
    if config['queue'] == 'file_queue':
      self.queue = file_queue(pod = self.pod, role = self.role, service = self.service)
    else:
      logging.critical('Invalid queue specified.')
      sys_exit(1)
    if config['inventory'] == 'aws_inventory':
      self.inventory = aws_inventory(aws_creds_file = '/usr/local/etc/.aws/restart_queue_creds', 
                                     region = self.region,
                                     environment = self.environment,
                                     pod = self.pod,
                                     role = self.role)
    elif config['inventory'] == 'local_inventory':
      self.inventory = local_inventory()
    else:
      logging.critical('Invalid inventory specified.')
      sys_exit(1)
    if config['alert'] == 'email_alert':
      self.alert = email_alert(recipients = config['email_alert']['recipients'])
    else:
      logging.critical('Invalid alert specified.')
      sys_exit(1)
    self.percentage = config['services'][service]['percentage']
    self.threshold = self._get_threshold()
    self.timeout = config['services'][service]['timeout']

  def restart(self):
    logging.info('Restart called for {} service.'.format(self.service))
    if not self.inventory.instance_is_registered():
      logging.info('The {} service on host {} is not registered in the service pool. We will restart with impunity!'.format(self.service, self.hostname))
      self._restart_service()
      sys_exit(0)
    if self.hostname in self.queue.get_restart_list():
      logging.info('{} service is already restarting; exiting.'.format(self.service))
      sys_exit(0)
    if self.hostname in self.queue.get_restart_queue():
      logging.info('{} service is already queued for restart; exiting.'.format(self.service))
      sys_exit(0)
    logging.info('Queuing {} service for restart.'.format(self.service))
    self.queue.append_to_queue(self.hostname)
    while self.queue.get_next_in_line() != self.hostname:
      if self.hostname not in self.queue.get_restart_queue():
        logging.warning('{} service was removed from the restart queue by another thread.'.format(self.service))
        sys_exit(1)
      sleep(10)
    while len(self.queue.get_restart_list()) >= self.threshold:
      if self.hostname not in self.queue.get_restart_queue():
        logging.warning('{} service was removed from the restart queue by another thread.'.format(self.service))
        sys_exit(1)
      sleep(10)
    logging.info('Restarting {} service.'.format(self.service))
    self.queue.move_from_queue_to_list(self.hostname)
    self.inventory.remove_instance_from_pool()
    while self.inventory.instance_is_healthy():
      sleep(5)
    self._restart_service()
    self.inventory.add_instance_to_pool()
    start_time = time()
    while not self.inventory.instance_is_healthy():
      if time() - start_time >= self.timeout:
        logging.error('Service {} startup timed out after {} seconds'.format(self.service, self.timeout))
        logging.debug('Mailing {}.'.format(config['email_alert']['recipients']))
        self.alert.send_alert(self.hostname, 'Restart timed out', 'Restart of {} on {} has timed out after {} seconds. This service will remain in the restart list until it is manually removed blocking services on other hosts from restarting.'.format(self.service, self.hostname, self.timeout))
        sys_exit(1)
      sleep(10)
    self.clear()
    logging.info('Service {} has been restarted.'.format(self.service))
    self.alert.send_alert(self.hostname, "Auto Restart", "Service {} has been restarted on {}".format(self.service, self.hostname))

  def cancel(self):
    '''Cancel the request to restart a service. Fails if service has begun to restart.'''
    logging.info('Cancel called for {} service.'.format(self.service))
    if self.hostname in self.queue.get_restart_queue():
      self.queue.remove_from_queue(self.hostname)
      logging.info('Restart of {} service cancelled.'.format(self.service))
    else:
      logging.warning('Cancel failed. {} service has already begun to restart.'.format(self.service))
      sys_exit(1)

  def clear(self):
    '''Mark a service as up. This should be called by an informed party when a service has
       finished restarting.'''
    logging.info('Clear called for {} service.'.format(self.service))
    if self.hostname in self.queue.get_restart_list():
      self.queue.remove_from_list(self.hostname)
      logging.info('{} service cleared from restart list.'.format(self.service))
    if self.hostname in self.queue.get_restart_queue():
      self.queue.remove_from_queue(self.hostname)
      logging.info('{} service cleared from restart queue.'.format(self.service))

  def _restart_service(self):
    call(['systemctl', 'restart', self.service])

  def _get_threshold(self):
    return ceil(self.percentage * self.inventory.pool_size)   

class file_queue:
  '''File queue and list backend'''

  def __init__(self, pod = None, role = None, service = None):
    self.base_dir = '/certain_software/restart'
    self.queue_dir = '{}/{}/{}/{}/queue'.format(self.base_dir, pod, role, service)
    self.restart_dir = '{}/{}/{}/{}/list'.format(self.base_dir, pod, role, service) 
    if not os.path.exists(self.queue_dir):
      os.makedirs(self.queue_dir)
    if not os.path.exists(self.restart_dir):
      os.makedirs(self.restart_dir)

  def append_to_queue(self, hostname):
    filename = "{}/{}".format(self.queue_dir, hostname)
    with open(filename, 'a'):
      os.utime(filename, None)

  def move_from_queue_to_list(self, hostname):
    src = "{}/{}".format(self.queue_dir, hostname)
    dst = "{}/{}".format(self.restart_dir, hostname)
    os.rename(src, dst)

  def remove_from_list(self, hostname):
    filename = "{}/{}".format(self.restart_dir, hostname)
    os.remove(filename)

  def remove_from_queue(self, hostname):
    filename = "{}/{}".format(self.queue_dir, hostname)
    os.remove(filename)

  def get_restart_list(self):
    return os.listdir(self.restart_dir)

  def get_restart_queue(self):
    return os.listdir(self.queue_dir)

  def get_next_in_line(self):
    a = [ {'hostname': h, 'ctime': os.stat('{}/{}'.format(self.queue_dir, h)).st_ctime} for h in os.listdir(self.queue_dir) ]
    return sorted(a, key=lambda k: k['ctime'])[0]['hostname']

    
class aws_inventory:
  '''Class to get inventory from AWS API'''

  def __init__(self, aws_creds_file = '/usr/local/etc/.aws/restart_queue_creds', region = None, environment = None, pod = None, role = None):
    self.aws_creds_file = aws_creds_file
    self.aws_access_key = self._get_aws_access_key()
    self.aws_secret_key = self._get_aws_secret_key()
    self.region = region
    self.environment = environment
    self.pod = pod
    self.role = role
    if environment == "prod" and pod == "pod1":
      self.elb =  "{}-{}-{}".format(self.role, self.pod, self.environment)
    else:
      self.elb = "elb-{}-{}-{}-{}".format(self.role, self.pod, self.environment, self.region)
    self.instance_id = self._get_instance_id()
    self.aws_region = self._get_aws_region()
    self.session = boto3.Session(aws_access_key_id = self.aws_access_key, 
                                 aws_secret_access_key = self.aws_secret_key,
                                 region_name = self.aws_region)
    self.client = self.session.client('elb')
    self.pool_size = self._get_pool_size()

  def _get_aws_access_key(self):
    with open(self.aws_creds_file) as f:
      return load(f.read())['aws_access_key']
  
  def _get_aws_secret_key(self):
    with open(self.aws_creds_file) as f:
      return load(f.read())['aws_secret_key']

  def _get_aws_region(self):
    region_map = { 'va': 'us-east-1', 
                   'oh': 'us-east-2',
                   'or': 'us-west-2',
                   'ca': 'us-west-1' }
    return region_map[self.region]

  def _get_pool_size(self):
    response = self.client.describe_load_balancers(LoadBalancerNames=[self.elb])
    size = len(response["LoadBalancerDescriptions"][0]["Instances"])
    logging.debug("Pool size: {}".format(size))
    return size

  def _get_instance_id(self):   
    salt_opts = salt.config.minion_config('/etc/salt/minion')
    salt_grains = salt.loader.grains(salt_opts)
    return salt_grains['ec2']['instance_id']

  def remove_instance_from_pool(self):
    response = self.client.deregister_instances_from_load_balancer(LoadBalancerName=self.elb, Instances=[{'InstanceId': self.instance_id}])
    registered_instances =  [ instance["InstanceId"] for instance in response["Instances"] ] 
    if self.instance_id in registered_instances:
      return False
    return True

  def add_instance_to_pool(self):
    response = self.client.register_instances_with_load_balancer(LoadBalancerName=self.elb, Instances=[{'InstanceId': self.instance_id}])
    registered_instances =  [ instance["InstanceId"] for instance in response["Instances"] ] 
    if self.instance_id in registered_instances:
      return True
    return False

  def instance_is_healthy(self):
    response = self.client.describe_instance_health(LoadBalancerName=self.elb, Instances=[{'InstanceId': self.instance_id}])
    if response['InstanceStates'][0]['State'] == "InService":
      return True
    return False

  def instance_is_registered(self):
    response = self.client.describe_load_balancers(LoadBalancerNames=[self.elb])
    registered_instances =  [ instance["InstanceId"] for instance in response["LoadBalancerDescriptions"][0]["Instances"] ] 
    if self.instance_id not in registered_instances:
      return False
    return True

class local_inventory:
  '''Dummy inventory class for local testing'''

  def __init__(self):
    self.pool_size = 2

class email_alert:
  '''Class for email alerting'''

  def __init__(self, recipients = None):
    self.recipients = recipients
    self.smtp_conn = SMTP('localhost')
    
  def send_alert(self, hostname, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'restart_alert@{}'.format(hostname)
    msg['To'] = ', '.join(self.recipients)
    try:
      self.smtp_conn.sendmail('restart_alert@{}'.format(hostname), self.recipients, msg.as_string())
    except Exception as e:
      logging.error(e)
  
def main():
  _configure_logging()
  args = _parse_command_line()
  config = _parse_config(args.config_file)
  
  my_service = restart_queue(service = args.service, config = config)
  if args.action == 'restart':
    my_service.restart()
  if args.action == 'cancel':
    my_service.cancel()
  if args.action == 'clear':
    my_service.clear()

if __name__ == '__main__':
  main()
