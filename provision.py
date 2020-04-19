# Purpose: Automatically generate configuration templates to provision Cisco IOS devices for connectivity to an Ansible server
# Programmer: Kadar Anwar
# Language: Python 3.8
# provision.py
# 19 APR 2020
# v0.1

# TODO: prompt for interfaces & configure IP's based on a CSV and/or line-delimited list of IP's

# Imports
import getpass
import os

# Variables
device_count = ''
device_type = ''
domain_name = ''
modulus = 0
username = ''
secret = ''
suffix = ''
hostname = ''

# Gather inputs
device_count = input("Input the number of devices to configure: ") # Prompt for # of devices
device_count = int(device_count)

print("\n")

# Present a menu to the user
print("Cisco IOS Configuration Generator for Python 3.8")
print("---------------------------------------------")
print("Select one of the following device types to configure: ")
print("1: Router")
print("2: Switch")
print("3: Firewall")
print("4: WLC")
print("5: UCS")

# Input validation
device_type = None

while device_type != "1" and device_type != "2" and device_type != "3" and device_type != "4" and device_type != "5":
    device_type = input("Select a device type to configure: ")
    if device_type != "1" and device_type != "2" and device_type != "3" and device_type != "4" and device_type != "5":
        print("Please pick a valid device from the list")
    else:
        break

device_type = int(device_type)

if device_type == 1:
    suffix = 'R-'
elif device_type == 2:
    suffix = 'SW-'
elif device_type == 3:
    suffix = 'FW-'
elif device_type == 4:
    suffix = 'WLC-'
elif device_type == 5:
    suffix = 'UCS-'
else:
    print("Invalid device type selected.")

domain_name = input("Enter the domain name: ")

while modulus < 30 or modulus > 4096:
    modulus = int(input("Enter the modulus key size to be used for generating RSA key [4096 recommended]: "))
    if modulus < 30 or modulus > 4096 or modulus == "":
        print("Please enter a valid modulus key size")
    else:
        modulus = modulus

#mgmt_IP = input("Enter the management IP of the Ansible server: ")
username = input("Enter the username to configure on each device: ")
secret = getpass.getpass(prompt="Enter the secret password. The password will not be echoed here: ")
secret2 = getpass.getpass(prompt="Enter password again, for verification: ")
if secret == secret2:
    print("Passwords were entered correctly.")
else:
    print("Please verify secret string was entered correctly.")

output = open('configuration.txt','w')

for i in range(1,device_count+1):
    hostname = suffix + str(i)
    print("Writing configuration for device: " + " " + hostname)
    output.write("\n")
    output.write("Configuration for " + " " + hostname)
    output.write("\n")
    output.write("-----------------------")
    output.write("\n")
    output.write("en")
    output.write("\n")
    output.write("conf t")
    output.write("\n")
    output.write("hostname" + " " + hostname)
    output.write("\n")
    output.write("ip domain-name" + " " + domain_name)
    output.write("\n")
    output.write("crypto key generate rsa modulus" + " " + str(modulus))
    output.write("\n")
    output.write("line vty 0 4")
    output.write("\n")
    output.write("transport input ssh")
    output.write("\n")
    output.write("exit")
    output.write("\n")
    output.write("username" + " " + username + " " + "secret" + " " + secret)
    output.write("\n")
    output.write("ip ssh version 2")
    output.write("\n")
    output.write("no ip domain-lookup")
    output.write("\n")
    output.write("cdp run")
    output.write("\n")
    output.write("end")
    output.write("\n")
    output.write("term len 0")
    output.write("\n")
    output.write("wr")
    output.write("\n")
    output.write("\n")
    output.write("\n")
    i = i + 1

output.close() # Close the file handler
print("Device configuration has been successfully saved in filename \'configuration.txt\'")