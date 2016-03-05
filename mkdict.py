#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
Produce more keys depending on what you have added

Author: p0wd3r
'''

import argparse
import textwrap


class MkDict(object):

    def main(self):
        parser = argparse.ArgumentParser(description=
            'Produce more keys depending on what you have added',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''
                Example:
                    python produce_dict.py -k admin -p 123,888 -a
                    python produce_dict.py -f keys.txt -l payloads.txt
            ''')
            )

        key_group = parser.add_mutually_exclusive_group()
        payload_group = parser.add_mutually_exclusive_group()
        key_group.add_argument('-k', help='add key', dest='key')
        key_group.add_argument('-f', help='add keys from keyfile', dest='key_file')
        payload_group.add_argument('-p', help='payloads', dest='payloads')
        payload_group.add_argument('-l', help='payloads file', dest='payloads_file')
        parser.add_argument('-c', help='the file you would add keys to', dest='current_key_file',
            default='dict.txt')
        parser.add_argument('-b', '--before', help='add payloads before key', action='store_true')
        parser.add_argument('-a', '--after', help='add payloads after key', action='store_true')

        args = parser.parse_args()

        self.add(args.key, args.key_file, args.current_key_file, args.before, args.after,
            args.payloads, args.payloads_file)

    def add(self, key=None, key_file=None, current_key_file='dict.txt', before=False, after=False,
        payloads=None, payloads_file=None):
        with open(current_key_file, 'a') as f:
            if key:
                for i in self.produce(key, payloads, payloads_file, before, after):
                    f.write(i + '\n')
            if key_file:
                with open(key_file, 'r') as r:
                    for key in r:
                        for i in self.produce(key.strip(), payloads, payloads_file, before, after):
                            f.write(i + '\n')

            print '[*] Done! The dictionary is in : %s ' % current_key_file

    def produce(self, key, payloads, payloads_file, before, after):
        result = []

        if payloads:
            payloads = payloads.split(',')
            result = self.joint(key, payloads, before, after, result)
        elif payloads_file:
            with open(payloads_file, 'r') as f:
                payloads_f = f.readlines()
            result = self.joint(key, payloads_f, before, after, result)

        result.append(key)

        return result

    def joint(self, key, payloads, before, after, result):
        for payload in payloads:
            if before and not after:
                result.append(str(payload).strip() + key)
            elif not before and after:
                result.append(key + str(payload).strip())
            else:
                result.append(str(payload).strip() + key)
                result.append(key + str(payload).strip())

        return result

if __name__ == '__main__':
    m = MkDict()
    m.main()
