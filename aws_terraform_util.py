#!/usr/bin/python
# Programmer : Charles Lee

import argparse
import logging
import time
import os
import sys
import subprocess
import pydoc
import pdb

def main():
  # Initialize
  build_args = parse_args()
  base_dir = terraform_build_base_dir()

  # Do work
  if build_args.action in ['plan', 'create']:
    build_dir = base_dir.create_build_dir(build_args.account, build_args.vpc, build_args.region, build_args.environment, build_args.pod, build_args.role)
    build = terraform_build(build_dir, vars(build_args))
    try:
      build.define_build()
    except:
      print sys.exc_info()
      #base_dir.delete_build_dir(build_dir)
    if build_args.action == 'create':
      try:
        build.create_build()
      except:
        build_dir.delete_build_dir(build_dir)
    else:
      print build_dir
  elif build_args.action in ['show']:
    base_dir.list_build_dirs()
  elif build_args.action in ['modify', 'destroy']: 
    base_dir.list_build_dirs()
    build_number  = _get_build_number()
    build_dir = base_dir.get_build_dir(build_number)
    print build_dir
    return
  else:
    return
    
def _get_build_number():
  while True:
    try:
      answer = int(raw_input("Choose build: "))
    except ValueError:
      print "Input must be a number"
      continue
    else:
      break
  return answer

def parse_args():
  parser = argparse.ArgumentParser(description='Create, Destroy, and Manage cloud resources through Terraform', formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=32))
  parser.add_argument('action', type=str.lower, choices=['plan','create','modify','destroy'], help='Terraform action')
  parser.add_argument('-a', '--account', type=str.lower, dest='account', choices=['dev', 'helpdesk', 'prod'], required=True, help='Define account in which to create resources.')
  parser.add_argument('-R', '--region', type=str.lower, dest='region', choices=['oregon', 'virginia', 'ohio'], required=True, help='Define region in which to create resources.')
  parser.add_argument('-V', '--vpc', type=str.lower, dest='vpc', choices=['poc', 'default', 'beta', 'website', 'prod', 'dev'], required=True, help='Define the VPC in which to create resources.')
  parser.add_argument('-E', '--environment', type=str.lower, dest='environment', choices=['dev', 'qa', 'beta', 'prod', 'poc', 'test', 'stag'], required=True, help='Define environment in which to create resources.')
  parser.add_argument('-p', '--pod', type=str.lower, dest='pod', choices=['pod0', 'pod1', 'pod2', 'pod3', 'pod4', 'pod5', 'pod6', 'pod7', 'gen', 'xp', 'testpod'], required=True, help='Define pod in which to create resources.')
  parser.add_argument('-r', '--role', type=str.lower, dest='role', choices=['web', 'app', 'api', 'int', 'ext', 'plat', 'bulkapi', 'ssomgr', 'ssodb', 'sso', 'cie', 'mgmt', 'evstr', 'nova', 'test', 'jprox', 'jahia', 'ame', 'webhelp', 'status'], required=True, help='Define type of instance to create.')
  parser.add_argument('-c', '--count', type=int, dest='count', help='Define number of instances to create.')
  parser.add_argument('-i', '--index', type=int, dest='start_index', help='Define start of instance numbering.')
  parser.add_argument('-e', '--create-elb', dest='elb', action='store_true', help='Create an ELB.') 
  parser.add_argument('-D', '--create-elb-dme-cname', type=str, dest='cname', help='Create a cname in DNSMadeEasy and point it to your elb. (Define the domain in cname.vars.tf).') 
  parser.add_argument('-s', '--create-s3-bucket', type=str, dest='bucket_name', help='Create an S3 bucket with the defined name (Define the base name in s3.vars.tf)')
  parser.add_argument('-t', '--type', type=str.lower, dest='type', help='Define type/size of the instance. Refer to the AWS documentation for available types/sizes.')
  parser.add_argument('-C', '--config-directory', type=str, dest='config_dir', help='Define terraform configuration directory.')
  parser.set_defaults(elb=False)

  build_args = parser.parse_args()
  build_args.config_dir = build_args.config_dir if build_args.config_dir else os.environ['HOME'] + '/Documents/gitRepos/certain/terraform'

  return build_args

class terraform_build_base_dir:
  '''This class manages the base build directory for terraform builds created with the terraform build class'''
  def __init__(self, build_base_dir = os.environ['HOME'] + '/Documents/terraform_builds'):
    self.build_base_dir = build_base_dir

  def create_build_dir(self, account, vpc, region, environment, pod, role):
    #build_dir = '{}/{}_{}_{}_{}_{}'.format(self.build_base_dir, region, environment, pod, role, self._get_date())
    build_dir = '{}/{}_{}_{}_{}_{}_{}_{}'.format(self.build_base_dir, account, vpc, region, environment, pod, role, self._get_date())
    subprocess.call(['mkdir', build_dir])
    return build_dir

  def delete_build_dir(self, build_dir):
    subprocess.call(['rm', '-rf', build_dir])

  def list_build_dirs(self):
    '''List all builds'''
    build_dirs = []
    output = ""
    for build_dir in os.listdir(self.build_base_dir): 
      build_dirs += [self._get_build_dir_info(build_dir)]
    template = '''
{number}. Role: {role}
   Created on: {date} at {time}
   Account: {account}
   VPC: {vpc}
   Region: {region}
   Environment: {environment}
   Pod: {pod}
   Message: {message}'''
    for num, build in enumerate(build_dirs):
      #date = convert_to_written()
      time_colon = build['time'].replace('-', ':')
      output += template.format(number = num + 1, 
                                role        = build['role'],
                                date        = build['date'],
                                time        = time_colon,
                                account     = build['account'],
                                vpc         = build['vpc'],
                                region      = build['region'],
                                environment = build['environment'],
                                pod         = build['pod'],
                                message     = build['message'])
    pydoc.pager(output)
    
  def get_build_dir(self, num):
    '''Take a number and return the full path of the build'''
    build_dirs = [ d for d in os.listdir(self.build_base_dir) ]
    full_path = '{}/{}'.format(self.build_base_dir, build_dirs[num])
    return full_path
  
  def _get_build_dir_info(self, build_dir):
    keys = [ 'account', 'vpc', 'region', 'environment', 'pod', 'role', 'date', 'time', 'message' ]
    if os.path.isfile('{}/{}/{}'.format(self.build_base_dir, build_dir, 'message')):
      with open('{}/{}/{}'.format(self.build_base_dir, build_dir, 'message')) as f:
       message = f.read()
      values = build_dir.split('_') + [message.rstrip()]
    else:
      values = build_dir.split('_') + ['']
    return dict(zip(keys,values))

  def _get_date(self):
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

