#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import hexdump
import argparse
import sys
import threading


class TCPProxy(object):

    def index(self):
        parser = argparse.ArgumentParser(description=
                                         'Simple TCP proxy')
        parser.add_argument('-l', help='local port', dest='lport')
        parser.add_argument('-u', help='remote host', dest='rhost')
        parser.add_argument('-p', help='remote port', dest='rport')
        parser.add_argument('-f', help='receive first', dest='first', default='False')
        args = parser.parse_args()

        if 'True' in args.first:
            args.first = True
        else:
            args.first = False

        self.server_loop(args.lport, args.rhost, args.rport, args.first)

    def server_loop(self, client_port, remote_host, remote_port, receice_first):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server.bind(('127.0.0.1', int(client_port)))
        except:
            print '[-] Failed to listen on port %s' % client_port
            sys.exit(0)

        print '[*] Listening on %s' % client_port

        server.listen(5)

        while True:
            client_socket, addr = server.accept()
            print '[==>] Received incoming from %s:%d' % (addr[0], addr[1])

            proxy_thread = threading.Thread(target=self.proxy_handler,
                                            args=(client_socket, remote_host, remote_port, receice_first))
            proxy_thread.start()

    def proxy_handler(self, client_socket, remote_host, remote_port, receice_first):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, int(remote_port)))

        if receice_first:
            remote_buffer = self.receive_from(client_socket)
            hexdump(remote_buffer)

            if len(remote_buffer):
                print '[<==] Sending %d bytes to localhost' % len(remote_buffer)
                client_socket.send(remote_buffer)

        while True:
            local_buffer = self.receive_from(client_socket)
            if len(local_buffer):
                print '[*] Received %d bytes from localhost' % len(local_buffer)
                hexdump(local_buffer)

                remote_socket.send(local_buffer)
                print '[==>] Send to remote'

            remote_buffer = self.receive_from(remote_socket)
            if len(remote_buffer):
                print '[*] Received %d bytes from remote' % len(remote_buffer)
                hexdump(remote_buffer)

                client_socket.send(remote_buffer)
                print '[<==] Send to localhost'

            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print '[*] No more data. Closing connection'
                break

    def receive_from(self, connection):
        buf = ''

        connection.settimeout(5)
        try:
            while True:
                data = connection.recv(2048)
                if not data:
                    break
                buf += data
        except:
            print '[-] Error when receive'

        return buf


if __name__ == '__main__':
    t = TCPProxy()
    t.index()
