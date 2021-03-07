#!/usr/bin/env python3

# Programmer : Charles Lee
# Description:
# aws SDK need be installed, need run aws configure to setup your AWS ID and key.
# This script can 1.read a file "server_list" of  EC2 instance names then for each name get its Private IP address and instance ID, VPC ID, subnet ID, security group name and ID, its state, and public IP
# ( All the IDs are useful when open support ticket with AWS)
#                 2.And can stop or start or reboot each EC2 instance in the file "server_list"
# 
# And the future version of this script, we can get which ELB, SG the EC2 instances belong to
# Instaed of using command "EC2", users can get the status of any AWS services.
# usage:
#       assuming the deafault VPC has 10 EC2 instances which are in a files, each instances was created by Terraform in aws_us_east_2. We have the hostnames in a file called "server_list" that we are going to use them to do test 'stop' 'start' 
#       aws_util_us_east_2 -h
#       aws_util_us_east_2.py -c command(ec2,s3,elb) -f name_tag_in_a_file  -a action(status,stop,start,reboot)
#        eg aws_us_east_2.py -c ec2 -f server_list   -a stop
#   The contents of file 'server_list'
# when execute ./aws_util_us_east_2.py -c ec2 -f server_list -a status, Besides the putput to screen, output also will be written in a file "instances"
#
 
import boto3
from botocore.exceptions import ClientError
import sys
import getopt
from time import sleep

instances = []
servers = []
file_name =  ""
WRITE_EC2_INSTANCES_STATUS = "EC2_Instances_Status"
SLEEPTIME=5

def describe_instances(c):

   ec2 = boto3.client(c)
   response = ec2.describe_instances()
   return response


def Start_Stop_instances(c,action):

   ec2 = boto3.client(c)
   if action == 'start':
    # Do a dryrun first to verify permissions
      try:
        ec2.start_instances(InstanceIds=instances, DryRun=True)
      except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
      try:
        response = ec2.start_instances(InstanceIds=instances, DryRun=False)
        sleep(SLEEPTIME)
      except ClientError as e:
        print(e)
   else:
    # Do a dryrun first to verify permissions
      try:
        ec2.stop_instances(InstanceIds=instances, DryRun=True)
      except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances witout dryrun
      try:
        response = ec2.stop_instances(InstanceIds=instances, DryRun=False)
        sleep(SLEEPTIME)
      except ClientError as e:
        print(e)
   
   Print_Status(c)

def Reboot_instances(c):

   ec2 = boto3.client(c)
   try:
      ec2.reboot_instances(InstanceIds=instances, DryRun=True)
   except ClientError as e:
      if 'DryRunOperation' not in str(e):
        print("You don't have permission to reboot instances.")
        raise

   try:
       response = ec2.reboot_instances(InstanceIds=instances, DryRun=False)
       print_IP_address(c)
   except ClientError as e:
       print('Error', e)

   Print_Status(c)

def execute_command(c,a):
   response = describe_instances(c)
   print (" Please wait .....................................................................................................................................")
   for r in response['Reservations']:
       for i in r['Instances']:
          tags = i['Tags'][0]
          hostname = tags['Value']
          State = i['State']['Name']
          InstanceID = i['InstanceId']
#Only execute command when the EC2 instnace is either in running or stopped state, otherwise the command won't do anything"
          if hostname in servers:
             if State  == 'running' or State == 'stopped':
                 instances.append(InstanceID)
             else:
                 print ("Only execute command when the EC2 instnace is either in running or stopped state, otherwise the command won't do anything")
   if instances == []:
     sys.exit(2)
   else:
     if a == 'stop' or a == 'start':
       Start_Stop_instances(c,a)
     elif  a == 'reboot':
       Reboot_instances(c)
     else:
       print ("Illegal command")
       sys.exit(2)

      

   
def Print_Status(c):

   ec2 = boto3.resource(c)
   response = describe_instances(c)

   print ('{0:8s} {1:22s} {2:16s} {3:14s} {4:10s} {5:16s} {6:55s} {7:25s} {8:16s}'.format('hostname','InstanceID','PrivateIP','VpcID','SubnetID','InstanceType','SecurityGroupName','State','PublicIP'))
   for r in response['Reservations']:
       for i in r['Instances']:
          tags = i['Tags'][0]
          hostname = tags['Value']
          instances.append(hostname)
          instances.append(" ") 
          InstanceID = i['InstanceId']
          instances.append(InstanceID)
          instances.append(" ") 
          PrivateIP = i['PrivateIpAddress']
          instances.append(PrivateIP)
          instances.append(" ")
          VpcID = i['VpcId']           
          instances.append(VpcID)
          instances.append(" ")
          SubnetID = i['SubnetId']
          instances.append(SubnetID)
          instances.append(" ")
          InstanceType = i['InstanceType']
          instances.append(InstanceType)
          instances.append(" ")
          SecurityGroupName = i['SecurityGroups'][0]
          instances.append(SecurityGroupName)
          instances.append(" ")
          State = i['State']
          instances.append(State)
          instances.append(" ")
          if 'PublicIpAddress' in i:
              PublicIP = i['PublicIpAddress']
              instances.append(PublicIP)
              instances.append(" ")
          else:
              PublicIP = ""
              instances.append(PublicIP)
          instances.append('\n')

          print (hostname.rjust(8),InstanceID,PrivateIP.rjust(14),VpcID.rjust(12),SubnetID,InstanceType,SecurityGroupName,State, PublicIP.rjust(16))
          print ()

   file= open (WRITE_EC2_INSTANCES_STATUS, 'w')
   for item in instances:
      file.write (str(item))
   file.close()
            
def main():

   help = 'aws_util_us_east_2.py -c command(ec2,s3,elb) -f name_tag_in_a_file  -a action(status,stop,start,reboot)'
   help1 = 'eg aws_us_east_2.py -c ec2 -f server_list -a stop'
   try:
      opts, args = getopt.getopt(sys.argv[1:],"hc:f:a:",["help","command","file_name","action"])
   except getopt.GetoptError as err:
      print (str(err))
      print (help)
      print (help1)
      sys.exit(2)
   for opt in opts:
      if opt[0] in ('-h', '--help'):
         print (help)
         print (help1) 
         sys.exit()
      elif opt[0] in ('-c', '--command'): 
         command = str(opt[1])
      elif opt[0] in ('-f', '--file_name'):
         file_name = str(opt[1])
      elif opt[0] in ('-a', '--action'):
         action = str(opt[1])
      else: 
         sys.exit(2)
   f = open(file_name,'r') 
   for line in f:
      servers.append(line.rstrip('\n'))

   f.close()
   if action == "status":
      Print_Status(command)
   elif action == "stop" or action == "start" or action == "reboot":
      print ()
      execute_command(command,action)
   else:
      sys.exit()

if __name__ == "__main__":
   main()
