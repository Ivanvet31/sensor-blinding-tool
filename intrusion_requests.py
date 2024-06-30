from scapy.all import *


def send_tcp_packet(rule):
    alert = IP(dst="109.71.242.119") / TCP(dport=rule["dport"], sport=RandShort(), flags="S") / Raw(load="GET / HTTP/1.0\r\n\r\n")
    send(alert, verbose=0)


def send_udp_packet(rule):
    alert = IP(dst="109.71.242.119") / UDP(dport=rule["dport"]) / Raw(load="DNS payload")
    send(alert, verbose=0)


suricata_rules = [
    {
        "msg": "ET SCAN Sipvicious User-Agent Detected (sipvicious)",
        "content": "User-Agent|3a| friendly-scanner",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET TROJAN Observed Malicious SSL Cert (likely Crypto Miner)",
        "content": "|30 82 01 0a 02 82 01 01|",
        "proto": "tls",
        "dport": 443
    },
    {
        "msg": "GPL ATTACK_RESPONSE SSH-1.99 Protocol Version Detected",
        "content": "SSH-1.99",
        "proto": "tcp",
        "dport": 22
    },
    {
        "msg": "ET SCAN Nmap Scripting Engine User-Agent Detected (Nmap NSE)",
        "content": "Nmap Scripting Engine User-Agent",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET TROJAN W32/Mytob.AA SMTP User-Agent Detected",
        "content": "MAIL FROM",
        "proto": "tcp",
        "dport": 25
    },
    {
        "msg": "ET SCAN Sipvicious Scan",
        "content": "GET / HTTP/1.0|0d0a|Host: 192.168.1.1|0d0a|",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "GPL ATTACK_RESPONSE Successful SSLv3.0 Client Hello",
        "content": "SSLv3.0 ClientHello",
        "proto": "tls",
        "dport": 443
    },
    {
        "msg": "ET SCAN Potential SSH Scan",
        "content": "SSH-2.0-libssh-0.1",
        "proto": "tcp",
        "dport": 22
    },
    {
        "msg": "ET TROJAN Zbot/Pushdo Checkin",
        "content": "|18 03 01 00|",
        "proto": "tls",
        "dport": 443
    },
    {
        "msg": "ET SCAN NMAP -sS window 1024",
        "content": "S|c0 14|",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET TROJAN Fake Flash Update Request",
        "content": "GET /mrclean.exe HTTP/1.1|0d0a|Host: 192.168.1.1|0d0a|",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET SCAN Potential SSH Scan (psscan)",
        "content": "SSH-2.0-Scan",
        "proto": "tcp",
        "dport": 22
    },
    {
        "msg": "ET POLICY PE EXE or DLL Windows file download HTTP",
        "content": "GET /test.exe",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET POLICY PE EXE or DLL Windows file download HTTP (from untrusted zone)",
        "content": "GET /test.exe",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET POLICY PE EXE or DLL Windows file download HTTP (from internal network)",
        "content": "GET /test.exe",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET POLICY PE EXE or DLL Windows file download HTTP (from external network)",
        "content": "GET /test.exe",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET POLICY exe in inbound HTTP request",
        "content": "GET /file.exe",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET POLICY exe in outbound HTTP request",
        "content": "GET /file.exe",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET POLICY exe Windows executable file sent by HTTP",
        "content": "GET /file.exe",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET POLICY PE EXE or DLL Windows file download HTTP (from internal network)",
        "content": "GET /test.exe",
        "proto": "tcp",
        "dport": 80
    },
    {
        "msg": "ET POLICY exe in outbound HTTP request",
        "content": "GET /file.exe",
        "proto": "tcp",
        "dport": 80
    },
]

for rule in suricata_rules:
    if rule["proto"] == "tcp":
        send_tcp_packet(rule)
    elif rule["proto"] == "udp":
        send_udp_packet(rule)