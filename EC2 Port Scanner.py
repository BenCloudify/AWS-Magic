import csv
import socket
import time

start_time = time.time()

#list to document in new csv file
filtered_list=[]
#MS SQL Server, MySQL, PostgreSQL, Oracle db
port_list=[22, 3306, 5432, 1521]


print("##########################################################################################")
print("##########            COI TEAM'S AWS EC2 DB Port Checker          ########################")
print("###########                    by Jeremiah Henry                 #########################")
print("##########################################################################################")
print("")

#function to read the csv file containing the ip addresses of all ec2 instances in the configured AWS account
with open('Book1.csv', 'r', encoding='utf-8-sig') as read_file:
  csv_reader = csv.DictReader(read_file, delimiter=',')

  for record in csv_reader:
    counter=0
    ip_address = record['IP Addresses']

    for port in port_list:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(3.0)
      port_result = sock.connect_ex((ip_address,port))

      if port_result == 0:
        
        port_check="running"
        
        if counter == 0:
          port_1_check = port_check
        elif counter == 1:
          port_2_check = port_check
        elif counter == 2:
          port_3_check = port_check
        elif counter == 3:
          port_4_check = port_check

        print(ip_address,"", "port", port, port_check)

      elif port_result == 10035:
        
        port_check="Timeout (check firewall config)"

        if counter == 0:
          port_1_check = port_check
        elif counter == 1:
          port_2_check = port_check
        elif counter == 2:
          port_3_check = port_check
        elif counter == 3:
          port_4_check = port_check

        print(ip_address,"", "port", port, port_check)

      else:
        
        port_check="not running"

        if counter == 0:
          port_1_check = port_check
        elif counter == 1:
          port_2_check = port_check
        elif counter == 2:
          port_3_check = port_check
        elif counter == 3:
          port_4_check = port_check
        
        print(ip_address,"", "port", port, port_check)

      counter += 1
      sock.close()

    print("_________________________________________________________________________________________\n")
    filtered_list.append({'Instance Name': record['Instance Name'], 'Instance ID': record['Instance ID'],'IP Addresses': record['IP Addresses'], 'MS SQL Port 1433': port_1_check, 'MySQL Port 3306': port_2_check, 'PostgreSQL Port 5432': port_3_check, 'OracleDB Port 1521': port_4_check})

  #function to generate a csv file listing ec2 instances with and without an SQL server running on them
    with open('Book2.csv', 'w', newline='') as write_file:
      fieldnames = ['Instance Name', 'Instance ID', 'IP Addresses', 'MS SQL Port 1433', 'MySQL Port 3306', 'PostgreSQL Port 5432', 'OracleDB Port 1521']
      csv_writer = csv.DictWriter(write_file, fieldnames=fieldnames)
      csv_writer.writeheader()

      for line in filtered_list:
        csv_writer.writerow(line)

print("Port scan completed in", format(time.time()-start_time, ".2f"), "seconds\n")