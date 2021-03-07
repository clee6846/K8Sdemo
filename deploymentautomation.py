#!/usr/bin/env python3
##############################################################################
#  The script includes functions of
#  1. To disable/enable jobs in project Level
#     To run 
#     for example 
#     to disable all workflow, report jobs for customer novartisus in project NOVARTIS level
#     deploymentautomation.py -c novartisus -s U
#    or disable all workflow, report jobs for customer novartiscn in project NOVARTIS-CN-PROD level
#     deploymentautomation.py -c novartiscn -s U
#     to enable  all workflow, report jobs for customer novartisus in project NOVARTIS level
#     deploymentautomation.py -c novartisus -s R
#    or disable all workflow, report jobs for customer novartiscn in project NOVARTIS-CN-PROD level
#     deploymentautomation.py -c novartiscn -s e
#
#  2. To unschedule/reschedule jobs in Jobs Level
#     To run 
#     for example
#     to disable all workflow jobs for customer novartisus in project NOVARTIS level
#     deploymentautomation.py -c novartisus -s u
#     to disable all workflow jobs for customer novartiscn in project NOVARTIS-CN-PROD level
#     deploymentautomation.py -c novartiscn -s u
#     to enable  all workflow jobs for customer novartisus in project NOVARTIS level
#     deploymentautomation.py -c novartisus -s r
#     to enable  all workflow jobs for customer novartisus in project NOVARTIS-CN-PROD level
#     deploymentautomation.py -c novartiscn -s r
#     include two BASH scripts
#     LISTSCHEDULERJOB = 'listscheduler.sh'
#     LISTBDPSCHEDULERJOB = 'list_bdp_scheduler_jobs.sh'
#     UNRESCHEDULEDJOBS = 'unrescheduledjobs.sh'
#
#  3. To backup tables include table contents
#     To run 
#     for example to backup pre selected tables in prod
#     deploymentautomation.py -c novartisus -s b
#     will backup all regarding tables with contents in novsrtisusprod database
#     to backup particular tables in particular database
#     rundeckmanager -c novsrtisus -s B -d novartisusprod_stage -t AKT_Survey AKT_SurveyQuestionEvent AKT_SurveyQuestionHold
#
#  4. assign/deprive QA acl [run,kill] permissions during deployment
#     Before deployment we will QA the privileges to run and kill production jobs.
#     To run 
#     for example
#     assign acl [run,kill] rights to QA of customer novartisus 
#     deploymentautomation.py -c novsrtisus -A
#     deprive acl [run,kill] rights to QA of customer novartisus 
#     deploymentautomation.py -c novsrtisus -R
#     include two BASH scripts : 
#     ASSIGNTEMPACLPOLICY = 'assigndeprivedeployaclpolicy.sh'
#     DEPRIVETEMPACLPOLICY = 'assigneprivedeployaclpolicy.sh'
#
#  5. load all jobs definitions from one project to the next project
#     To run,
#     for example, to load all jobs from UAT to prod
#     assume project SANOFI-US-PROD has been created
#     deploymentautomation.py -c sanofius -s P
#  
#  6. To take RDS snapshot
#     Before the deployment to take RDS snapshot
#     for example:
#     deploymentautomation.py -c sanofius -s s      
#
#  By : Charles Lee 5-7-2020
#
#############################################################################
import subprocess
import argparse
import os
import sys
import time

DATETIME = time.strftime('%Y%m%d-%H%M%S')

