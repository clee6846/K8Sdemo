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
import json
import pprint
import zipfile
from zipfile import ZipFile
import operator

def get_all_file_paths(directory):
 
    # initializing empty file paths list
    file_paths = []
 
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
 
    # returning all file paths
    return file_paths       


def upload_file(region, archivename, vaultname):
    inventory = open ('glacier_inventory','a')
    glacier = boto3.client('glacier',region_name=region)
    if os.path.isfile(archivename) and zipfile.is_zipfile(archivename):
       response = glacier.upload_archive(
                 accountId='-',
                 body=archivename,
                 vaultName=vaultname
                 )
    if os.path.isfile(archivename) and zipfile.is_zipfile(archivename) == False:
       zf = archivename + '.zip'
       print (zf)
       with ZipFile(zf,'w') as zip:
        # writing each file one by one
          zip.write(archivename)
       response = glacier.upload_archive(
                 accountId='-',
                 body=zf,
                 vaultName=vaultname
                 )

    if os.path.isdir(archivename):
       file_paths = get_all_file_paths(archivename)
       if str(archivename.split('/')[-1]) != '':
         zf = archivename + '/' + str(archivename.split('/')[-1]) + '.zip'
       else:
         print ("directory can not end with / error")
       with ZipFile(zf,'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file) 
       response = glacier.upload_archive(
                  accountId='-',
                  body=zf,
                  vaultName=vaultname
                 )
    sorted_response = sorted(response.items(), key=operator.itemgetter(0))
    print (sorted_response)
    inventory.write(str(sorted_response))
    inventory.write("\n")
      
 

def download_file(region, filename, vaultname):
    glacier = boto3.client('glacier',region_name=region)

def delete_vault(region,vaultname):
    confirm = input('Are you sure, you want to delete a vault? if you are sure, please input the vaultname again :')
    if confirm == vaultname:
       glacier = boto3.client('glacier',region_name=region)
       response = glacier.delete_vault(
                  vaultName = vaultname,
                  accountId='-'
                  )
    else:
       print ("Bye")
    print ("Vault %s is deleted  %s" % (vaultname, response))
    list_vaults(region)

def create_vault(region,vaultname):
    confirm = input('Are you sure, you want to create a vault? if you are sure, please input the vaultname again :')
    if confirm == vaultname:
       glacier = boto3.client('glacier',region_name=region)
       response = glacier.create_vault(
                  vaultName = vaultname,
                  accountId='-'
                  )
    else:
       print ("Bye") 
    print ("Vault %s is created %s" % (vaultname, response))  

def list_vaults(region):
    glacier = boto3.client('glacier',region_name=region)
    response = glacier.list_vaults()
    pprint.pprint (response)
    exit(0)

#Parse command line
def _parse_command_line():
  parser = argparse.ArgumentParser(description='S3 services', usage='%(prog)s --region --format')
  parser.add_argument("--region", help="The region of the Classic Load Baddlancers "
                                         "that you want to describe",required=True)
  parser.add_argument("--action",  help="upload, download, move, a file, create, delete, and list a vault",required=True)
  return parser.parse_args()

            
def main():
    args = _parse_command_line()
    if args.action == 'upload' or args.action == 'download' or args.action == 'copy' or args.action == 'empty' or args.action == 'delete' or args.action == 'create':
       vaultname = input ('Please input the vault name : ')
    if args.action == 'upload':
       filename = input('Please input the upload file : ')
       upload_file(args.region, filename, vaultname)
    if args.action == 'download':
       filename = input('input the download file : ')
       download_file(args.region,filename,vaultname)
    if args.action == 'delete':
       delete_vault(args.region,vaultname)
    if args.action == 'create':
       create_vault(args.region,vaultname)
    if args.action == 'list':
       list_vaults(args.region)

if __name__ == "__main__":
   main()
