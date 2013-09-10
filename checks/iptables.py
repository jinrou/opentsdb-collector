#! /usr/bin/python

import os
import sys
import time
import socket
import re
import subprocess


def main():
        out = subprocess.check_output('ip6tables -L -vnx', shell=True).split('\n')
        ts = int(time.time())
        targets = {}
        for line in out:
                m = re.match("\s*(?P<pkts>\d+)\s+(?P<bytes>\d+)\s+(?P<target>[A-Za-z-_]+)\s+.*\s+(?P<source>[a-fA-F0-9\:\/]+)\s+(?P<destination>[a-fA-F0-9\:\/]+)\s*$", line.strip())
                if not m:
                        continue
                if targets.has_key(m.group('target')) is True:
                	targets[m.group('target')]['bytes'] += m.group('bytes')
                	targets[m.group('target')]['pkts']  += m.group('pkts')
                else:
                	targets[m.group('target')] = {}
                	targets[m.group('target')]['bytes'] = m.group('bytes')
                	targets[m.group('target')]['pkts']  = m.group('pkts')                

        for key in targets.keys():
        	print ("ip6tables.pkts %d %s target=%s" % (ts, targets[key]['pkts'], key))
        	print ("ip6tables.bytes %d %s target=%s" % (ts, targets[key]['bytes'], key))

if __name__ == '__main__':
        main()