Customers = {
'msdca' : ['bdpus001.xxxxx.com','rundeck-us'],
'novartisus' : ['bdpus001.xxxxx.com','rundeck-us'],
'sanofius' : ['bdpus001.xxxxx.com','rundeck-sanofius'],
'leous' : ['bdpus001.xxxxx.com','rundeck-leous'],
'bayerca' : ['bdpus002.xxxxx.com','rundeck-bayerca'],
'gskus' : ['bdpus002.xxxxx.com','rundeck-gskus'],
'lillyus' : ['bdpus003.xxxxx.com','rundeck-lillyus'],
'novartisbr' : ['bdpus003.xxxxx.com','rundeck-novartisbr'],
'novartisca' : ['bdpus003.xxxxx.com','rundeck-novartisca'],
'emdseronous' : ['bdpus003.xxxxx.com','rundeck-emdseronous'],
'pfizerus' : ['bdpus005.xxxxx.com','rundeck-pfizerus'],
'msdja' : ['bdpjp001.xxxxx.com','rundeck-msdja'],
'novartisau' : ['bdpjp001.xxxxx.com','rundeck-novartisau'],
'ucbcn' : ['bdpjp001.xxxxx.com','rundeck-ucbcn'],
'dmmsdcn' : ['bdpjp001.xxxxx.com','rundeck-dmmsdcn'],
'bdpjp' : ['bdpjp001.xxxxx.com','rundeck-bdpjp'],
'janssencn' : ['bdpjp002.xxxxx.com','rundeck-janssencn'],
'bayerja' : ['bdpjp002.xxxxx.com','rundeck-bayerja'],
'janssenja' : ['bdpjp002.xxxxx.com','rundeck-janssenja'],
'novartisjp' : ['bdpjp002.xxxxx.com','rundeck-novartisjp'],
'pfizerjp' : ['bdpjp003.xxxxx.com','rundeck-pfizerjp'],
'pfizercn' : ['bdpjp003.xxxxx.com','rundeck-pfizercn'],
'chugaijp' : ['bdpjp003.xxxxx.com','rundeck-chugaijp'],
'bijp' : ['bdpjp003.xxxxx.com','rundeck-bijp'],
'merckcn' : ['bdpjp003.xxxxx.com','rundeck-merckcn'],
'novartiscn' : ['bdpjp003.xxxxx.com','rundeck-novartiscn'],
'biogeneu' : ['bdpeu001.xxxxx.com','rundeck-eu'],
'msdes' : ['bdpeu001.xxxxx.com','rundeck-eu'],
'msdgb' : ['bdpeu001.xxxxx.com','rundeck-eu'],
'msdit' : ['bdpeu001.xxxxx.com','rundeck-eu'],
'pfizerde' : ['bdpeu001.xxxxx.com','rundeck-pfizerde'],
'pfizerfr' : ['bdpeu001.xxxxx.com','rundeck-pfizerfr'],
'novartisde' : ['bdpeu001.xxxxx.com','rundeck-novartisde'],
'bayerfr' : ['bdpeu002.xxxxx.com','rundeck-bayerfr'],
'pfizeruk' : ['bdpeu002.xxxxx.com','rundeck-pfizeruk'],
'novartises' : ['bdpeu002.xxxxx.com','rundeck-novartises'],
'bayeruk' : ['bdpeu002.xxxxx.com','rundeck-bayeruk'],
'pfizeres' : ['bdpeu003.xxxxx.com','rundeck-pfizeres'],
'bayerde' : ['bdpeu003.xxxxx.com','rundeck-bayerde'],
'novartisuk' : ['bdpeu003.xxxxx.com','rundeck-novartisuk'],
'bayerit' : ['bdpeu003.xxxxx.com','rundeck-bayerit'],
'novartisit' : ['bdpeu003.xxxxx.com','rundeck-novartisit'],
'msdfr' : ['bdpeu003.xxxxx.com','rundeck-msdfr'],
'msdde' : ['bdpeu003.xxxxx.com','rundeck-msdde'],
'novartisfr' : ['bdpeu005.xxxxx.com','rundeck-novartisfr'],
'pfizerit' : ['bdpeu005.xxxxx.com','rundeck-pfizerit']
}

usrds = ['leousrds.xxxxx.com','gskusrds.xxxxx.com', 'lillyusrds-encrypted.xxxxx.com', 'pfizerusrds-encrypted.xxxxx.com', 'sanofiusrds.xxxxx.com', 'novartisbrrds.xxxxx.com', 'bayercards.xxxxx.com', 'emdseronousrds.xxxxx.com', 'msdcards.xxxxx.com', 'novartisusrds.xxxxx.com','novartiscards.xxxxx.com']

