#!/usr/bin/env python3
import mysql.connector 
from mysql.connector import Error
import argparse
import boto3
from botocore.exceptions import NoCredentialsError
import time
import datetime

DATETIME = time.strftime('%Y%m%d-%H%M%S')
BACKUP_PATH = '/root/dbbackup'
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

def upload_to_aws(local_file, bucket, s3_file):
   s3 = boto3.client('s3')
   try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
   except FileNotFoundError:
        print("The file was not found")
        return False
   except NoCredentialsError:
        print("Credentials not available")
        return False

def take_tables_backup(customer):

   try:
        connection = mysql.connector.connect(
                    host = customer + "rds.xxxxx.com",
                    user = "automation",
                    passwd = "",
                    database = customer + "dev"
                    )
        if connection.is_connected():
           db_Info = connection.get_server_info()
           print("Connected to MySQL Server version ", db_Info)
           mycursor = connection.cursor()
           mycursor.execute("select database();")
           record = mycursor.fetchone()
           print("You're connected to database: ", record)
           Accountbackup = "Account." + DATETIME
           command = "CREATE TABLE `" + Accountbackup + "` AS SELECT * FROM " +  "`Account`;"
           print (command)
           mycursor.execute(command)
           AccountProductbackup = "AccountProduct." + DATETIME
           command = "CREATE TABLE `" + AccountProductbackup + "` AS SELECT * FROM " +  "`AccountProduct`;"
           print (command)
           mycursor.execute(command)
           AccountProductLabelValuebackup = "AccountProductLabelValue." + DATETIME
           command = "CREATE TABLE `" + AccountProductLabelValuebackup + "` AS SELECT * FROM " +  "`AccountProductLabelValue`;"
           print (command)
           mycursor.execute(command)
           AktanaUserbackup = "AktanaUser." + DATETIME
           command = "CREATE TABLE `" + AktanaUserbackup + "` AS SELECT * FROM " +  "`AktanaUser`;"
           print (command)
           mycursor.execute(command)
           DATABASECHANGELOGbackup = "DATABASECHANGELOG." + DATETIME
           command = "CREATE TABLE `" + DATABASECHANGELOGbackup + "` AS SELECT * FROM " +  "`DATABASECHANGELOG`;"
           print (command)
           mycursor.execute(command)
           DSEConfigbackup = "DSEConfig." + DATETIME
           command = "CREATE TABLE `" + DSEConfigbackup + "` AS SELECT * FROM " +  "`DSEConfig`;"
           print (command)
           mycursor.execute(command)
           DSEConfigRunGroupbackup = "DSEConfigRunGroup." + DATETIME
           command = "CREATE TABLE `" + DSEConfigRunGroupbackup + "` AS SELECT * FROM " +  "`DSEConfigRunGroup`;"
           print (command)
           mycursor.execute(command)
           DSEConfigRunGroupRepbackup = "DSEConfigRunGroupRep." + DATETIME
           command = "CREATE TABLE `" + DSEConfigRunGroupRepbackup + "` AS SELECT * FROM " +  "`DSEConfigRunGroupRep`;"
           print (command)
           mycursor.execute(command)
           Facilitybackup = "Facility." + DATETIME
           command = "CREATE TABLE `" + Facilitybackup + "` AS SELECT * FROM " +  "`Facility`;"
           print (command)
           mycursor.execute(command)
           DSESuggestionLifecyclebackup = "DSESuggestionLifecycle." + DATETIME
           command = "CREATE TABLE `" + DSESuggestionLifecyclebackup + "` AS SELECT * FROM " +  "`DSESuggestionLifecycle`;"
           print (command)
           mycursor.execute(command)
           Eventbackup = "Event." + DATETIME 
           command = "CREATE TABLE `" + Eventbackup + "` AS SELECT * FROM " +  "`Event`;"
           print (command)
           mycursor.execute(command)
           Interactionbackup = "Interaction." + DATETIME
           command = "CREATE TABLE `" + Interactionbackup + "` AS SELECT * FROM " +  "`Interaction`;"
           print (command)
           mycursor.execute(command)
           InteractionAccountbackup = "InteractionAccount." + DATETIME
           command = "CREATE TABLE `" + InteractionAccountbackup + "` AS SELECT * FROM " +  "`InteractionAccount`;"
           print (command)
           mycursor.execute(command)
           InteractionProductbackup = "InteractionProduct." + DATETIME
           command = "CREATE TABLE `" + InteractionProductbackup + "` AS SELECT * FROM " +  "`InteractionProduct`;"
           print (command)
           mycursor.execute(command)
           LabelTypebackup = "LabelType." + DATETIME
           command = "CREATE TABLE `" + LabelTypebackup + "` AS SELECT * FROM " +  "`LabelType`;"
           print (command)
           mycursor.execute(command)
           parameterControlsbackup = "parameterControls." + DATETIME
           command = "CREATE TABLE `" + parameterControlsbackup + "` AS SELECT * FROM " +  "`parameterControls`;"
           print (command)
           mycursor.execute(command)
           Productbackup = "Product." + DATETIME
           command = "CREATE TABLE `" + Productbackup + "` AS SELECT * FROM " +  "`Product`;"
           print (command)
           mycursor.execute(command)
           Repbackup = "Rep." + DATETIME
           command = "CREATE TABLE `" + Repbackup + "` AS SELECT * FROM " +  "`Rep`;"
           print (command)
           mycursor.execute(command)
           RepAccountAssignmentbackup = "RepAccountAssignment." + DATETIME
           command = "CREATE TABLE `" + RepAccountAssignmentbackup + "` AS SELECT * FROM " +  "`RepAccountAssignment`;"
           print (command)
           mycursor.execute(command)
           RepAccountHoldbackup = "RepAccountHold." + DATETIME
           command = "CREATE TABLE `" + RepAccountHoldbackup + "` AS SELECT * FROM " +  "`RepAccountHold`;"
           print (command)
           mycursor.execute(command)
           RepDateLocationbackup = "RepDateLocation." + DATETIME
           command = "CREATE TABLE `" + RepDateLocationbackup + "` AS SELECT * FROM " +  "`RepDateLocation`;"
           print (command)
           mycursor.execute(command)
           RepProductAuthorizationbackup = "RepProductAuthorization." + DATETIME
           command = "CREATE TABLE `" + RepProductAuthorizationbackup + "` AS SELECT * FROM " +  "`RepProductAuthorization`;"
           print (command)
           mycursor.execute(command)
           RepTeamRepbackup = "RepTeamRep." + DATETIME
           command = "CREATE TABLE `" + RepTeamRepbackup + "` AS SELECT * FROM " +  "`RepTeamRep`;"
           print (command)
           mycursor.execute(command)
           StrategyTargetbackup = "StrategyTarget." + DATETIME
           command = "CREATE TABLE `" + StrategyTargetbackup + "` AS SELECT * FROM " +  "`StrategyTarget`;"
           print (command)
           mycursor.execute(command)
           sysParametersbackup = "sysParameters." + DATETIME
           command = "CREATE TABLE `" + sysParametersbackup + "` AS SELECT * FROM " +  "`sysParameters`;"
           print (command)
           mycursor.execute(command)

           mycursor.execute("select * from Account  order by accountId")
           myresult = mycursor.fetchall()
        
           account = []
           account = [list(i) for i in myresult]
           backupfile = customer + '.txt.' + DATETIME
           with open(backupfile, "a") as f:
       	      for customername in account:
                 f.write (str(customername))
                 f.write ('\n')

        #  uploaded = upload_to_aws(backupfile, 'xxxxxx-db-backup-us', customer + '/{}'.format(backupfile))
        #   if uploaded:
        #     print ("uploaded successfully")
   except Error as e:
           print("Error while connecting to MySQL", e)
   finally:
        if (connection.is_connected()):
             mycursor.close()
             connection.close()
             print("MySQL connection is closed")

def take_db_snapshot(customer):
    rds = boto3.client('rds')
    try:
# get all of the db instances
       dbs = rds.describe_db_instances()
       for db in dbs['DBInstances']:
           print ("%s@%s:%s %s") % (
             db['MasterUsername'],
             db['Endpoint']['Address'],
             db['Endpoint']['Port'],
             db['DBInstanceStatus'])
    except Exception as error:
       print (error)
def main():
   parser = argparse.ArgumentParser(description='Short sample app')
   parser.add_argument('-c', '--customer', type=str.lower, dest='customer',  required=True, help='Define region in which to create resources.')
   parser.add_argument('-s', '--select', type=str, dest='select', choices=['s','snapshot', 'b','dbbackup', 't','tablebackup'], required=True, help='Define account in which to create resources.')
   args = parser.parse_args()
   if args.select == 'snapshot'or args.select == 's':
      take_db_snapshot(args.customer)
   if args.select == 'dbbackup' or args.select == 'd':
      take_db_backup(args.customer, args.select)
   if args.select == 'tablesbackup' or args.select == 't':
      take_tables_backup(args.customer)
if __name__ == "__main__":
   main()


