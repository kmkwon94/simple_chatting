import socket
import select
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to server
s.connect(('127.0.0.1', 8000))

name = None

while True:
    # wating user's input
    read, write, fail = select.select((s, sys.stdin), (), ())
    # if message is arrived
    for desc in read:
        if desc == s:  # if messages from server
            # read 4096 bytes from socket
            data = s.recv(4096)
            print(data.decode())  # print bytes to string

            if name is None:  # if user connect first time, Save given name and notice other people that I'm appeared.
                name = data.decode()
                s.send(f'{name} is connected'.encode())
        else:  # if messages from user, read user's input string and transport server
            msg = desc.readline()
            msg = msg.replace('\n', '')
            s.send(f'{name} : {msg}'.encode())
