#!/bin/python3.6
from flask import Flask, request, jsonify, url_for, render_template, redirect
import subprocess, json
from json2html import *

app = Flask(__name__)
app.config['DEBUG'] = True

apigateway_list = ["get-account","get-api-keys","get-authorizers","get-base-path-mappings","get-client-certificates","get-deployments","get-documentation-parts","get-documentation-versions","get-domain-names","get-export","get-gateway-responses","get-integration-response","get-models","get-request-validators","get-resources","get-rest-apis","get-sdk-types","get-stages","get-tags","get-usage-plan-keys","get-usage-plans","get-vpc-links"]

coudwatch_list = ["describe-alarm-history","describe-alarms","list-metrics","list-dashboards"]

ec2_list = ["describe-addresses","describe-availability-zones","describe-hosts","describe-instance-status","describe-instances","describe-route-tables","describe-route-tables","describe-security-groups","describe-subnets","describe-volume-status","describe-volumes","describe-vpcs"]

elb_list = ["describe-account-limits","describe-load-balancers","describe-load-balancer-policies","describe-load-balancer-policy-types"]

iam_list = ["list-access-keys","list-account-aliases","list-attached-group-policies","list-attached-role-policies","list-attached-user-policies","list-entities-for-policy","list-group-policies","list-groups","list-groups-for-user","list-instance-profiles","list-instance-profiles-for-role","list-mfa-devices","list-open-id-connect-providers","list-policies","list-policy-versions","list-role-policies","list-roles","list-saml-providers","list-ssh-public-keys","list-server-certificates","list-service-specific-credentials","list-signing-certificates","list-user-policies","list-users"]

lambda_list = ["list-event-source-mappings","list-functions"]

rds_list = ["describe-account-attributes","describe-certificates","describe-db-cluster-backtracks","describe-db-cluster-parameter-groups","describe-db-cluster-parameters","describe-db-cluster-snapshot-attributes","describe-db-cluster-snapshots","describe-db-clusters","describe-db-engine-versions","describe-db-instances","describe-db-log-files","describe-db-parameter-groups","describe-db-parameters","describe-db-security-groups","describe-db-snapshot-attributes","describe-db-snapshots","describe-db-subnet-groups","describe-engine-default-cluster-parameters","describe-engine-default-parameters","describe-event-categories","describe-event-subscriptions","describe-events","describe-option-group-options","describe-option-groups","describe-orderable-db-instance-options","describe-pending-maintenance-actions","describe-reserved-db-instances","describe-reserved-db-instances-offerings","describe-source-regions","describe-valid-db-instance-modifications"]

route53_list = ["list-geo-locations","list-health-checks","list-hosted-zones","list-hosted-zones-by-name","list-query-logging-configs","list-resource-record-sets","list-reusable-delegation-sets","list-tags-for-resource","list-tags-for-resources","list-traffic-policies","list-traffic-policy-instances","list-traffic-policy-instances-by-hosted-zone","list-traffic-policy-instances-by-policy","list-traffic-policy-versions","list-vpc-association-authorizations"]


