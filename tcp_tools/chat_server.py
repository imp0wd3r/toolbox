#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading


class ChatServer(object):
    def __init__(self):
        self.thread_condition = threading.Condition()
        self.data = ''

    def main(self):
        """main"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 6969))
        sock.listen(5)
        print '[*] Server started'

        while True:
            try:
                conn, addr = sock.accept()
                username = conn.recv(1024)
                self.send_to_all('Welcome: ' + username)

                thread_out = threading.Thread(target=self.handler_out, args=(conn, username))
                thread_out.daemon = True
                thread_out.start()
                thread_in = threading.Thread(target=self.handler_in, args=(conn, username))
                thread_in.daemon = True
                thread_in.start()
            except KeyboardInterrupt:
                exit('\n' + '[-] User aborted')

    def handler_out(self, conn, username):
        """thread handler for sending data"""
        while True:
            with self.thread_condition:
                self.thread_condition.wait()
                if self.data:
                    try:
                        conn.send(self.data)
                    except:
                        return

    def handler_in(self, conn, username):
        """thread handler for receiving data"""
        while True:
            try:
                in_str = conn.recv(1024)
                if not in_str:
                    conn.close()
                    return
                self.send_to_all(in_str)
                print self.data
            except:
                self.send_to_all(username + 'leaves')
                print self.data
                return

    def send_to_all(self, data):
        """send data to all user"""
        with self.thread_condition:
            self.data = data
            self.thread_condition.notifyAll()


if __name__ == '__main__':
    server = ChatServer()
    server.main()
