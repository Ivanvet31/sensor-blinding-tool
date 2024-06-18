#! /usr/bin/python
import socket
import sys
from threading import Thread
import time

ip_addr = str(sys.argv[1])

file_stream = open(sys.argv[2], "rb")

conmap = [0 for _ in range(65536)]
threshhold = 2

def send(sock_fd, ip_addr, port, p_num, t):
    if conmap[port] > threshhold: return
    try:
        sock_fd.connect((ip_addr, port))
        print(p_num," ", 'tcp' if t == 1 else 'udp' if t == 2 else t, " ", port, " connected")
        sock_fd.send(packet)
    except ConnectionRefusedError:
        conmap[port] += 1
        print(p_num, " ", 'tcp' if t == 1 else 'udp' if t == 2 else t,  " ", port, " connection refused error")
    except TimeoutError:
        conmap[port] += 1
        print(p_num," ", 'tcp' if t == 1 else 'udp' if t == 2 else t,  " ", port, "connection timeouterror")

threads = []
for i in range(0, int(sys.argv[3])):
    #print('==================<<package number ', i, '>>=============')
    
    t = int.from_bytes(file_stream.read(1))
    
    port = int.from_bytes(file_stream.read(2))
    ln = int.from_bytes(file_stream.read(4))
    packet = file_stream.read(ln)

    if i >= int(sys.argv[4]) & i <= int(sys.argv[5]):
        #print('tcp' if t == 1 else 'udp' if t == 2 else t)
        #print(port)
        #print(ln)
        #print(packet)
        
        sock_fd = socket.socket(socket.AF_INET, t)
        thread = Thread(target = send, args = (sock_fd, ip_addr, port, i, t))
        thread.start()
        threads.append(thread)
    else:
        continue

for thread in threads:
    thread.join()

file_stream.close()

