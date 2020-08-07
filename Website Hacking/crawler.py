#! /usr/bin/env python

import requests

def scan_domain(url):
    try:
        return requests.get("http://"+url)
    except requests.ConnectionError:
        pass

def get_domain(target_url):
    with open("subdomains.txt","r") as subdomains_list:
        for subdomains in subdomains_list:
            url = subdomains.strip()+"."+ target_url
            response = scan_domain(url)
            if response:
                print("[+]Discovered subdomain : "+url)

def get_directory(target_url):
    total = 0
    with open("directory.txt","r") as directory_list:
        for directory in directory_list:
            url = target_url+"/"+directory.strip()
            response = scan_domain(url)
            if response:
                print("[+]Discovered URL --> "+url)
                total=total+1
    print("Total Directory Found " + str(total))

target_url = "google.com"
#get_domain(target_url)
get_directory(target_url)
