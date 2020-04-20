# Purpose: Automatically generate configuration templates to provision Cisco IOS devices for connectivity to an Ansible server
# Programmer: Kadar Anwar
# Language: Python 3.8
# provision.py
# 19 APR 2020
# v0.5

# TODO: prompt for interfaces & configure IP's based on a CSV and/or line-delimited list of IP's
# TODO: functions & classes
# TODO: implement writelines instead of several dozen .write statements. It's not scalable.

# Imports
import getpass
import os
from os import path
from time import sleep

# Variables
device_count = ''
device_type = ''
domain_name = ''
modulus = 0
username = ''
secret = ''
prefix = ''
hostname = ''

# Present a menu to the user
print("Cisco IOS Configuration Generator for Python 3.8")
print("---------------------------------------------")
device_count = int(input("Input the number of devices to configure: ")) # Prompt for # of devices
sleep(.5)
print("Select one of the following device types to configure: ")
print("1: Router")
print("2: Switch")
#print("3: Firewall")
#print("4: WLC")
#print("5: UCS")

# Input validation
device_type = None

while device_type != "1" and device_type != "2" and device_type != "3" and device_type != "4" and device_type != "5":
    device_type = input("Select a device type to configure: ")
    if device_type != "1" and device_type != "2" and device_type != "3" and device_type != "4" and device_type != "5":
        print("Please pick a valid device from the list")
    else:
        break

# Append a prefix based on device type; used for device configuration & filename scheme
device_type = int(device_type)

if device_type == 1:
    prefix = 'R-'
elif device_type == 2:
    prefix = 'SW-'
# elif device_type == 3:
#     prefix = 'FW-'
# elif device_type == 4:
#     prefix = 'WLC-'
# elif device_type == 5:
#     prefix = 'UCS-'
else:
    print("Invalid device type selected.")

domain_name = input("Enter the domain name: ")

while modulus < 30 or modulus > 4096:
    modulus = int(input("Enter the modulus key size to be used for generating RSA key [4096 recommended]. Not all devices support 4096 bit modulus: "))
    if modulus < 30 or modulus > 4096 or modulus == "":
        print("Please enter a valid modulus key size")
    else:
        modulus = modulus

#mgmt_IP = input("Enter the management IP of the Ansible server: ")

# Input validation on secret to ensure it is typed correctly
username = input("Enter the username to configure on each device: ")
secret = getpass.getpass(prompt="Enter the secret password. The password will not be echoed here: ")
secret2 = getpass.getpass(prompt="Enter password again, for verification: ")
if secret == secret2:
    print("Passwords were entered correctly. Please note the secret will be in plaintext in the initial text file, but the IOS device will encrypt it when the command is sent to the device.")
else:
    print("Please verify secret string was entered correctly. Please note the secret will be in plaintext in the initial text file, but the IOS device will encrypt it when the command is sent to the device.")
sleep(1)

# Generate a separate directory for configurations and move into to it
dir = os.getcwd()

# Skip creating if the directory already exists
if os.path.exists('./config') == True:
    cwd = os.chdir('./config')
else:
    os.makedirs('config')
    cwd = os.chdir('./config')

for device in range(1,device_count+1):
    hostname = prefix + str(device)
    output = open("%s.txt" % hostname, "wt")
    print("Writing configuration for device: " + " " + hostname)
    output.write("! Configuration for " + " " + hostname) # added ! so these lines are treated as comments and the file can be copy/pasted directly, for ease of use
    output.write("\n")
    output.write("! -----------------------")
    output.write("\n")
    output.write("en")
    output.write("\n")
    output.write("conf t")
    output.write("\n")
    output.write("hostname" + " " + hostname)
    output.write("\n")
    output.write("ip domain-name" + " " + domain_name)
    output.write("\n")
        # TODO: If the device is a legacy IOS device on 12.X code (such as a 3745) then there is
        # a seperate prompt for 'crypto key generate rsa', after which it prompts for a modulus up # to 2048
        # Fix: simply put the modulus on the next line after 'rsa'. This fixes it for 12.X code and # other devices I tested (IOU & IOSv)
    output.write("crypto key generate rsa")
    output.write("\n")
    output.write(str(modulus))
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
    sleep(.1) # artificial delay to help user keep up with script output
    device = device + 1
    output.close() # Close the file handler

cwd = os.getcwd()
sleep(.5)
print("Configuration files have been successfully written to: ",cwd)
