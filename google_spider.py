#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Get url from google with google hack

Author: p0wd3r
'''

import requests
import argparse
import threading
from urlparse import urlparse
from bs4 import BeautifulSoup


class GoogleSpider(object):
    def index(self):
        parser = argparse.ArgumentParser(description=
                                         'Get url from google with google hack')
        parser.add_argument('-d', help='google hack dork', dest='dork', required=True)
        parser.add_argument('-n', help='the number of urls that you want to collect', dest='num', default=10)
        args = parser.parse_args()

        page_tuple = divmod(int(args.num), 10)
        for i in xrange(0, page_tuple[0]):
            spider_thread = threading.Thread(target=self.spider_handler, args=(args.dork, i*10))
            spider_thread.start()

    def spider_handler(self, dork, num):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.85 Chrome/45.0.2454.85 Safari/537.36'
        }
        html = requests.get('https://www.google.com/search?q=' + dork + '&start=' + str(num), headers=headers, verify=False).content
        soup = BeautifulSoup(html, 'lxml')
        tags = soup.find_all('h3')
        for tag in tags:
            try:
                url = tag.find('a')['href']
                host = urlparse(url).netloc
                print host
            except Exception, e:
                print e


if __name__ == '__main__':
    g = GoogleSpider()
    g.index()
