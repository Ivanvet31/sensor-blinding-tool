#! /usr/bin/env python
import socket
import sys
from threading import Thread

ip_addr = str(sys.argv[1])

conmap = [0 for _ in range(65536)]
threshhold = 10

sock_count = 0
sock_limit = 50000

socket.setdefaulttimeout(5)

def send(sock_fd, ip_addr, port, p_num, t):
    global sock_count
    if conmap[port] > threshhold: 
        sock_fd.close()
        sock_count -= 1
        return
    try:
        sock_fd.connect((ip_addr, port))
        print(p_num," ", 'tcp' if t == 1 else 'udp' if t == 2 else t, " ", port, " connected")
        sock_fd.send(packet)

        sock_fd.close()
        sock_count -= 1
    except ConnectionRefusedError:
        conmap[port] += 1
        print(p_num, " ", 'tcp' if t == 1 else 'udp' if t == 2 else t,  " ", port, " connection refused error")
        sock_fd.close()
        sock_count -= 1
    except TimeoutError:
        conmap[port] += 1
        print(p_num," ", 'tcp' if t == 1 else 'udp' if t == 2 else t,  " ", port, "connection timeouterror")
        sock_fd.close()
        sock_count -= 1

threads = []

packet_counter = 0

for i in range(0, int(sys.argv[3])):
    with open(sys.argv[2], "rb") as file_stream:
        t = int.from_bytes(file_stream.read(1))
        while t:
            port = int.from_bytes(file_stream.read(2))
            ln = int.from_bytes(file_stream.read(4))
            packet = file_stream.read(ln)

            sock_fd = socket.socket(socket.AF_INET, t)
            sock_count += 1
            while sock_count > sock_limit: pass

            thread = Thread(target = send, args = (sock_fd, ip_addr, port, packet_counter, t))
            thread.start()
            threads.append(thread)
            t = int.from_bytes(file_stream.read(1))
            packet_counter += 1


for thread in threads:
    thread.join()