eurds = ['bayerderds.xxxxx.com','bayerfrrds.xxxxx.com','bayerukrds.xxxxx.com','msdderds.xxxxx.com','msdesrds.xxxxx.com','msdfrrds.xxxxx.com','msdgbrds.xxxxx.com','msditrds.xxxxx.com','novartisderds.xxxxx.com','novartisesrds.xxxxx.com','novartisfrrds.xxxxx.com','novartisitrds.xxxxx.com','novartisukrds.xxxxx.com','pfizerderds.xxxxx.com','pfizerukrds.xxxxx.com', 'bayeritrds.xxxxx.com']

asiards = ['pfiszercnrds.xxxxx.com','pfizerjards.xxxxx.com','janssenjards.xxxxx.com','bayerjards.xxxxx.com', 'msdjards.xxxxx.com', 'novartisjprds.xxxxx.com','novartiscnrds.xxxxx.com','merckcnrds.xxxxx.com', 'bijprds.xxxxx.com', 'msdcnrds.xxxxx.com','ucbcnrds.xxxxx.com','novartisaurds.xxxxx.com']

WORKDIR = '/mnt/data/rundeck/workspace/operations/deploymentutilities'
TMP = '/tmp'
RUNNINGJOBSOUTPUT = 'runningjobs.' + DATETIME + '.txt'
JOBIDSOUTPUT = 'jobids.' + DATETIME + '.txt'
JOBSCHEDULEROUTPUT = 'scheduler.' + DATETIME + '.txt'
SCHEDULER = 'scheduler.' + DATETIME + '.txt'
LISTEXECUTIONS = 'listexecutions.sh'
UNRESCHEDULEDJOBS = 'unrescheduledjobs.sh'
KILLJOBS = 'killjobs.sh'
LISTSCHEDULERJOB = 'listscheduler.sh'
LISTBDPSCHEDULERJOB = 'list_bdp_scheduler_jobs.sh'
DOWNLOADJOBS = 'downloadjobsdefinitions.sh'
UPLOADJOBS = 'uploadjobsdefinitions.sh'
ASSIGNTEMPACLPOLICY = 'assigndeprivedeployaclpolicy.sh'
ASSIGNQATEMPACLPOLICY = 'assigndepriveQAdeployaclpolicy.sh'
ASSIGNCSTEMPACLPOLICY = 'assigndepriveCSdeployaclpolicy.sh'
ASSIGNDEVTEMPACLPOLICY = 'assigndepriveDEVdeployaclpolicy.sh'
DEPRIVEQATEMPACLPOLICY = 'assigndepriveQAdeployaclpolicy.sh'
DEPRIVECSTEMPACLPOLICY = 'assigndepriveCSdeployaclpolicy.sh'
DEPRIVEDEVTEMPACLPOLICY = 'assigndepriveDEVdeployaclpolicy.sh'
RDSBACKUP = 'rdsbackup.py'
BDPUSURL = 'https://ops-bdpus.xxxxx.com'
BDPUSHOST = 'bdpus001.xxxxx.com'
BDPEUURL = 'https://ops-bdpeu.xxxxx.com'
BDPEUHOST = 'bdpeu001.xxxxx.com'
BDPASIAHOST= 'bdpjp001.xxxxx.com'
USREGION = 'us'
EUREGION = 'eu'
ASIAREGION = 'jp'
LOCALBIN = '/usr/local/bin'

##################################################################################################
# from the current VPC, it's unable to connect to the RDS directly, we need to
# ssh log in the host colocation in a VPC with the RDS to run python script on the host
##################################################################################################

def rdstablebackup(customer, *args):
   if customer == 'lillyus' or customer == 'pfizerus':
      tunnelhost = BDPUSHOST
   if customer + "rds.xxxxx.com" in usrds:
       tunnelhost = BDPUSHOST
    #   print(host)
   elif customer + "rds.xxxxx.com" in eurds:
       tunnelhost = BDPEUHOST
    #   print (host)
   elif customer + "rds.xxxxx.com" in asiards:
       tunnelhost = BDPASIAHOST
    #  print (host)
   destdir = LOCALBIN
   source = WORKDIR + "/" + RDSBACKUP
   runfile = LOCALBIN + "/" + RDSBACKUP
   subprocess.Popen(["scp",source,"%s:%s" % (tunnelhost,destdir)]).wait()
   if len(args) == 0:
      database = customer + 'uat'
      print( 'Running ', customer, ' ', database, ' tables backup')
      emptytable = ''
      subprocess.Popen(["ssh","-t","-t", "%s" % tunnelhost,runfile, "-c", "%s" % customer, "-s", "t", "-d", "%s" % database, "-t", "%s" % emptytable]).wait()
   else:
      print( 'Running ', customer, 'production tables backup')
      database = args[0]
      tables = args[1]
      str1 = ' '
      str1 = str1.join(tables)
      subprocess.Popen(["ssh","-t","-t", "%s" % tunnelhost,runfile,"-c", "%s" % customer, "-s", "t", "-d", "%s" % database, "-t", "%s" % str1]).wait()

