#!/usr/bin/env python3

import sys
import threading 
import time
from scapy.all import *

def handle_dhcp(packet):

    #parse DHCPOffer   
    if DHCP in packet and packet[DHCP].options[0][1] == 2:
        print("* DHCPOFFER received:")

        print("ip offered = {}".format(packet[BOOTP].yiaddr))

        for opt in packet[DHCP].options:
            if opt == 'end': 
                break
            print("{} = {}".format(opt[0], opt[1]))
            
        print ("* done")
        sys.exit(1)


def do_discovery(iface):

    # construct discovery packet
    print ("* constructing DHCPDISCOVER packet")
    src_mac = get_if_hwaddr(iface)
    p_ether = Ether(dst='ff:ff:ff:ff:ff:ff',src=src_mac,type=0x800)
    p_ip = IP(src='0.0.0.0', dst='255.255.255.255')
    p_udp = UDP(dport=67, sport=68)
    p_bootp = BOOTP(chaddr=mac2str(src_mac), ciaddr='0.0.0.0', op=1, xid=0x01020304)
    req_opts = [ 1, 3, 6, 15, 44, 33, 119,150, 43]
    p_dhcp = DHCP(options=[('message-type','discover'),('param_req_list', req_opts),('end')])
    packet = p_ether / p_ip / p_udp / p_bootp / p_dhcp

    #ls(packet)

    print("* sending DHCPDISCOVER...")
    sendp(packet, iface=iface, verbose=False)


def wait_for_offer():
    print("* waiting for DHCPOFFER")
    sniff(iface=iface, filter="udp and port 67", prn=handle_dhcp) 


if (len(sys.argv) < 2):
    print("{} interface".format(sys.argv[0]))
    sys.exit(1)

iface = sys.argv[1]


t = threading.Thread(target=wait_for_offer)
t.start()
time.sleep(2)

do_discovery(iface)