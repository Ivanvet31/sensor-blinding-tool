from scapy.all import *


def send_tcp_packet(dst_ip, dport, payload):
    packet = IP(dst=dst_ip) / TCP(dport=dport, sport=RandShort(), flags="S") / Raw(load=payload)
    send(packet, verbose=0)


def send_udp_packet(dst_ip, dport, payload):
    packet = IP(dst=dst_ip) / UDP(dport=dport) / Raw(load=payload)
    send(packet, verbose=0)


def send_dns_packet(dst_ip, dport, query):
    packet = IP(dst=dst_ip) / UDP(dport=dport) / DNS(rd=1, qd=DNSQR(qname=query))
    send(packet, verbose=0)


def send_icmp_packet(dst_ip, payload):
    packet = IP(dst=dst_ip) / ICMP() / Raw(load=payload)
    send(packet, verbose=0)


rules = [
    {"proto": "tcp", "dport": "20:100", "payload": "example"},
    {"proto": "udp", "dport": "21:23", "payload": "example"},
    {"proto": "dns", "dport": "21:23", "payload": "example"},
    {"proto": "icmp", "dport": "21:23", "payload": "example"},
    
    # {"proto": "tcp", "dport": "1:65535", "payload": b"\x02\x00\x00\x06\x00\x00\x00\x44\x72\x69\x76\x65\x73\x24\x00"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"qazwsx.hsq"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"BN\x10\x00\x02\x00\x05\x00"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"Remote: You are connected to me.\r\nRemote: Ready for commands"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"Wtzup Use"},
    
    # {"proto": "tcp", "dport": "1:65535", "payload": b"host"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"USER w0rm"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"GateCrasher Server On-Line..."},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"FTP Port open"},
    # {"proto": "udp", "dport": "1:65535", "payload": b"activate"},
    # {"proto": "udp", "dport": "1:65535", "payload": b"logged in"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"\xB4\xB4"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"ypi0ca"},
    # {"proto": "udp", "dport": "1:65535", "payload": b"Ahhhh My Mouth Is Open"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"phAse zero server"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"w00w00"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"backdoor"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"r00t"},
    # {"proto": "tcp", "dport": "1:65535", "payload": b"rewt"},
]

target_ip = "109.71.242.119"

for rule in rules:
    if rule["proto"] == "tcp":
        if isinstance(rule["dport"], str) and ":" in rule["dport"]:
            dport_start, dport_end = map(int, rule["dport"].split(":"))
            for port in range(dport_start, dport_end + 1):
                send_tcp_packet(target_ip, port, rule["payload"])
        else:
            send_tcp_packet(target_ip, rule["dport"], rule["payload"])
    elif rule["proto"] == "udp":
        if isinstance(rule["dport"], str) and ":" in rule["dport"]:
            dport_start, dport_end = map(int, rule["dport"].split(":"))
            for port in range(dport_start, dport_end + 1):
                send_udp_packet(target_ip, port, rule["payload"])
        else:
            send_udp_packet(target_ip, rule["dport"], rule["payload"])
    elif rule["proto"] == "icmp":
        send_icmp_packet(target_ip, rule["payload"])

print("All packets sent.")