def rdstakesnapshot(customer, description):
   runfile = WORKDIR + "/" + RDSBACKUP
   print( 'Taking Snapshot of  ', customer )
   subprocess.Popen([runfile,"-c", "%s" % customer, "-s", "s", "-D", "%s" % description[0]]).wait()


#########################################################################################################

def get_HOST_RUNDECK_PROJECT_URL(customer):
   global HOST, RUNDECK, PROJECT, URL
   for key, values in Customers.items():
       if key == customer:
          print (values[0],values[1])
          HOST = values[0]
          RUNDECK = values[1]
   bdpus = ['novartisus','msdca']
   bdpeu = ['biogeneu','msdes','msdgb','msdit']
   if customer in bdpeu:
      URL = "https://ops-bdpeu.xxxxx.com/api/22"
      for cust in bdpeu:
         if cust  == 'biogeneu' and customer == cust:
            PROJECT = "BIOGEN"
         elif cust == 'msdes' and customer == cust:
            PROJECT = 'MSD_ES'
         elif cust == 'msdgb' and customer == cust:
            PROJECT = 'MSD_GB'
         elif cust == 'msdit'and customer == cust:
            PROJECT = 'MSD_IT'
   elif customer  in bdpus:
      URL = "https://ops-bdpus.xxxxx.com/api/21"
      for cust in bdpus:
         if cust == 'msdca' and customer == cust:
            PROJECT = 'MSD_CA'
         elif cust == 'novartisus' and customer == cust:
            PROJECT = 'NOVARTIS'
   else:
      URL = "https://ops-bdp-" + customer + ".xxxxx.com/api/24"
      l = list(customer)
      l = [x.upper() for x in l]
      str1 = ''
      str2 = ''
      PROJECT = ''
      PROJECT = str1.join(l[:-2]) + "-" +str2.join(l[-2:]) + "-PROD"
      print (PROJECT)
      print (URL)
   #command = "ssh " + host + " \"docker exec -i " + rundeck + " bash -c \'export RD_URL=" + URL + ";export RD_USER=ansible;export RD_PASSWORD=" + PASSWORD + ";rd executions list -p " + PROJECT +" \'\""
   #print (command)



###################################################################################################
# Here to swap ACL policy is a tedious job
#
def assign_deploy_aclpolicy(customer,group):
   get_HOST_RUNDECK_PROJECT_URL(customer)
   if group == 'QA':
      subprocess.run([WORKDIR + "/" + ASSIGNQATEMPACLPOLICY,HOST,RUNDECK,URL,PROJECT,'a'])
   elif group == 'CS':
      subprocess.run([WORKDIR + "/" + ASSIGNCSTEMPACLPOLICY,HOST,RUNDECK,URL,PROJECT,'a'])
   elif group == 'Dev':
      subprocess.run([WORKDIR + "/" + ASSIGNDEVTEMPACLPOLICY,HOST,RUNDECK,URL,PROJECT,'a'])

def deprive_deploy_aclpolicy(customer,group):
   get_HOST_RUNDECK_PROJECT_URL(customer)
   if group == 'QA':
      subprocess.run([WORKDIR + "/" + ASSIGNQATEMPACLPOLICY,HOST,RUNDECK,URL,PROJECT,'d'])
   elif group == 'CS':
      subprocess.run([WORKDIR + "/" + ASSIGNCSTEMPACLPOLICY,HOST,RUNDECK,URL,PROJECT,'d'])
   elif group == 'Dev':
      subprocess.run([WORKDIR + "/" + ASSIGNDEVTEMPACLPOLICY,HOST,RUNDECK,URL,PROJECT,'d'])


