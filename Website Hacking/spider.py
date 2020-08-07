#! /usr/bin/env python

import requests
import re
import urllib.parse as urlparse

def scan(url):
    response = requests.get(url)
    return extract_target_links(response)


def extract_target_links(response):
    href_links = re.findall('(?:href=")(.*?")', str(response.content))
    return href_links

def extract_href_links(url):

    href_links = scan(url)
    for href_link in href_links:
        href_link = urlparse.urljoin(target_url, href_link)
        if "#" in href_link:
            href_link=href_link.split("#")[0]
        if target_url in href_link and href_link not in target_href_links and "cloud" not in href_link:
            target_href_links.append(href_link)
            print("[+]URL --->", href_link)
            extract_href_links(href_link)
    return target_href_links

target_href_links = []
target_url = "https://zsecurity.org"
target_href_links =extract_href_links(target_url)