profile_list = [
"em-qa-dev",
"em-qa-prod",
"em-pso-dev",
"em-encw-dev",
"em-platform-audit-prod",
"em-platform-audit-dev",
"em-epc2-prod",
"em-epc2-dev",
"em-ebsasync-prod",
"em-ebsasync-dev",
"em-cpe-prod",
"em-cpe-dev",
"em-bizops-dev",
"em-accord-prod",
"em-accord-dev",
"em-eventbus-prod",
"em-eventbus-dev",
"em-top-prod",
"em-top-dev",
"em-consumer-connect-prod",
"em-infosec-dev",
"em-consumer-connect-dev",
"em-webhooks-prod",
"em-webhooks-dev",
"em-encompassdb-dev",
"em-devtools-dev",
"em-streams-prod",
"em-streams-dev",
"em-eds-prod",
"em-analytics-prod",
"em-ems3-dev",
"em-krypto-nonprod-dev",
"em-iamcloud-prod",
"em-iamcloud-dev",
"em-capitalyze-dev",
"em-citrix-dev",
"em-velocify-prod",
"em-velocify-dev",
"em-pds-prod",
"em-cv-dev",
"em-datascience-databricks-sandbox",
"em-analytics-dev",
"em-efs-prod",
"em-efs-dev",
"em-mavent-prod",
"em-shared-concept",
"em-allregs-prod",
"em-resource-center-prod",
"em-resource-center-dev",
"em-deploy-dev",
"em-deploy-prod",
"em-mythos-purpleteam-dev",
"em-availableaccount-dev",
"em-prius-service-dev",
"em-mythos-ebs-dev",
"em-marketing-prod",
"em-identity-platform-prod",
"em-identity-platform-dev",
"em-entitlements-prod",
"em-entitlements-dev",
"em-performance-prod",
"em-performance-dev",
"em-epc-prod",
"em-epc-dev",
"em-training-prod",
"em-training-dev",
"em-vdi-prod",
"em-payment-prod",
"em-payment-dev",
"em-devops-prod",
"em-devops-dev",
"em-sre-prod",
"em-sre-dev",
"em-ebs-prod",
"em-ebs-dev",
"em-workflow-prod",
"em-edm-prod",
"em-infra-corp",
"em-datascience-prod",
"em-datascience-dev",
"em-iameng-prod",
"em-dev-corp",
"em-available-account-1-corp",
"em-allregs-corp",
"em-ecrm-dev",
"em-epps-prod",
"em-krypto-prod",
"em-krypto-dev",
"em-eds-dev",
"em-beacon-prod",
"em-beacon-dev",
"em-dps-prod",
"em-dps-dev",
"em-secops-prod",
"em-techpubs-prod",
"em-secops-dev",
"em-techpubs-dev",
"em-transit-dev",
"em-data-prod",
"em-iamtest-dev",
"em-pds-dev",
"em-iamprod-prod",
"em-support-prod",
"em-workflow-dev",
"em-edm-dev",
"em-automation-test-framework-dev",
"em-screenflow-prod",
"em-infra-dev",
"em-mavent-dev",
"em-avs-prod",
"em-notification-prod",
"em-allregs-dev",
"em-avs-dev",
"em-support-dev",
"em-mobile-prod",
"em-mgmt-prod",
"em-kelvin1-prod",
"em-publiccloud-dev",
"em-audit-prod",
"em-infra-prod",
"em-hackathon-dev",
"em-shared-sandbox",
"em-shared-dev",
"em-devtools-prod",
"em-shared-prod",
"em-marketing-dev",
"em-architecture-dev",
"em-data-dev",
"em-epps-dev",
"em-screenflow-dev",
"em-notification-dev",
"em-apigw-prod",
"em-apigw-dev",
"em-vdi-dev",
"em-ecrm-prod",
"em-master-prod"]


Performance_dict = {
"PPkZrjsH2q":"Amazon EBS Provisioned IOPS Volume Attachment Configuration",
"Bh2xRR2FGH":"Amazon EC2 to EBS Throughput Optimization ",
"B913Ef6fb4":"Amazon Route 53 Alias Resource Record Sets ",
"N420c450f2":"CloudFront Alternate Domain Names ",
"796d6f3D83":"CloudFront Content Delivery Optimization ",
"N415c450f2":"CloudFront Header Forwarding and Cache Hit Ratio ",
"ZRxQlPsb6c":"High Utilization Amazon EC2 Instances ",
"j3DFqYTe29":"Large Number of EC2 Security Group Rules Applied to an Instance ",
"k3J2hns32g":"Overutilized Standard Amazon EBS Volumes "
}

Security_dict = {
"ePs02jT06w":"Amazon EBS Public Snapshots",
"rSs93HQwa1":"Amazon RDS Public Snapshots",
"nNauJisYIT":"Amazon RDS Security Group Access Risk",
"c9D319e7sG":"Amazon Route 53 MX and SPF Resource Record Sets",
"Pfx0RwqBli":"Amazon S3 Bucket Permissions",
"vjafUGJ9H0":"AWS CloudTrail Logging",
"N425c450f2":"CloudFront Custom SSL Certificates in the IAM Certificate Store",
"N430c450f2":"CloudFront SSL Certificate on the Origin Server",
"a2sEc6ILx":"ELB Listener Security",
"xSqX82fQu":"ELB Security Groups",
"DqdJqYeRm5":"IAM Access Key Rotation",
"Yw2K9puPzl":"IAM Password Policy",
"zXCkfM1nI3":"IAM Use Security",
"7DAFEmoDos":"MFA on Root Account",
"HCP4007jGY":"Security Groups - Specific Ports Unrestricted",
"1iG5NDGVre":"Security Groups - Unrestricted Access"
}

