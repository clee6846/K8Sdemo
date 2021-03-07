#!/usr/bin/env python3
# Programmer : Charles Lee
# Description:
# aws SDK need be installed, need run aws configure to setup your AWS ID and key.
#
 
import boto3
import botocore
from botocore.exceptions import ClientError
import pprint
import os
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

def isFileexist(bucketname,filename):

    s3 = boto3.resource('s3')
    exists = True
    try:
       s3.Object(bucketname, filename).load()
    except botocore.exceptions.ClientError as e:
       if e.response['Error']['Code'] == "404":
          exists = False
    return exists

def upload_file(bucketname, local_directory, destination):

    if isBucketexist(bucketname) == False:
       print ("%s doesn't exist" % bucketname)
    else:
       client = boto3.client('s3')
       # enumerate local files recursively
       for root, dirs, files in os.walk(local_directory):

          for filename in files:

          # construct the full local path
              local_path = os.path.join(root, filename)

          # construct the full Dropbox path
              relative_path = os.path.relpath(local_path, local_directory)
              s3_path = os.path.join(destination, relative_path)

          # relative_path = os.path.relpath(os.path.join(root, filename))

              print ("Searching {} in {}".format(s3_path, bucketname))
              try:
                  client.head_object(Bucket=bucketname, Key=s3_path)
                  print ("Path found on S3! Skipping %s..." % s3_path)

                  # try:
                  # client.delete_object(Bucket=bucket, Key=s3_path)
                  # except:
                  # print "Unable to delete %s..." % s3_path
              except:
                  print ("Uploading %s..." % s3_path)
                  client.upload_file(local_path, bucketname, s3_path)

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
       confirm = input('Are you sure, you want to empty a bucket? if you are sure, please input the bucketname again :')
       if confirm == bucketname:
          s3 = boto3.resource('s3')
          bucket = s3.Bucket(bucketname)
          bucket.objects.all().delete()
       else:
          print ("Bye")
    else:
       print ("The bucket doesn't exists")


def delete_bucket(bucketname):
    if isBucketexist(bucketname):
       confirm = input('Are you sure, you want to delete a bucket? if you are sure, please input the bucketname again :')
       if confirm == bucketname:
          s3 = boto3.resource('s3')
          bucket = s3.Bucket(bucketname)
          bucket.objects.all().delete()
          bucket.delete()
       else:
          print ("Bye")
    else:
       print ("The bucket doesn't exists")
    list_buckets()

def create_bucket(bucketname):
    if isBucketexist(bucketname) == False:
       confirm = input('Are you sure, you want to create a bucket? if you are sure, please input the bucketname again :')
       if confirm == bucketname:
          s3 = boto3.client('s3')
          s3.create_bucket(
                   ACL='private',
                   Bucket= bucketname,
                   CreateBucketConfiguration={
                   'LocationConstraint': 'us-west-1'
                   },
           )
       else:
          print ("Bye") 
    else:
       print ("Bucket already created")
   
def list_buckets():
   s3 = boto3.resource('s3')
   for bucket in s3.buckets.all():
       if isBucketexist(bucket.name):
          print ('bucket name : ', bucket.name)
         # for obj in bucket.objects.all():
          #    print('{0}'.format( obj.key))

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
    if args.action == 'upload' or args.action == 'download' or args.action == 'copy' or args.action == 'empty' or args.action == 'delete' or args.action == 'create':
       bucketname = input ('Please input the bucket name : ')
    if args.action == 'upload':
       filename = input('Please input the upload file : ')
       foldername = input('input the upload foldernme : ')
       upload_file(bucketname, filename, foldername)
    if args.action == 'download':
       filename = input('input the download file : ')
       foldername = input('input the foldername : ')
       download_file(bucketname,filename,foldername)
    if args.action == 'copy':
       source = input('input the source file : ')
       target = input('input the target file : ')
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
