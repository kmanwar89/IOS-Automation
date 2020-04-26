# Purpose: Automatically generate configuration templates to provision Cisco IOS devices for connectivity to an Ansible server
# Programmer: Kadar Anwar
# Language: Python 3.8
# provision.py
# 19 APR 2020
# v1.0

# TODO: prompt for interfaces & configure IP's based on a CSV and/or line-delimited list of IP's
# TODO: add support for configurations for Firewall, WLC and UCS devices

# Imports
import getpass
import os
from os import path
from time import sleep

# Variables
device_count= ''
device_type = ''
domain_name = ''
modulus = 0
username = ''
secret = ''
hostname = ''

def main():
    # Present a menu
    user_menu()

    # Check for different device types and assign a prefix
    device_type, prefix = device_check()

    # Get device count from above menu
    device_count = int(input("Input the number of devices to configure: ")) # Prompt for # of devices

    # Gather relevant inputs for use in other functions
    get_inputs()

    # Gather modulus for RSA key generation and ensure it is a valid value
    modulus_check()

    #mgmt_IP = input("Enter the management IP of the Ansible server: ")

    # Gather username & secret info, including data validation
    get_user_info()

    #print("Prefix - main()", prefix)

    # Write output to a per-device configuration
    write_output(device_count, prefix, username, secret, domain_name)

    cwd = os.getcwd()
    sleep(.5)
    print("Configuration files have been successfully written to: ",cwd)

def user_menu():
    # Present a menu to the user
    print("Cisco IOS Configuration Generator for Python 3.8")
    print("---------------------------------------------")
    sleep(.5)
    print("Select one of the following device types to configure: ")
    print("1: Router")
    print("2: Switch")
    # Placeholders for future functionality
    #print("3: Firewall")
    #print("4: WLC")
    #print("5: UCS")

def device_check():
    # Input validation
    device_type = None
    prefix = None

    while device_type != "1" and device_type != "2" and device_type != "3" and device_type != "4" and device_type != "5":
        device_type = input("Select a device type to configure: ")
        if device_type != "1" and device_type != "2" and device_type != "3" and device_type != "4" and device_type != "5":
            print("Please pick a valid device from the list")
        else:
            break

    # Append a prefix based on device type; used for device configuration & filename scheme
    device_type = int(device_type)

    # TODO: Implement this using a dictionary and .get() instead of if/elif
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

    # print("Prefix - device_check()", prefix)

    return device_type, prefix

def get_inputs():
    
    domain_name = input("Enter the domain name: ")

    # return device_count
    return domain_name

def modulus_check():
    modulus = 0
    while modulus < 30 or modulus > 4096:
        modulus = int(input("Enter the modulus key size to be used for generating RSA key [4096 recommended]. Not all devices support 4096 bit modulus: "))
        if modulus < 30 or modulus > 4096 or modulus == "":
            print("Please enter a valid modulus key size")
        else:
            modulus = modulus
    return int(modulus)

def get_user_info():
    # Input validation on secret to ensure it is typed correctly
    username = input("Enter the username to configure on each device: ")
    secret = getpass.getpass(prompt="Enter the secret password. The password will not be echoed here: ")
    secret2 = getpass.getpass(prompt="Enter password again, for verification: ")
    if secret == secret2:
        print("Passwords were entered correctly. Please note the secret will be in plaintext in the initial text file, but the IOS device will encrypt it when the command is sent to the device.")
    else:
        print("Please verify secret string was entered correctly. Please note the secret will be in plaintext in the initial text file, but the IOS device will encrypt it when the command is sent to the device.")
    sleep(1)

    return username,secret
    
# Expanded this function to include more arguments - fixing a bug where output wasn't correctly printing secret, username & domain_name
def write_output(device_count, prefix, username, secret, domain_name):
    #print("Prefix - write_output() ", prefix)
    # Generate a separate directory for configurations and move into to it
    os.getcwd()

    # Skip creating if the directory already exists
    if os.path.exists('./config') == True:
        os.chdir('./config')
    else:
        os.makedirs('config')
        os.chdir('./config')

    for device in range(1,device_count+1):
        hostname = prefix + str(device)
        output = open("%s.txt" % hostname, "wt")
        print("Writing configuration for device: " + " " + hostname)
        
        # # For large amounts of devices, introduce a reduced delay. For a smaller amount of devices, # briefly print the status

        # if device_count <30:
        #     sleep(.075)
        # else:
        #     sleep(.01)

        output_text =   ["!Configuration for " + " " + hostname,
                        "\n!-----------------------",
                        "\nen",
                        "\nconf t",
                        "\nhostname" + " " + hostname,
                        "\nip domain-name" + " " + domain_name,
                        "\ncrypto key generate rsa\n",
                        str(modulus),
                        "\nline vty 0 4",
                        "\ntransport input ssh",
                        "\nexit",
                        "\nusername" + " " + username + " " + "secret" + " " + secret,
                        "\nip ssh version 2",
                        "\nno ip domain-lookup",
                        "\ncdp run",
                        "\nend",
                        "\nterm len 0",
                        "\nwr"
                        ]

        output.writelines(output_text)

        # Artificial delay to help user keep up with script output. For large amount of devices, 
        # introduce a brief delay.
        if device_count <30:
            sleep(.075)
        else:
            sleep(.01)
        
        device = device + 1
        output.close() # Close the file handler

main()