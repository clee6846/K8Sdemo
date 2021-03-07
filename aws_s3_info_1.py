#!/usr/bin/env python3
# Date :10-21-2017
# Programmer : Charles Lee
# Description:
# aws SDK need be installed, need run aws configure to setup your AWS ID and key.
# when execute ./aws_vpc_info.py -c ec2 -f server_list -a status, Besides the putput to screen, output also will be written in a file "instances"
#
 
import boto3
from botocore.exceptions import ClientError
import pprint
import sys
from time import sleep
import argparse

SLEEPTIME=5

def upload_file():
    s3 = boto3.resource('s3')
    s3.Bucket('cluster2.dev.kopsshop.com').upload_file( 'aws_S3_info.py','hello.txt')

def download_file():
    s3 = boto3.resource('s3')
    s3.Bucket('mybucket').download_file('hello.txt', '/tmp/hello.txt')

def empty_bucket():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('cluster2.dev.certain.com')
    bucket.objects.all().delete()
    # for obj in bucket.objects.all():
    #    obj.delete()


def delete_bucket():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('clusters1.dev.certain.com')
    bucket.objects.all().delete()
    # for obj in bucket.objects.all():
    #    obj.delete()
    bucket.delete()
    list_buckets()

def create_bucket():
    s3 = boto3.client('s3')
    response = s3.create_bucket(
    ACL='private',
    Bucket='cluster3.dev.kopsshop.com',
    CreateBucketConfiguration={
        'LocationConstraint': 'us-west-1'
    },
    )

   
def list_buckets():
   s3 = boto3.client('s3')
   
   response = s3.list_buckets()
   # Get a list of all bucket names from the response
   buckets = [bucket['Name'] for bucket in response['Buckets']]
   
   for bucket in buckets:
       pp = pprint.PrettyPrinter(depth=6,indent=4)
       pp.pprint ("Bucket Name: %s,  " % (bucket))
       print()

#Parse command line
def _parse_command_line():
  parser = argparse.ArgumentParser(description='S3 services')
  parser.add_argument(
  'action', type=str.lower,
  choices=['upload', 'download', 'move','create','delete','empty','list'],
  help='upload, download, move, delete a file, create, erase, empty and list a bucket')
  return parser.parse_args()

            
def main():
  args = _parse_command_line()

  if args.action == 'upload':
    upload_file()
  if args.action == 'download':
    download_file()
  if args.action == 'move':
    move_file()
  if args.action == 'empty':
    empty_bucket()
  if args.action == 'delete':
    delete_bucket()
  if args.action == 'create':
    create_bucket()
  if args.action == 'list':
    list_buckets()

if __name__ == "__main__":
   main()
