# Imported modules.
import boto3
import csv
import time
import datetime

# Script Start.
start_time = time.time()  

#ASCII Art
print("\n########################################################################")
print("##########   Magikarp Automated IAM Roles Report Generator   ###########")
print("##########                  by Jeremiah Henry                ###########")
print("##########                GitHub @ jerrykingbob              ###########")
print("########################################################################")

try:
  with open(r"C:\Users\jerry\Documents\PythonVS\AWS Automated IAM Reports\koi.txt", 'r') as picture:
    for line in picture:
      print(line)

  print("\n########################################################################")
  print("\nQuerying AWS Roles across all AWS accounts.")
  print("This might take a while...\n")
except:
  print("########################################################################")
  print("##########   Magikarp Automated IAM Roles Report Generator   ###########")
  print("##########                  by Jeremiah Henry                ###########")
  print("##########                GitHub @ jerrykingbob              ###########")
  print("########################################################################")

  print("\nQuerying AWS Roles across all AWS accounts.")
  print("This might take a while...\n")



# Global variables and lists.
profiles = [] # List of profiles.
roles_list = [] # List of roles.
appended_roles_list = [] # Temporary list to load quried data for roles to be stored in csv.
total_role_counter = 0
role_counter = 0 # Number of roles queried.
role_180_active = 0 # Counter for roles used within 180 days
role_180_inactive = 0 # Counter for roles used within 180 days

# Load profiles from ~/.aws/config file
for profile in boto3.session.Session().available_profiles:
    profiles.append(profile)

# Establish a new boto3 session for each AWS account to query data for each role. 
for profile in profiles:
  current_session = boto3.session.Session(profile_name = profile)
  
  if profile == "default":
    profile = "default"
  print("[", profile, "]", end =  '\r')

  iam = current_session.resource("iam")

  for roles in iam.roles.all():
    roles_list.append(roles.name)

  for roles in roles_list:
    role = iam.Role(roles)
    flag_180days_active = "No"

    if "LastUsedDate" in role.role_last_used:

      # Calculates the time between the current datetime and the LastUsedDate datetime.
      time_difference = datetime.datetime.now(datetime.timezone.utc) - role.role_last_used["LastUsedDate"]

      # Returns datetime, 180 days before the current datetime.
      check_180days_before = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days = 180)



      print("[", profile, "]", "Total roles queried:", role_counter+1, "|", role.name, end= '\r', flush = True)
          
      if role.role_last_used["LastUsedDate"] > check_180days_before:
        flag_180days_active = "Yes"
        role_180_active += 1
      else:
        flag_180days_active = "No"
        role_180_inactive +=1

      appended_roles_list.append({"Account": profile, "Role Name": role.name, "ARN": role.arn, "Role ID": role.role_id, \
        "Description": role.description, "JSON Policy Doc": role.assume_role_policy_document, "Max Session Duration": role.max_session_duration, \
          "Creation Date": role.create_date, "Last Used": role.role_last_used["LastUsedDate"], "Time Since Last Use": time_difference, "Used in Last 180 Days?": flag_180days_active})
    else:

      print("[", profile, "]", "Total roles queried:", role_counter+1, "|", role.name, end= '\r', flush = True)
      role_180_inactive += 1

      appended_roles_list.append({"Account": profile, "Role Name": role.name, "ARN": role.arn, "Role ID": role.role_id, \
        "Description": role.description, "JSON Policy Doc": role.assume_role_policy_document, "Max Session Duration": role.max_session_duration, \
          "Creation Date": role.create_date, "Last Used": "Never Used", "Time Since Last Use": "Null", "Used in Last 180 Days?": "No" })
      
    role_counter += 1
    roles_list = []


    # Export CSV report.
    with open("IAM Roles Report.csv" , 'w', newline='') as write_file:
        fieldnames = ["Account", "Role Name", "ARN", "Role ID", "Description", "JSON Policy Doc", "Max Session Duration", "Creation Date", "Last Used", "Time Since Last Use", "Used in Last 180 Days?"] 
        csv_writer = csv.DictWriter(write_file, fieldnames = fieldnames)
        csv_writer.writeheader()

        for line in appended_roles_list:
          csv_writer.writerow(line)
    
  print("[", profile, "]", "Completed >", role_counter, "Roles", "> Roles used within 180 days:", role_180_active, "> Roles not used within 180 days:", role_180_inactive, "\t\t")
  role_counter = 0
  role_180_active = 0
  role_180_inactive = 0

# Script end.
print()
print(total_role_counter,"roles queried", format(time.time()-start_time, ".2f"), "seconds\n")
print("IAM report SUCCESSFULLY generated!\n")