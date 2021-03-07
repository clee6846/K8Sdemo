#!/usr/bin/env python3
# Programmer : Charles Lee
# Description:
# aws SDK need be installed, need run aws configure to setup your AWS ID and key.
#
 
import boto3
import botocore
from botocore.exceptions import ClientError
import pprint
import sys
from time import sleep
import argparse

SLEEPTIME=5

def isBucketexist(bucketname):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketname)
    exists = True
    try:
       s3.meta.client.head_bucket(Bucket=bucketname)
    except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
       error_code = int(e.response['Error']['Code'])
       if error_code == 404:
            exists = False
    return exists

def upload_file(bucketname, foldername, filename):
    if isBucketexist(bucketname):
       s3 = boto3.resource('s3')
       s3.Bucket(bucketnme).upload_file( 'filename','foldername/filename')
    else:
       print ("The bucket doesn't exists")

def download_file(bucketname, foldername, filename):
    if isBucketexist(bucketname):
       s3 = boto3.resource('s3')
       s3.Bucket(bucketnme).download_file( 'foldername/filename','filename')
    else:
       print ("The bucket doesn't exists")

def copy_file(bucketname,source,target):
    if isBucketexist(bucketname):
       s3 = boto3.resource('s3')
       copy_source = {
            'Bucket': bucketname,
            'Key': source
       }
       bucket = s3.Bucket(bucketnme)
       bucket.copy(copy_source, target)
    else:
       print ("The bucket doesn't exists")

def empty_bucket(bucketname):
    if isBucketexist(bucketname):
       s3 = boto3.resource('s3')
       bucket = s3.Bucket(bucketname)
       bucket.objects.all().delete()
    else:
       print ("The bucket doesn't exists")


def delete_bucket(bucketname):
    if isBucketexist(bucketname):
       s3 = boto3.resource('s3')
       bucket.objects.all().delete()
       bucket.delete()
    else:
       print ("The bucket doesn't exists")
    list_buckets()

def create_bucket(bucketname):
    if isBucketexist(bucketname):
       s3 = boto3.client('s3')
       s3.create_bucket(
          ACL='private',
          Bucket= bucketname,
          CreateBucketConfiguration={
                 'LocationConstraint': 'us-west-1'
          },
       )
    else:
       print ("Bucket already created")
   
def list_buckets():
   s3 = boto3.resource('s3')
   for bucket in s3.buckets.all():
       if isBucketexist(bucket.name):
          print ('bucket name : ', bucket.name)
          for obj in bucket.objects.all():
              print('{0}'.format( obj.key))

#Parse command line
def _parse_command_line():
  parser = argparse.ArgumentParser(description='S3 services')
  parser.add_argument(
  'action', type=str.lower,
  choices=['upload', 'download', 'copy','create','delete','empty','list'],
  help='upload, download, move, delete a file, create, erase, empty and list a bucket')
  return parser.parse_args()

            
def main():
    args = _parse_command_line()
    if args.action == 'empty' or args.action == 'delete' or args.action == 'create':
       bucketname = input ('Please input the bucket name : '
    if args.action == 'upload':
       filename = input('Please input the upload file : ')
       foldername = input('input the upload foldernme : ')
       upload_file(bucketname, filename, foldername)
    if args.action == 'download':
       filename = input('input the download file : ')
       foldername = input('input the foldername' : ')
       download_file(bucketname,foldername)
    if args.action == 'copy':
       source = input ('input the source file : ')
       target = input ('input the target file " ')
       copy_file(bucketname,source,target)
    if args.action == 'empty':
       empty_bucket(bucketname)
    if args.action == 'delete':
       delete_bucket(bucketname)
    if args.action == 'create':
       create_bucket(bucketname)
    if args.action == 'list':
       list_buckets()

if __name__ == "__main__":
   main()