class terraform_build:
  '''This class wraps terraform. It defines, plans, applies, modifies, and destroys builds.'''
  def __init__( self, build_dir, build_args, 
                config_files = ['instance.tf', 'common.vars.tf'],
                build_base_dir = os.environ['HOME'] + '/Documents/terraform_builds', 
                terraform = 'terraform',
                dot = '/usr/local/bin/dot'
              ):
    self.dot = dot
    self.terraform = terraform
    self.build_args = build_args
    self.config_files = config_files
    self.build_base_dir = build_base_dir
    self.build_dir = build_dir

  def define_build(self):
    '''Create build directory and populate it with the associated Terraform files'''
    self.config_files.append('{}/{}.vars.tf'.format(self.build_args['account'], 'account'))
    self.config_files.append('{}/{}/{}.vars.tf'.format(self.build_args['account'], self.build_args['region'], self.build_args['vpc']))
    self.config_files.append('{}.vars.tf'.format(self.build_args['role']))
    if self.build_args['elb']:
      if self.build_args['role'] in ['app', 'api', 'jahia']:
        self.config_files.append('elb_2.tf')
      else: 
        self.config_files.append('elb.tf')
      self.config_files.append('elb.vars.tf')
    if self.build_args['cname']:
      self.config_files.append('cname.tf')
      self.config_files.append('cname.vars.tf')
    if self.build_args['bucket_name']:
      self.config_files.append('s3.tf')
      self.config_files.append('s3.vars.tf')
    self.config_files = [ '{0}/{1}'.format(self.build_args['config_dir'], config) for config in self.config_files ]
    try:
      subprocess.call(['mkdir', '-p', self.build_dir])
      subprocess.call(['cp'] + self.config_files + [self.build_dir])
    except OSError:
      raise
    try:
      self._create_override_file()
      self._create_map_file()
    except:
      raise
  
  def _create_override_file(self):
    '''Create a Terraform override file to override default variables'''
    override_template = '''variable "{0}" {{
  description = "Overwrite the {0} variable "
  default = "{1}"
}}

'''
    self.build_args = self.build_args
    with open('{0}/{1}'.format(self.build_dir, 'override.tf'), 'w') as override_file:
      for variable in self.build_args.keys():
        #if variable != 'action' and self.build_args[variable] != None:
        if variable not in ['action', 'account', 'vpc'] and self.build_args[variable] != None:
          override_file.write(override_template.format(variable, self.build_args[variable]))

  def _create_map_file(self):
    '''Create a map file using terraform map'''
    with open("{0}/{1}".format(self.build_dir, 'graph.dot'), 'w') as graph_dot:
      try:
        subprocess.call([self.terraform, 'graph'], stdout = graph_dot,  cwd = self.build_dir)
      except:
        raise
    with open("{0}/{1}".format(self.build_dir, 'graph.png'), 'w') as graph_png: 
      # Maybe it's best to do this with python, so I don't require the dot program
      subprocess.call([self.dot, '-Tpng', 'graph.dot'], stdout = graph_png, cwd = self.build_dir)

  def _clean_build(self):
    '''Remove build files if something fails'''
    subprocess.call(['rm', '-rf', self.build_dir])

  def run_build(self):
    '''Execute the Terraform command'''
    if self.build_args.action == 'create':
      if subprocess.call([self.terraform, 'apply'], cwd = self.build_dir):
        self._clean_build()
    elif self.build_args.action == 'modify':
      subprocess.call(subprocess.call([self.terraform, 'apply', self.command_variables], cwd = self.build_dir))
    elif self.build_args.action == 'destroy':
      subprocess.call(subprocess.call([self.terraform, 'destroy', self.command_variables], cwd = self.build_dir))
    else: 
      True

  def create_build(self):
    # Can I use a Try statement here? What exception would subprocess.call throw
    #   It should throw OSError
    #if subprocess.call([self.terraform, 'apply'], cwd = self.build_dir): 
    #  self._clean_build()
    #  return 1
    try:
      subprocess.call([self.terraform, 'apply'], cwd = self.build_dir) 
    except OSError:
      self._clean_build()
      raise

  def plan_build(self):
    '''Define the build and return file objects (?) which contain the plan, map, and override file'''
    # I don't think it's a good idea to pass open file objects
    self._define_build()

  def modify_build(self): 
    True

  def destroy_build(self):
    True
  
if __name__ == "__main__":
  main()
