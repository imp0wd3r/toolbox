#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Get ip from ip.taobao.com

Author: p0wd3r
'''

import requests
import json
import argparse
import prettytable
import dns.resolver


def main():
    parser = argparse.ArgumentParser(description=
                                     'Get ip from ip.taobao.com')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--ip', help='IP address', dest='ip')
    group.add_argument('--host', help='Host address', dest='host')
    args = parser.parse_args()

    ip_list = []
    if args.ip:
        ip_list.append(args.ip)
    else:
        try:
            answer = dns.resolver.query(args.host, 'A')
            for r in answer:
                ip_list.append(r)
        except dns.resolver.NXDOMAIN:
            print '[-] Cannot resolve hostname'

    for ip in ip_list:
        data_json = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=' + str(ip)).content
        data = json.loads(data_json)
        if data['code'] == 0:
            data = data['data']
            table = prettytable.PrettyTable(['IP', '国家', '省份', '城市', '运营商'])
            table.add_row([str(ip), data['country'], data['region'], data['city'], data['isp']])
            print table
        else:
            print '[-] ' + data['data']

if __name__ == '__main__':
    main()