CostOptimization_dict = {
"1e93e4c0b5":"Amazon EC2 Reserved Instance Lease Expiration",
"1MoPEMsKx6":"Amazon EC2 Reserved Instances Optimization",
"Ti39halfu8":"Amazon RDS Idle DB Instances",
"51fC20e7I2":"Amazon Route 53 Latency Resource Record Sets",
"hjLMh88uM8":"Idle Load Balancers",
"Qch7DwouX1":"Low Utilization Amazon EC2 Instances",
"Z4AUBRNSmz":"Unassociated Elastic IP Addresses",
"DAvU99Dc4C":"Underutilized Amazon EBS Volumes",
"G31sQ1E9U":"Underutilized Amazon Redshift Clusters"
}

FaultTolerance_dict = {
"xuy7H1avtl":"Amazon Aurora DB Instance Accessibility",
"H7IgTzjTYb":"Amazon EBS Snapshots",
"wuy7G1zxql":"Amazon EC2 Availability Zone Balance",
"opQPADkZvH":"Amazon RDS Backups",
"f2iK5R6Dep":"Amazon RDS Multi-AZ",
"Cb877eB72b":"Amazon Route 53 Deleted Health Checks",
"b73EEdD790":"Amazon Route 53 Failover Resource Record Sets",
"C056F80cR3":"Amazon Route 53 High TTL Resource Record Sets",
"cF171Db240":"Amazon Route 53 Name Server Delegations",
"BueAdJ7NrP":"Amazon S3 Bucket Logging",
"R365s2Qddf":"Amazon S3 Bucket Versioning",
"CLOG40CDO8":"Auto Scaling Group Health Check",
"8CNsSllI5v":"Auto Scaling Group Resources",
"0t121N1Ty3":"AWS Direct Connect Connection Redundancy",
"8M012Ph3U5":"AWS Direct Connect Location Redundancy",
"4g3Nt5M1Th":"AWS Direct Connect Virtual Interface Redundancy",
"V77iOLlBqz":"EC2Config Service for EC2 Windows Instances",
"7qGXsKIUw":"ELB Connection Draining",
"xdeXZKIUy":"ELB Cross-Zone Load Balancing",
"tfg86AVHAZ":"Large Number of Rules in an EC2 Security Group",
"iqdCTZKCUp":"Load Balancer Optimization",
"Wnwm9Il5bG":"PV Driver Version for EC2 Windows Instances",
"S45wrEXrLz":"VPN Tunnel Redundancy"
}

