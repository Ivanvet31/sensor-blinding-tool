#! /usr/bin/env python

import sys
import random
import re
import string
from xeger import Xeger

def generate(len: int) -> str:
    res = ""
    for _ in range(len):
        res += random.choice(string.ascii_letters)
    return res

# TODO: wrtie http packet generation
def generate_http(rules):
    http_method = ""
    http_uri = ""
    http_header = ""
    http_client_body = ""
    http_cookie = ""
    for rule in rules:
        if rule.get("http_uri", 0):
            if rule.get("pcre"):
                pass
        elif rule.get("http_header", 0):
            pass
        elif rule.get("http_method", 0):
            pass
        elif rule.get("http_client_body", 0):
            pass
        elif rule.get("http_cookie", 0):
            pass

packet_counter = 0
packet_dir = "../packets/"
packets = "packets_1.bin"
output = open(packet_dir + packets, "wb")

def write_packet(protocol : int, port : int, packet : bytes):
    global packets, output, packet_counter
    file_num = int(packets[8:-4])
    if packet_counter > (file_num * 1000):
        packets = f"packets_{file_num + 1}.bin"
        output.close()
        output = open(packet_dir + packets, "wb")
        write_packet(protocol, port, packet)
        return

    if not output:
        return

    data = int.to_bytes(protocol) + int.to_bytes(port % 65536, 2) + int.to_bytes(len(packet), 4) + packet

    output.write(data)
        