####################################################################################################

def download_Rundeck_PreEnv_upload_to_NextEnv(customer,env):
    preenv = ''
    pre = ''
    target = ''
    if env == 'U':
      preenv = 'D'
      pre = 'dev'
      target = 'uat'
    elif env == 'P':
      preenv = 'U'
      pre = 'uat'
      target = 'prod'
    elif env == 'T':
      preenv = 'U'
      pre = 'uat'
      target = 'test'
    elif env == 'E':
      prevenv = 'U'
      pre = 'uat'
      target = 'preprod'
    else:
      print ("Wrong env")
    subprocess.run([WORKDIR + DOWNLOADJOBS, customer, pre.upper()])
    xmlfile1 = TMP + "/" + customer + '-' + pre.upper() + '.xml'
    xmlfile2 = TMP + "/" + customer + '-' + target.upper() + '.xml'
    xml1 = open(xmlfile1,"r")
    xml2 = open(xmlfile2,"w")
    for line in xml1:
        string = line.strip()
        if 'uat' in string:
           xml2.write(string.replace(pre,target))
           xml2.write("\n")
        elif pre.upper() in string:
           xml2.write(string.replace(pre.upper(),target.upper()))
           xml2.write("\n")
        else:
           xml2.write(string)
           xml2.write("\n")
    xml1.close()
    xml2.close()

    #subprocess.run([WORKDIR + UPLOADJOBS, customer, target.upper()])


def get_running_job_ids_and_kill(customer):
   get_HOST_RUNDECK_PROJECT_URL(customer)
   customerrunningjobs = TMP + "/" + customer + RUNNINGJOBSOUTPUT
   with open(customerrunningjobs, "w") as f1:
     print("checking current running jobs")
     subprocess.call([WORKDIR + "/" + LISTEXECUTIONS, HOST, RUNDECK, URL, PROJECT], stdout=f1)
   array = [] 
   with open(customerrunningjobs,"r") as f2:
     for line in f2:
         array.append(line.strip())
   if len(array) >= 1:
      array = array[1:]
      for item in array:
         #print (list(item.split())[6])
         print (list(item.split()))
         jobid = list(item.split())[6]
         print (" Pause 1 minute to check the job, if you don't want to kill this  ", jobid, "Please kill this Rundeck job")
         time.sleep(60)
         print("60 seconds passed, killing job id", jobid)
         subprocess.call([WORKDIR + KILLJOBS, HOST, RUNDECK, URL, jobid])
         print("checking current running jobs")
         subprocess.call([WORKDIR + "/" + LISTEXECUTIONS, HOST, RUNDECK, URL, PROJECT])

######################################################################################################
 
def get_scheduled_job_ids_and_reschedule_jobs(customer):
    get_HOST_RUNDECK_PROJECT_URL(customer)
    customersavedidfile = TMP + "/" + customer + "UnscheduledID.txt"
    print (customersavedidfile)
    with open (customersavedidfile, "r") as f:
      customerjobids = f.read()
      print(customerjobids)
      with open (customerjobids, "r") as f1:
          for line in f1:
             #print (line)
             jobid=line.strip()
             print("jobid: ",jobid) 
             subprocess.call([WORKDIR + "/" + UNRESCHEDULEDJOBS, HOST, RUNDECK, URL, PROJECT, jobid, 'r'])

#####################################################################################################

def print_ids(customer,job):
   get_HOST_RUNDECK_PROJECT_URL(customer)

   customerjobids = TMP + "/" + customer + JOBIDSOUTPUT
   if 'scheduled: true' in job and 'scheduleEnabled: true' in job and 'enabled: true' in job:
      with open (customerjobids, "a+") as f1:
          for line in job:
             if line.startswith('id:'):
                #print (line.split(':')[1].strip())
                jobid = line.split(':')[1].strip()
                f1.write(jobid)
                f1.write("\n")
                print("jobid :",jobid)
                subprocess.call([WORKDIR  + "/" + UNRESCHEDULEDJOBS, HOST, RUNDECK, URL, PROJECT, jobid, 'u'])
   customersavedidfile = TMP + "/" + customer + "UnscheduledID.txt"
   with open (customersavedidfile,'w') as f2:
        f2.write (customerjobids)
      
