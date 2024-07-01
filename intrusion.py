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


rules = [
    {"msg": "MALWARE-BACKDOOR - Dagger_1.4.0", "proto": "tcp", "dport": 2589, "payload": b"\x02\x00\x00\x06\x00\x00\x00\x44\x72\x69\x76\x65\x73\x24\x00"},
    {"msg": "MALWARE-BACKDOOR QAZ Worm Client Login access", "proto": "tcp", "dport": 7597, "payload": b"qazwsx.hsq"},
    {"msg": "MALWARE-BACKDOOR NetBus Pro 2.0 connection established", "proto": "tcp", "dport": 20034, "payload": b"BN\x10\x00\x02\x00\x05\x00"},
    {"msg": "MALWARE-BACKDOOR SatansBackdoor.2.0.Beta", "proto": "tcp", "dport": 666, "payload": b"Remote: You are connected to me.\r\nRemote: Ready for commands"},
    {"msg": "MALWARE-BACKDOOR Doly 2.0 access", "proto": "tcp", "dport": 6789, "payload": b"Wtzup Use"},
    {"msg": "example", "proto": "tcp", "dport": 6789, "payload": "example"},
    {"msg": "example", "proto": "tcp", "dport": 80, "payload": "example"},
    {"msg": "MALWARE-BACKDOOR HackAttack 1.20 Connect", "proto": "tcp", "dport": 31785, "payload": b"host"},
    {"msg": "PROTOCOL-FTP ADMw0rm ftp login attempt", "proto": "tcp", "dport": 21, "payload": b"USER w0rm"},
    {"msg": "MALWARE-BACKDOOR GateCrasher", "proto": "tcp", "dport": 6969, "payload": b"GateCrasher Server On-Line..."},
    {"msg": "MALWARE-BACKDOOR BackConstruction 2.1 Server FTP Open Reply", "proto": "tcp", "dport": 666, "payload": b"FTP Port open"},
    {"msg": "MALWARE-BACKDOOR Matrix 2.0 Client connect", "proto": "udp", "dport": 3344, "payload": b"activate"},
    {"msg": "MALWARE-BACKDOOR Matrix 2.0 Server access", "proto": "udp", "dport": 3345, "payload": b"logged in"},
    {"msg": "MALWARE-BACKDOOR WinCrash 1.0 Server Active", "proto": "tcp", "dport": 5714, "payload": b"\xB4\xB4"},
    {"msg": "MALWARE-BACKDOOR CDK", "proto": "tcp", "dport": 79, "payload": b"ypi0ca"},
    {"msg": "MALWARE-BACKDOOR DeepThroat 3.1 Server Response", "proto": "udp", "dport": 2140, "payload": b"Ahhhh My Mouth Is Open"},
    {"msg": "MALWARE-BACKDOOR PhaseZero Server Active on Network", "proto": "tcp", "dport": 555, "payload": b"phAse zero server"},
    {"msg": "MALWARE-BACKDOOR w00w00 attempt", "proto": "tcp", "dport": 23, "payload": b"w00w00"},
    {"msg": "MALWARE-BACKDOOR attempt", "proto": "tcp", "dport": 23, "payload": b"backdoor"},
    {"msg": "MALWARE-BACKDOOR MISC r00t attempt", "proto": "tcp", "dport": 23, "payload": b"r00t"},
    {"msg": "MALWARE-BACKDOOR MISC rewt attempt", "proto": "tcp", "dport": 23, "payload": b"rewt"},
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
        send_udp_packet(target_ip, rule["dport"], rule["payload"])

print("All packets sent.")
