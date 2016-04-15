#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import threading


class ChatClient(object):
    def __init__(self):
        self.in_str = ''
        self.out_str = ''
        self.username = ''

    def main(self):
        """main"""
        self.username = raw_input('Please input your username: ')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 6969))
        sock.send(self.username)

        thread_out = threading.Thread(target=self.handler_out, args=(sock,))
        thread_out.daemon = True
        thread_out.start()
        thread_in = threading.Thread(target=self.handler_in, args=(sock,))
        thread_in.daemon = True
        thread_in.start()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                exit('\n' + '[-] User aborted')


    def handler_out(self, sock):
        """thread handler for sending data"""
        while True:
            self.out_str = raw_input()
            self.out_str = self.username + ':' + self.out_str
            sock.send(self.out_str)

    def handler_in(self, sock):
        """thread handler for receiving data"""
        while True:
            try:
                self.in_str = sock.recv(1024)
                if not self.in_str:
                    break
                if self.in_str != self.out_str:
                    print self.in_str
            except:
                break


if __name__ == '__main__':
    client = ChatClient()
    client.main()
