#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Login/out ssdut campus network

Author: p0wd3r
'''

import re
import requests
import argparse


class SSDUTSrun(object):
    def __init__(self, user, pwd):
        self.session = requests.Session()
        self.user = user
        self.pwd = pwd
        self.url_login = 'http://172.20.20.1/cgi-bin/srun_portal'
        self.url_logout = 'http://172.20.20.1/rad_online.php'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
            'Referer': 'http://172.20.20.1/srun_portal.html?&ac_id=6&sys='
        }

    def do_request(self, url, data):
        """do request"""
        try:
            rep_html = self.session.post(url, headers=self.headers, data=data).content
            return rep_html
        except Exception, e:
            exit(e)

    def login(self):
        """login with username and password"""
        data = {
            'action': 'login',
            'username': self.user,
            'password': self.pwd,
            'ac_id': 6,
            'type': 1
        }
        rep_html = self.do_request(self.url_login, data=data)
        if re.search(r'login_ok', rep_html):
            print '[+] Login successful'
        else:
            print '[-] ' + rep_html

    def logout(self):
        """logout with sid"""
        data = {
            'username': self.user,
            'password': self.pwd
        }
        rep_html = self.do_request(self.url_logout, data=data)
        m = re.search(r'do_drop\(\'(.*)\'\)', rep_html)
        if m:
            data = {
                'action': 'dm',
                'sid': m.group(1)
            }
            rep_html = self.do_request(self.url_logout, data=data)
            if re.search(r'users droped', rep_html):
                print '[+] Logout successful'
            else:
                print '[-] ' + rep_html
        else:
            print '[-] Invalid username or password'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     'Login/out campus network')
    parser.add_argument('-u', help='username', dest='user', required=True)
    parser.add_argument('-p', help='password', dest='pwd', required=True)
    group_action = parser.add_mutually_exclusive_group(required=True)
    group_action.add_argument('-i', help='login', dest='login', action='store_true')
    group_action.add_argument('-o', help='logout', dest='logout', action='store_true')
    args = parser.parse_args()

    s = SSDUTSrun(args.user, args.pwd)
    if args.login:
        s.login()
    else:
        s.logout()
