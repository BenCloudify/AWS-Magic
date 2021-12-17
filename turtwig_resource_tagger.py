# Imported python modules.
import boto3
import csv
import time

print("\n########################################################################")
print("##########               Turtwig Resource Tagger             ###########")
print("##########                  by Jeremiah Henry                ###########")
print("##########                GitHub @ jerrykingbob              ###########")
print("########################################################################")

# <SCRIPT START>
start_time = time.time()

# Global variables and lists.
column_counter = 0
csv_headers = []

# Load profiles from ~/.aws/config file
for profile in boto3.session.Session().available_profiles:
    current_session = boto3.session.Session(profile_name = profile)

# Create dict objects of resources to tag.
ec2 = current_session.client("ec2")
rds = current_session.client("rds")

# Get the headers in the csv file
with open('Book1.csv', 'r', encoding='utf-8-sig') as read_file:
  csv_reader = csv.reader(read_file, delimiter=',')
  header_object = next(csv_reader)
  column_counter = len(header_object)

  for x in header_object:
    csv_headers.append(x)

  for record in csv_reader:
    tagcount = 2

    for header in csv_headers:
      if(record[0].lower() == "ec2 instance"):
        ec2.create_tags(Resources = [record[1]], Tags=[{'Key':csv_headers[tagcount], 'Value':record[tagcount]}])
        tagcount += 1
        print(tagcount)

        if tagcount == len(csv_headers):
          break

      elif(record[0].lower() == "ebs volume"):
        ec2.create_tags(Resources = [record[1]], Tags=[{'Key':csv_headers[tagcount], 'Value':record[tagcount]}])
        tagcount += 1
        print(tagcount)

        if tagcount == len(csv_headers):
          break

# <SCRIPT END>
print("Successfully tagged all listed resources in", format(time.time()-start_time, ".2f"), "seconds\n")


