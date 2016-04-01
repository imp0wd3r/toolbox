#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Get phone info from apix.cn

Author: p0wd3r
'''

import requests
import json
import argparse
import prettytable


def main():
    parser = argparse.ArgumentParser(description=
                                     'Get phone info from apix.cn')
    parser.add_argument('phone_num', help='phone number')
    args = parser.parse_args()

    url = 'http://a.apix.cn/apixlife/phone/phone'
    querystring = {'phone': args.phone_num}
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'apix-key': ''
    }
    json_data = requests.get(url, headers=headers, params=querystring).content
    try:
        dict_data = json.loads(json_data)
    except Exception, e:
        exit(e)

    if dict_data['message'] == 'success':
        data = dict_data['data']

        table = prettytable.PrettyTable(['号码', '省份', '城市', '运营商'])
        table.add_row([args.phone_num, data['province'], data['city'], data['operator']])
        print table
    else:
        print '[-] 号码不合法'

if __name__ == '__main__':
    main()
