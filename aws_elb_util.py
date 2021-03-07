#!/usr/bin/env python3
# Programmer : Charles Lee
# Description:
# aws SDK need be installed, need run aws configure to setup your AWS ID and key.
#
 
import boto3
import botocore
from botocore.exceptions import ClientError
import csv
import sys
import argparse

CONSOLE_PREFIX = '.console.aws.amazon.com/ec2/v2/home?region=#LoadBalancers:'

def get_csv(elb_data):
    fileds = sorted(list(set(k for d in elb_data for k in d)))
    with open('CLBConsoleLink.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(fileds)
        for lb in elb_data:
            writer.writerow([lb.get(col, None) for col in fileds])

def get_output(elb_data):
    fileds = sorted(list(set(k for d in elb_data for k in d)))
    for item in fileds:
        print (item,end=' ')
    print()
    for lb in elb_data:
        print ([lb.get(col, None) for col in fileds], end = ' ')
        print()
   
def get_elb_data(region):
    elbc = boto3.client('elb', region_name=region)
    # Describes the specified Classic Load Balancer.
    try:
        paginator = elbc.get_paginator('describe_load_balancers')
    except botocore.exceptions.ClientError as e:
        logger.error(e.response['Error']['Message'])
    elb_data = []
    for describe_load_balancers in paginator.paginate():
    # Render a dictionary that contains the Classic Load Balancer attributes
        for lb in describe_load_balancers['LoadBalancerDescriptions']:
            elb_item = {}
            elb_item['DNSName']= lb['DNSName']
            elb_item['Scheme'] = lb['Scheme']
            elb_item['HostedZoneID'] = lb['CanonicalHostedZoneNameID']
            elb_item['Name'] = lb['LoadBalancerName']
            elb_item['ConsoleLink'] = 'https://' + str(region) + CONSOLE_PREFIX + str(region) + '#LoadBalancers:loadBalancerName=' + lb['LoadBalancerName']
            elb_item['CreatedTime'] = lb['CreatedTime']
            elb_item['AvailabilityZones'] = lb['AvailabilityZones']
            elb_item['BackendInstances'] = lb['Instances']
            # Check if a Classic Load Balancer is in EC2-Classic or EC2-VPC
            if not lb['Subnets']:
                elb_item['EC2Platform'] = 'EC2-Classic'
                elb_item['Subnets'] = None
                elb_item['SecurityGroup'] = lb['SourceSecurityGroup']['GroupName']
                elb_item['VPCId'] = None
            else:
                elb_item['EC2Platform'] = 'EC2-VPC'
                elb_item['Subnets'] = lb['Subnets']
                elb_item['SecurityGroup'] = lb['SecurityGroups']
                elb_item['VPCId'] = lb['VPCId']
            elb_data.append(elb_item)
    return elb_data

#Parse command line
def _parse_command_line():
    parser = argparse.ArgumentParser(description='ELB service', usage='%(prog)s --region --format')
    parser.add_argument("--region", help="The region of the Classic Load Balancers "
                                         "that you want to describe",required=True)
    parser.add_argument("--format", help="The format of the output file that you "
                                         "want to retrieve. Current ",required=True)

     # if no options, print help
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()       
    return  parser.parse_args()

def main():
    args = _parse_command_line()
    elb_data=get_elb_data(args.region)
    if args.format == 'output':
       get_output(elb_data)
    if args.format == 'csv':
       get_csv(elb_data)
if __name__ == "__main__":
   main()