##############################################################################################################
# unschedule customer's jobs in job level
##############################################################################################################

def get_scheduled_job_ids_and_unschedule_jobs(customer):
   get_HOST_RUNDECK_PROJECT_URL(customer)
   biglist = []
   list =[]
   customerscheduler = TMP + "/" + customer + SCHEDULER
   with open(customerscheduler,"w+") as f1:
     if customer == 'novartisus' or customer == 'msdca':
        subprocess.call([WORKDIR + "/" + LISTBDPSCHEDULERJOB, BDPUSHOST, BDPUSURL, USREGION], stdout=f1)
     elif customer == 'biogeneu' or customer == 'msdes' or customer == 'msdgb' or customer == 'msdit':
        subprocess.call([WORKDIR + "/" + LISTBDPSCHEDULERJOB, BDPEUHOST, BDPEUURL, EUREGION], stdout=f1)
     else:
        subprocess.call([WORKDIR + "/" + LISTSCHEDULERJOB, HOST, RUNDECK, URL], stdout=f1)
   
   with open(customerscheduler) as f:
     for line in f:
         line=line.strip()
         #print(line)
         if line.startswith("id:") or line.startswith("name:") or line.startswith("group:") or line.startswith("project:") or line.startswith("href:") or line.startswith("permalink:")  or  line.startswith("scheduled:") or line.startswith("scheduleEnabled:") or line.startswith("description:") or line.startswith("scheduled:") or line.startswith("shceduleEnabled:"):
             list.append(line)
         elif line.startswith("enabled"):
             list.append(line)
             biglist.append(list)
             list = []
   
   customerjobids = TMP + "/" + customer + JOBIDSOUTPUT
   if os.path.exists(customerjobids):
      os.remove(customerjobids)
   for job in biglist:
      if customer == 'novartisus':
         if 'project: NOVARTIS' in job:            
            if 'group: Workflow-prod' in job or 'group: Workflow-PROD' in job:
               print_ids(customer,job)
      elif customer == 'msdca':
         if 'project: MSD_CA' in job:
            if 'group: Workflow-prod' in job or 'group: Workflow-PROD' in job:
               print_ids(customer,job)
      elif customer == 'biogeneu':
         if 'project: BIOGEN' in job:
            if 'group: Workflow-prod' in job or 'group: Workflow-PROD' in job:
               print_ids(customer,job)
      elif customer == 'msdes':
         if 'project: MSD_ES' in job:
            if 'group: Workflow-prod' in job or 'group: Workflow-PROD' in job:
               print_ids(customer,job)
      elif customer == 'msdgb':
         if 'project: MSD_GB' in job:
            if 'group: Workflow-prod' in job or 'group: Workflow-PROD' in job:
               print_ids(customer,job)
      elif customer == 'msdit':
         if 'project: MSD_IT' in job:
            if 'group: Workflow-prod' in job or 'group: Workflow-PROD' in job:
               print_ids(customer,job)
      else:
         if 'group: Workflow-prod' in job or 'group: Workflow-PROD' in job:
            print_ids(customer,job)

#############################################################################################################
# disable sheduled customer jobs in project level
#############################################################################################################

def disable_scheduled_customer_jobs_in_project_level(customer):
    get_HOST_RUNDECK_PROJECT_URL(customer)
    PROJECTCONFIGUREFILE = TMP + '/' + 'projectconfiguration.' + DATETIME + '.properties'
    with open (PROJECTCONFIGUREFILE , "w") as f1:
         subprocess.call([WORKDIR + "/" + 'getprojectconfiguration.sh', HOST, RUNDECK, URL, PROJECT],stdout=f1) 
    subprocess.call([WORKDIR + "/" + 'setprojectconfiguration.sh', HOST, RUNDECK, URL, PROJECT, PROJECTCONFIGUREFILE, 'd'])

#############################################################################################################
# enable sheduled customer jobs in project level
#############################################################################################################

