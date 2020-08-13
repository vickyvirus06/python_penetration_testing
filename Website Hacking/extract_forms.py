#! /usr/bin/env python

import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse

def scan(url):
    try:
        return requests.get(url)
    except requests.ConnectionError:
        pass

target_url="http://127.0.0.1/mutillidae/index.php?page=dns-lookup.php"
response = scan(target_url)
parsed_html = BeautifulSoup(response.content,features="html.parser")
forms_list = parsed_html.find_all("form")

for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url,action)
    method = form.get("method")
    print("[+]Action --> " +action)
    print("[+]Method --> " + method)
    input_list = form.find_all("input")
    post_data = {}

    for input in input_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")

        if input_type == "text":
            input_value = "test"


        post_data[input_name]=input_value
    response = requests.post(post_url,data=post_data)
    print(str(response.content.decode()))