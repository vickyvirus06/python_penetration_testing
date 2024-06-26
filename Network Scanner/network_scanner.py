#!/usr/bin/env python

import scapy.all as scapy
from os import sys
import optparse


def get_argument():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Target IP / Target Range IP")
    (options, argument) = parser.parse_args()
    if not options.target_ip:
        print("[-] Enter Target IP or Range of IP  type help for more info")
        sys.exit(0)
    else:
        return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    client_list = []

    for answered in answered_list:
        answered_dict = {"ip": answered[1].psrc, "mac": answered[1].hwsrc}
        client_list.append(answered_dict)
    if not client_list:
        print("No Information stored")
        sys.exit(0)
    else:
        return client_list

def print_result(scan_result):
    print("\n-------------------------------------------------\n")
    print("   IP \t\t\tAt MAC Address")
    print("-------------------------------------------------\n")
    for client in scan_result:
        print(client["ip"] + "\t\t" + client["mac"])

options = get_argument()
scan_result = scan(options.target_ip)
print_result(scan_result)
print()






