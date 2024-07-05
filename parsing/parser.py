#! /usr/bin/env python

import sys
import random
import re

DEBUG = 1

vars = {}

output = open('../packets/packets.bin', 'wb')

def get_variables(file_str : str):
    global vars

    with open(file_str, 'r') as file:
        lines = file.readlines()

        for line in lines:
            m = re.match(r"^([a-zA-Z]*)var\s+(\w+)\s+(.*)", line)
            if m:
                key = m.group(1)
                name = m.group(2)
                value = m.group(3)

                if value[0] == '$':
                    vars[name] = [vars[value[1:]][0], key]
                else:
                    vars[name] = [value, key]

def write(output, protocol, port, packet):
    if not output: return

    data = int.to_bytes(protocol, 1) + int.to_bytes(port, 2) + int.to_bytes(len(packet), 4) + packet

    output.write(data)

def parse_content(content : str):
    m = re.search(r"^([^\|]*)\|([^\|]*)\|(.*)", content)
    if m is None: return bytes(content, 'ascii')
    
    hexed = b''.join(list(map(lambda x: int.to_bytes(int(x, 16), 1), m.group(2).split())))

    return bytes(m.group(1), 'ascii') + hexed + parse_content(m.group(3))


def content_generate(contents, is_http, cont_str, opt_str):
    opts = {}

    opt_match = re.findall(r'(\w+):?([\w,-]*);', opt_str)

    if opt_match is None: return
    
    for opt in opt_match:
        opt_0 = re.sub(r'http_raw_?', r'http_', opt[0])
        opts[opt_0] = 1 if opt[1] == '' else opt[1]
    
    
    if not is_http:
        contents.append(b'A' * int(opts.get('offset', 0)) + parse_content(cont_str))
        return

    if opts.get('http_method', 0):
        if not contents.get('method', 0): contents['method'] = b''
        contents['method'] += b'A' * int(opts.get('offset', 0)) + parse_content(cont_str)
    if opts.get('http_uri', 0):
        if not contents.get('uri', 0): contents['uri'] = b''
        contents['uri'] += b'A' * int(opts.get('offset', 0)) + parse_content(cont_str)
    if opts.get('http_header', 0):
        if not contents.get('header', 0): contents['header'] = b''
        contents['header'] += b'A' * int(opts.get('offset', 0)) + parse_content(cont_str)
    if opts.get('http_cookie', 0):
        if not contents.get('cookie', 0): contents['cookie'] = b''
        contents['cookie'] += b'A' * int(opts.get('offset', 0)) + parse_content(cont_str) + b';'
    if opts.get('http_client_body', 0):
        if not contents.get('body', 0): contents['body'] = b''
        contents['body'] += b'A' * int(opts.get('offset', 0)) + parse_content(cont_str)


if __name__ == '__main__':

    finputs = sys.argv[2:]
    foutput = '../packets/packets.bin'

    get_variables(sys.argv[1])

    for finput in finputs:
        print('Parsing', finput)
        with open(finput, 'r') as rule_file:
            rules = rule_file.readlines()
            for rule in rules:
                try:

                    rule_match : re.Match | None = re.match(r"^#(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(->|<>|<-)\s+(\S+)\s+(\S+)\s+(.*)$", rule)

                    if rule_match is None:
                        continue

                    logtype = rule_match.group(1)
                    proto = rule_match.group(2)
                    src = rule_match.group(3)
                    src_port = rule_match.group(4)
                    dir = rule_match.group(5)
                    dst = rule_match.group(6)
                    dst_port = rule_match.group(7)
                    options = rule_match.group(8)

                    options = re.sub(r'nocase;', r'', options)

                    dsize_match = re.search(r'dsize\s*:\s*([^;]+);', options)
                    dsize = ''
                    if not dsize_match is None:
                        dsize = dsize_match.group(1)

                    content_pattern = re.compile(r'content\s*:\s*"([^"]+)";(.*?)(content\s*:.*)')

                    content_match = content_pattern.search(options)

                    is_http = 'http' in dst.lower() or 'http' in dst_port.lower()

                    if is_http:
                        contents = {'version' : b'HTTP/1.1'}
                    else:
                        contents = []

                    
                    while not content_match is None:
                        content_generate(contents, is_http, content_match.group(1), content_match.group(2))
                        options = content_match.group(3)
                        content_match = content_pattern.search(options)

                    cont = re.search(r'content\s*:"([^"]+)";(.*)', options)
                    if cont:
                        content_generate(contents, is_http, cont.group(1), cont.group(2))

                    payload = ''
                    if is_http:
                        uri = contents.get('uri', b'/dir ')
                        if chr(uri[0]) != '/': uri = b'/' + uri
                        cl_body = contents.get('body', b'A' * 10)
                        if len(contents.keys()) == 1: continue
                        lst = [
                                contents.get('method', b'GET') + b' ',
                                uri + b' ',
                                contents.get('version') + b'\n',
                                b'Host: something.com\n',
                                contents.get('header', b'Something: Something') + b'\nContent-length: ' + bytes(str(len(cl_body)), 'ascii'),
                                contents.get('cookie', b'') + b'\n\n',
                                cl_body
                            ]

                        payload = b''.join(lst)
                    else:
                        payload = b''.join(contents)
                    print(payload)

                    if dsize:
                        dmatch = re.match(r'(\D?)(\d+)', dsize)
                        if not dmatch is None:
                            sign = dmatch.group(1)
                            padlen = int(dmatch.group(2)) - len(payload)
                            padlen += 1 if sign == '>' else -1 if sign == '<' else 0
                            payload += b'B' * padlen

                    var = vars.get(dst_port[(dst_port[0] == '$'):], 0)
                    if var:
                        dst_port = var[0]

                    port_match = re.findall(r'\[?[,]?(\d+)[:]?\]?', dst_port)
                    if port_match != []:
                        ports = list(map(int, port_match))
                    else:
                        ports = [random.randint(0, 65535)]

                    protocol = 2
                    match proto:
                        case 'tcp':
                            protocol = 1
                        case 'udp':
                            protocol = 2
                        case 'icmp':
                            protocol = 3


                    for port in ports:
                        write(output, protocol, port, payload)

                except Exception as e:
                    continue

