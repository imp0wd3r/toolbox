#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import sys


target_host = sys.argv[1]
target_port = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((target_host, target_port))

    response = ''

    while 1:
        data = raw_input('Say what you want: ')
        client.send(data)

        data = client.recv(2048)
        response += data
        if not len(data):
            print '[-] Server exit'
            break
        print response

except KeyboardInterrupt:
    print '[-] Client exit'
    client.close()

except Exception, e:
    print e
    client.close()