ServiceLimits_dict = {
"fW7HH0l7J9":"Auto Scaling - Groups",
"aW7HH0l7J9":"Auto Scaling - Launch Configurations",
"gW7HH0l7J9":"CloudFormation - Stacks",
"eI7KK0l7J9":"EBS - Active Snapshots ",
"fH7LL0l7J9":"EBS - Active Volumes ",
"dH7RR0l6J9":"EBS - General Purpose SSD Volume Storage ",
"cG7HH0l7J9":"EBS - Magnetic (standard) Volume Storage ",
"tV7YY0l7J9":"EBS - Provisioned IOPS (SSD) Volume Aggregate IOPS ",
"gI7MM0l7J9":"EBS - Provisioned IOPS SSD (io1) Volume Storage ",
"aW9HH0l8J6":"EC2 - Elastic IP Addresses ",
"0Xc6LMYG8P":"EC2 - On-Demand Instances ",
"iH7PP0l7J9":"EC2 - Reserved Instance Leases ",
"iK7OO0l7J9":"ELB - Active Load Balancers ",
"sU7XX0l7J9":"IAM - Group ",
"nO7SS0l7J9":"IAM - Instance Profiles ",
"rT7WW0l7J9":"IAM - Server Certificates ",
"qS7VV0l7J9":"IAM - Users ",
"bW7HH0l7J9":"Kinesis - Shards per Region",
"jtlIMO3qZM":"RDS - Cluster Parameter Groups ",
"7fuccf1Mx7":"RDS - Cluster roles ",
"gjqMBn6pjz":"RDS - Clusters ",
"XG0aXHpIEt":"RDS - DB Instances ",
"jEECYg2YVU":"RDS - DB Parameter Groups ",
"gfZAn3W7wl":"RDS - DB Security Groups ",
"dV84wpqRUs":"RDS - DB snapshots per user ",
"keAhfbH5yb":"RDS - Event Subscriptions ",
"dBkuNCvqn5":"RDS - Max Auths per Security Group ",
"3Njm0DJQO9":"RDS - Option Groups ",
"pYW8UkYz2w":"RDS - Read Replicas per Master ",
"UUDvOa5r34":"RDS - Reserved Instances ",
"dYWBaXaaMM":"RDS - Subnet Groups ",
"jEhCtdJKOY":"RDS - Subnets per Subnet Group ",
"P1jhKWEmLa":"RDS - Total Storage Quota ",
"hJ7NN0l7J9":"SES - Daily Sending Quota ",
"lN7RR0l7J9":"VPC - Elastic IP Address ",
"kM7QQ0l7J9":"VPC - Internet Gateways ",
"jL7PP0l7J9":"VPC - Network Interfaces "
}

def show_all():
   json_data = {}
   for p in profile_list:
       command = 'aws support describe-trusted-advisor-check-result --check-id "Qch7DwouX1" --region us-east-1 --profile %s' %(p)
       output = subprocess.check_output(command,shell=True)
       data = json.loads(output.decode('utf-8'))
       json_data = json_data.append(data)
   json_results = json.dumps(json_data, indent=4,sort_keys=True)
   return json2html.convert(json=json_results)

def show_describe_trusted_advisor_check_result(id,p):
   command = '/bin/aws support describe-trusted-advisor-check-result --check-id %s --region us-east-1 --profile %s' %(id, p)
   output = subprocess.check_output('/bin/aws support describe-trusted-advisor-check-result --check-id %s --region us-east-1 --profile %s' %(id, p),shell=True)
   data = json.loads(output.decode('utf-8'))
   json_results = json.dumps(data, indent=4,sort_keys=True)
   return json2html.convert(json=json_results)


@app.route("/")
def main():
    html = render_template('ta.html')
    return html

@app.route('/show_ta', methods = ['POST'])
def show_ta():
    resp = ""
    list = []
    for field in request.form.keys():
       print (field)
       list.append(field)     
    
    profile = request.form[list[0]]
    id = request.form[list[1]]

    if id in Security_dict:
      ta_name = "Security"
      service = Security_dict[id]
      table= show_describe_trusted_advisor_check_result(id,profile)
    elif id in ServiceLimits_dict:
      ta_name = "Service Limits"
      service = ServiceLimits_dict[id]
      table= show_describe_trusted_advisor_check_result(id,profile)
    elif id in CostOptimization_dict:
      ta_name = "Cost Optimization"
      service = CostOptimization_dict[id]
      table= show_describe_trusted_advisor_check_result(id,profile)
    elif id in FaultTolerance_dict:
      ta_name = "Fault Tolerance"
      service = FaultTolerance_dict[id]
      table= show_describe_trusted_advisor_check_result(id,profile)
    elif id in Performance_dict:
      ta_name = "Performance"
      service = Performance_dict[id]
      table = show_describe_trusted_advisor_check_result(id,profile)
    else:
         print ('print All Cost')
         table = show_all ()

    resp = "<div> <font color=blue> <a href='/'>HOME</a></font><br><br></div><b>{key}</b>: {value}<br>".format(key=" The profile is : " + profile.upper() + " , The Trusted Advisor Service Name is : " + ta_name.upper() + " , The Trused Advisor service is : " + service.upper() + " , The Trused Advisor ID is : " + id.upper() ,value=table)
    return resp 

if __name__ == "__main__":
   app.run(host='0.0.0.0',port=80)
