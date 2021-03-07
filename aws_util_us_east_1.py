#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
import sys
import getopt
import json

verbose = False

def describe_instances(c,instance_id):

   ec2 = boto3.client(c)
   instance_id =  instance_id.split()
   response = ec2.describe_instances()
   response = response.json()
   print(response)

def start_stop_instances(c,instance_id,action):
   
   instance_id = instance_id.split()
   print (instance_id)

   ec2 = boto3.client(c)
   if action == 'start':
    # Do a dryrun first to verify permissions
      try:
        ec2.start_instances(InstanceIds=instance_id, DryRun=True)
      except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
      try:
        response = ec2.start_instances(InstanceIds=instance_id, DryRun=False)
        print(response)
      except ClientError as e:
        print(e)
   else:
    # Do a dryrun first to verify permissions
      try:
        ec2.stop_instances(InstanceIds=instance_id, DryRun=True)
      except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances witout dryrun
      try:
        response = ec2.stop_instances(InstanceIds=instance_id, DryRun=False)
        print(response)
      except ClientError as e:
        print(e)

def reboot_instances(c,instance_id,action):

   ec2 = boto3.client(c)
   print(instance_id)
   try:
      ec2.reboot_instances(InstanceIds=[instance_id], DryRun=True)
   except ClientError as e:
      if 'DryRunOperation' not in str(e):
        print("You don't have permission to reboot instances.")
        raise

   try:
       response = ec2.reboot_instances(InstanceIds=[instance_id], DryRun=False)
       print('Success', response)
   except ClientError as e:
       print('Error', e)

def terminate_instances(c,instance_id,action):
   pass

def execute_command(c,i,a):
   if (a == 'start' or a == 'stop'):
       start_stop_instances(c,i,a)
   elif (a == 'reboot'):
       reboot_instances(c,i,a)
   elif (a == 'terminate'):
       terminate_instances(c,i,a)
   else:
       describe_instances(c,i)

   

def main():

   help = 'aws_util_us_east_1.py -c command(ec2,s3,elb) -i instance_id -a action(stop,start,reboot,terminate)'
   help1 = 'eg aws_us_east_1.py -c ec2 -i "i-0e5f53a8d81780efe" -a "stop"'
   try:
      opts, args = getopt.getopt(sys.argv[1:],"hc:i:a:v",["help", "command","instance_id","action"])
   except getopt.GetoptError as err:
      print (str(err))
      print (help)
      print (help1)
      sys.exit(2)
   for opt in opts:
      if opt[0] == "-v":
         verbose = True
      elif opt[0] in ('-h', '--help'):
         print (help)
         print (help1) 
         sys.exit()
      elif opt[0] in ('-c', '--command'): 
         command = opt[1]
      elif opt[0] in ('-i',  '--instance_id'):
         instance_ids = opt[1]
      elif opt[0] in ('-a', '--action'):
         action = opt[1]
      else: 
         sys.exit(2)

   execute_command(command,instance_ids,action)

if __name__ == "__main__":
   main()
