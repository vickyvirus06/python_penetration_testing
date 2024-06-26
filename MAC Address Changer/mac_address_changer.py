#! /usr/bin/env python

import subprocess
import optparse
import re
from os import sys

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help=" Enter Interface ")
    parser.add_option("-m","--mac",dest="new_mac_address",help=" Enter MAC Address to change ")
    (options,arguments)=parser.parse_args()
    if not options.interface:
        print("[-] Specify a Interface use --help for more Info")
        sys.exit(0)
    elif not options.new_mac_address:
        print("[-] Specify a MAC Address  --help for more Info")
        sys.exit(0)
    return options

def mac_changer(interface,new_mac_address,current_mac_address):
    print("\n[+] Changing MAC Address of " + interface + " : " + current_mac_address +"\n")
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac_address])
    subprocess.call(["ifconfig",interface,"up"])

def get_current_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    return mac_address_result.group(0)

options=get_arguments()
current_mac_address= get_current_mac_address(options.interface)
mac_changer(options.interface,options.new_mac_address,str(current_mac_address))
current_mac_address = get_current_mac_address(options.interface)

if current_mac_address == options.new_mac_address:
    print("[+] MAC Address Successfully changed to " + str(current_mac_address))
else :
    print("[-] MAC Address Failed to change " )
