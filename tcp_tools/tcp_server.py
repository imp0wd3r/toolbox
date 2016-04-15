#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading


bind_ip = '0.0.0.0'
bind_port = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print '[*] Listening on %s:%d' % (bind_ip, bind_port)

def handle_client(client_socket):
    while 1:
        request = client_socket.recv(2048)
        if not len(request):
            print '[-] Client exit'
            break
        print '[+] Received: %s' % request
        print '[+] Upper: %s' % request.upper()
        client_socket.send(request.upper())

    client_socket.close()


if __name__ == '__main__':
    client_list = []

    while 1:
        try:
            client, addr = server.accept()
            client_list.append(client)
            print '[+] Accepted connection from: %s:%d' % (addr[0], addr[1])

            client_thread = threading.Thread(target=handle_client, args=(client,))
            client_thread.daemon = True
            client_thread.start()

        except KeyboardInterrupt:
            print '[-] Server exit'
            break
