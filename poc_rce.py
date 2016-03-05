#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Poc of RCE when execute `ping`

Author: p0wd3r
'''

from scapy.all import *


def packet_callback(packet):
    """packet callback"""
    try:
        if (packet[ICMP].type == 8) & (packet[IP].dst == '127.0.0.1'):
            print '[+] Receive echo request from: ' + packet[IP].src
    except Exception, e:
        print e


sniff(filter='icmp', prn=packet_callback, store=0)
