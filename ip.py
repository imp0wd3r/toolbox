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


def main():
    parser = argparse.ArgumentParser(description=
                                     'Get ip from ip.taobao.com')
    parser.add_argument('ip', help='The ip address you want to query')
    args = parser.parse_args()

    json_data = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=' + args.ip).content
    data = json.loads(json_data)['data']
    table = prettytable.PrettyTable(['IP', '国家', '省份', '城市', '运营商'])
    table.add_row([args.ip, data['country'], data['region'], data['city'], data['isp']])
    print table

if __name__ == '__main__':
    main()