def enable_scheduled_customer_jobs_in_project_level(customer):
    get_HOST_RUNDECK_PROJECT_URL(customer)
    PROJECTCONFIGUREFILE = TMP + '/' + 'projectconfiguration.' + DATETIME + '.properties'
    with open (PROJECTCONFIGUREFILE , "w") as f1:
         subprocess.call([WORKDIR + "/" + 'getprojectconfiguration.sh', HOST, RUNDECK, URL, PROJECT],stdout=f1) 
    subprocess.call([WORKDIR + "/" + 'setprojectconfiguration.sh', HOST, RUNDECK, URL, PROJECT, PROJECTCONFIGUREFILE,'e'])

def main():
   parser = argparse.ArgumentParser(description='Short sample app')
   parser.add_argument('-c', '--customer', type=str.lower, dest='customer', required=True, help='The Aktana Customer name with region')
   parser.add_argument('-s', '--select', type=str, dest='select', choices=['s', 'snapshot','u','unschedule','r','reschedule','D','disableschedule','E','enableschedule', 'k', 'kill', 'b','backup','B','Backup','a','assignacl','d','deprivecl','U','uat','P','prod','T','test','p','preprod'], required=True, help='Define account in which to create resources.')
   parser.add_argument('-d', '--database', type=str.lower, dest='database', help='Name of database novartisusprod_stage')
   parser.add_argument('-t', '--tables', type=str, nargs='+',dest='tables', help='Name of tables AKT_Survey AKT_SurveyQuestionEvent AKT_SurveyQuestionHold') 
   parser.add_argument('-D', '--description', type=str, nargs='+',dest='description', help='describe the reason why take this snapshot') 
   parser.add_argument('-g', '--group', type=str, dest='group', choices=['QA','CS','Dev'], help='group to assign/deprive ACL rights') 
   args = parser.parse_args()

   # Before deployment, if need to stop all jobs then disable all jobs in project level
   if args.select == 'disableschedule' or args.select == 'D':
      disable_scheduled_customer_jobs_in_project_level(args.customer)

   # After  deployment, enable job schedule in project level
   if args.select == 'enablechedule' or args.select == 'E':
      enable_scheduled_customer_jobs_in_project_level(args.customer)

   # Before deployment, find customer current running job ids in produdction and kill current running jobs by using job id
   if args.select == 'kill' or args.select == 'k':
      get_running_job_ids_and_kill(args.customer)

   # backup customer's regarding tables with data in porduction RDS database
   if args.select == 'backup' or args.select == 'b':
      rdstablebackup(args.customer)

   # backup customer's regarding tables with data in porduction RDS database
   if args.select == 'Backup' or args.select == 'B':
      rdstablebackup(args.customer,args.database,args.tables)
   
   # Before deployment take RDS snapshot
   if args.select == 'snapshot' or args.select == 's':
      rdstakesnapshot(args.customer,args.description)

   # Before deployment, find customer's current all production scheduled jobs, backup them first then unschedule them
   if args.select == 'unschedule' or args.select == 'u':
      get_scheduled_job_ids_and_unschedule_jobs(args.customer)

   # After deployment, get the uscheduled jobs list from backup then reschedule each jobs
   # according to backup list before the deployment.
   if args.select == 'reschedule' or args.select == 'r':
      get_scheduled_job_ids_and_reschedule_jobs(args.customer)

   # Before deployment assign QA group [run,kill] rights at production environment  
   if args.select == 'assignacl' or args.select == 'a':
      assign_deploy_aclpolicy(args.customer,args.group)

   # After deployemnt revert QA the rights to [run,kill] production jobs
   if args.select == 'depriveacl' or args.select == 'd':
      deprive_deploy_aclpolicy(args.customer,args.group)

   # After complete all tests download all jobs from pre environment, upload to next  environment
   # Most time pre enviroment is uat, move uat jobs to prod, preprod, test. 
   # when pre environment is dev, move all jobs to uat
   if args.select == 'preprod' or args.select == 'p':
      download_Rundeck_PreEnv_upload_to_NextEnv(args.customer, args.select)
   if args.select == 'prod' or args.select == 'P':
      download_Rundeck_PreEnv_upload_to_NextEnv(args.customer, args.select)
   if args.select == 'uat' or args.select == 'U':
      download_Rundeck_PreEnv_upload_to_NextEnv(args.customer, args.select)

if __name__ == "__main__":
   main()