if __name__ == "__main__":
    file_name = sys.argv[1]
    with open(file_name, "r") as rules:
        for line in rules.readlines():
            if len(line) < 2: continue
            splat = line.split()
            protocol = splat[1]

            if splat[0] != "alert": 
                continue

            if splat[2] != "$EXTERNAL_NET":
                continue

            is_http = "HTTP" in line
            
            ports = ""
            match splat[6]:
                case "$HTTP_PORTS":
                    ports = "[36,80,81,82,83,84,85,86,87,88,89,90,311,323,383,443,444,555,591,593,623,631,664,801,808,818,901,972,1158,1220,1270,1414,1533,1581,1719,1720,1741,1801,1812,1830,1942,2231,2301,2375,2381,2578,2809,2869,2980,3000,3029,3037,3057,3128,3323,3443,3702,4000,4343,4444,4592,4848,5000,5054,5060,5061,5117,5222,5250,5416,5443,5450,5480,5555,5600,5814,5894,5984,5985,5986,6060,6080,6173,6988,7000,7001,7005,7070,7071,7080,7144,7145,7180,7181,7510,7770,7777,7778,7779,8000,8001,8008,8014,8015,8020,8028,8040,8080,8081,8082,8085,8088,8090,8095,8118,8123,8161,8180,8181,8182,8222,8243,8280,8300,8333,8344,8393,8400,8443,8484,8500,8509,8511,8694,8787,8800,8848,8852,8880,8888,8899,8983,9000,9001,9002,9050,9060,9080,9090,9091,9111,9200,9201,9290,9443,9447,9502,9700,9710,9788,9830,9850,9990,9999,10000,10080,10100,10250,10255,10297,10443,11371,12601,13014,14592,15489,16000,16992,16993,16994,16995,17000,18081,19980,20000,29991,30007,30018,30888,33300,34412,34443,34444,36099,37215,40007,41080,44449,49152,49153,50000,50002,50452,51423,53331,54444,55252,55555,56712]"
                case "$SSH_PORTS":
                    ports = "22"
                case "$ORACLE_PORTS":
                    ports = "1024"
                case "$FILE_DATA_PORTS":
                    ports = "36"
                    ports = "[36,80,81,82,83,84,85,86,87,88,89,90,311,323,383,443,444,555,591,593,623,631,664,801,808,818,901,972,1158,1220,1270,1414,1533,1581,1719,1720,1741,1801,1812,1830,1942,2231,2301,2375,2381,2578,2809,2869,2980,3000,3029,3037,3057,3128,3323,3443,3702,4000,4343,4444,4592,4848,5000,5054,5060,5061,5117,5222,5250,5416,5443,5450,5480,5555,5600,5814,5894,5984,5985,5986,6060,6080,6173,6988,7000,7001,7005,7070,7071,7080,7144,7145,7180,7181,7510,7770,7777,7778,7779,8000,8001,8008,8014,8015,8020,8028,8040,8080,8081,8082,8085,8088,8090,8095,8118,8123,8161,8180,8181,8182,8222,8243,8280,8300,8333,8344,8393,8400,8443,8484,8500,8509,8511,8694,8787,8800,8848,8852,8880,8888,8899,8983,9000,9001,9002,9050,9060,9080,9090,9091,9111,9200,9201,9290,9443,9447,9502,9700,9710,9788,9830,9850,9990,9999,10000,10080,10100,10250,10255,10297,10443,11371,12601,13014,14592,15489,16000,16992,16993,16994,16995,17000,18081,19980,20000,29991,30007,30018,30888,33300,34412,34443,34444,36099,37215,40007,41080,44449,49152,49153,50000,50002,50452,51423,53331,54444,55252,55555,56712,110,143]"
                case "$SIP_PORTS":
                    ports = "[5060,5061,5600]"
                case _:
                    ports = splat[6]

            opt_list = []
            option_string = line[line.find("(") + 1:line.rfind(")") - 1]

            option_list = re.split("content:", option_string)[1:]

            for opt_line in option_list:
                options_pcre = opt_line.split("pcre:")


                option_pairs = list(map(lambda x: x.split(":"), options_pcre[0].split("; ")))

                options = {}
                if option_pairs[0][0] == '!':
                    options['content'] = option_pairs[0][0][2:-1]
                    options['not'] = 1
                else:
                    options['content'] = option_pairs[0][0][1:-1]
                    options['not'] = 0
                options["pcre"] = 0

                for option in option_pairs[1::]:
                    if len(option) == 1:
                        options[option[0]] = 1
                        continue
                    options[option[0]] = option[1]

                opt_list.append(options)

                for options_with_pcre in options_pcre[1:]:

                    option_pairs = list(map(lambda x: x.split(":"), options_with_pcre.split("; ")))

                    options = {}
                    if option_pairs[0][0] == '!':
                        options['content'] = option_pairs[0][0][2:-1]
                        options['not'] = 1
                    else:
                        options['content'] = option_pairs[0][0][1:-1]
                        options['not'] = 0
                    options["pcre"] = 1

                    for option in option_pairs[1::]:
                        if len(option) == 1:
                            options[option[0]] = 1
                            continue
                        options[option[0]] = option[1]

                    opt_list.append(options)


            # TODO: Packet generation
            packet = b""

            pcre = 0

            if is_http:
                continue
            else:
                packet_str = ""
                for opt in opt_list:
                    pcre = opt.get("pcre", 0)
                    if pcre:
                        content = opt.get("content")
                        if len(content) > 300: continue
                        offset = int(opt.get("offset", 0))
                        depth = int(opt.get("depth", offset + len(content)))
                        length = int(opt.get("length", len(content)))

                        xeg = Xeger(limit=length)
                        reverse = ""
                        if opt.get("not"):
                            reverse = xeg.xeger(f"^(?!({content})).*")
                        else:
                            reverse = xeg.xeger(content)
                        left_buf = generate(max(0, offset - len(packet_str)))
                        right_buf = generate(max(0, depth - offset - len(content)))
                        packet_str = packet_str[:min(offset, len(packet_str))] + left_buf + reverse + right_buf + ("" if len(packet_str) <= depth else packet_str[depth:])
                    else:
                        content = opt.get("content")
                        content_str = ""
                        for i, chunk in enumerate(content.split('|')):
                            if i % 2:
                                content_str += ''.join(list(map(lambda x: chr(int(x, 16)), chunk.split())))
                            else:
                                content_str += chunk
                        offset = int(opt.get("offset", 0))
                        depth = int(opt.get("depth", offset + len(content_str)))
                        length = int(opt.get("length", len(content_str)))
                        left_buf = generate(max(0, offset - len(packet_str)))
                        right_buf = generate(max(0, depth - offset - len(content)))
                        packet_str = packet_str[:min(offset, len(packet_str))] + left_buf + content_str + right_buf + ("" if len(packet_str) <= depth else packet_str[depth:])


                for ch in packet_str:
                    packet += int.to_bytes(ord(ch))
                        

            prot_id = 2
            match protocol:
                case "tcp":
                    prot_id = 1
                case "udp":
                    prot_id = 2
                case "icmp":
                    prot_id = 3

            if ports.isnumeric():
                packet_counter += 1
                write_packet(prot_id, int(ports), packet)
            elif ports[0] == '[' and ports[-1] == ']':
                ports = list(map(int, ports[1:-1].split(',')))
                for port in ports:
                    packet_counter += 1
                    write_packet(prot_id, port, packet)
            else:
                continue


