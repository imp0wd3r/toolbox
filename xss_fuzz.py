#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
Simple xss fuzz

Author: p0wd3r
'''

import urlparse
import re
import gevent
from gevent import monkey; monkey.patch_all()
import requests
import argparse
import urllib
import colorama


class XssFuzz(object):

    url = ''
    para = ''
    payload_file = ''
    xss_num = 0


    def main(self):
        colorama.init(autoreset=True)

        parser = argparse.ArgumentParser(description=
            'make xss fuzz with simple payloads')
        parser.add_argument('-u', help='the url you want to fuzz', dest='url', required=True)
        parser.add_argument('-f', help='payload file', dest='payload_file', required=True)
        parser.add_argument('-p', help='the parameter you want to fuzz on', dest='para')
        parser.add_argument('--data', help='post data', dest='data')
        args = parser.parse_args()
        self.url = args.url
        self.para = args.para
        self.payload_file = args.payload_file

        try:
            if args.data:
                self.g(args.data)
            else :
                self.g()
            self.print_result()
        except KeyboardInterrupt:
            print colorama.Fore.RED + '[-] User aborted'

    def g(self, post_data=None):
        with open(self.payload_file, 'r') as f:
            payloads = iter(f)
            for payload in payloads:
                payload = payload.strip()
                if post_data:
                    gevent.spawn(self.post_fuzz, post_data, payload).join()
                else :
                    gevent.spawn(self.get_fuzz, payload).join()

    def get_fuzz(self, payload):
        print colorama.Fore.BLUE + '[*] Payload: ' + payload

        if self.para:
            url = re.sub(self.para + r'=[\d\w]*', self.para + '=' + payload, self.url)
            html = requests.get(url).content
            self.save_result(html, url)
        else :
            url_parts = list(urlparse.urlparse(self.url))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            for k, v in query.items():
                query[k] = payload
                url_parts[4] = urllib.urlencode(query)
                url = urlparse.urlunparse(url_parts)
                try:
                    html = requests.get(url, timeout=5).content
                    self.save_result(html, url, para=k)
                except requests.exceptions.Timeout:
                    print colorama.Fore.RED + '[-] Connection timeout'
                    break
                query[k] = v

    def post_fuzz(self, post_data, payload):
        print colorama.Fore.BLUE + '[*] Payload: ' + payload

        if self.para:
            data_str = re.sub(self.para + r'=[\d\w]*', self.para + '=' + payload, post_data)
            data_dict = dict(urlparse.parse_qsl(data_str))
            html = requests.post(self.url, data=data_dict).content
            self.save_result(html, payload=payload)
        else :
            data_dict = dict(urlparse.parse_qsl(post_data))
            for k, v in data_dict.items():
                data_dict[k] = payload
                try:
                    html = requests.post(self.url, data=data_dict, timeout=5).content
                    self.save_result(html, payload=payload, para=k)
                except requests.exceptions.Timeout:
                    print colorama.Fore.RED + '[-] Connection timeout'
                    break
                data_dict[k] = v

    def save_result(self, html, url=None, payload=None, para=None):
        result = re.findall(r'alert\(23333\)', html)
        if not para:
            para = self.para
        if result:
            self.xss_num = self.xss_num + 1
            with open('fuzz.log', 'a') as f:
                if url:
                    print colorama.Fore.GREEN + '[+] Xss!: ' + url
                    log_msg = 'type:GET' + '\n' +  'url:' + url + '\n' + 'para:' + para + '\n\n'
                else :
                    print colorama.Fore.GREEN + '[+] Xss!: ' + self.url
                    log_msg = 'type:POST' + '\n' + 'url:' + self.url + '\n' + 'para:' + para + '\n' + 'payload:' + payload + '\n\n'

                f.write(log_msg)

    def print_result(self):
        if self.xss_num:
            print colorama.Fore.GREEN + '\n[+] Find ' + str(self.xss_num) + ' xss'
            print colorama.Fore.GREEN + '[+] The results have been saved to ./fuzz.log'
        else :
            print colorama.Fore.RED + '\n[-] The url seems to be invulnerable'

if __name__ == '__main__':
    f = XssFuzz()
    f.main()
