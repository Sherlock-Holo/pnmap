import re
import random
import logging
import argparse
from time import sleep
from scapy.all import *
from concurrent.futures import ThreadPoolExecutor

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# close the scapy output
conf.verb = 0

# color
fore = '\033[0;33m'
back = '\033[0m'

# core
def scan(host, port):
    # for escape the SYN flood detect
    sleep(random.randrange(1,2))

    s = sr1(IP(dst = host) / TCP(sport = RandShort(), dport = port, flags = 'S'), timeout = 1)

    if s.getlayer(TCP).flags == 18:
        print('The {}{}{} port should be opened'.format(fore,port,back))

# Argument
parser = argparse.ArgumentParser(description='a python version nmap')
parser.add_argument('host', help='scan the host')
parser.add_argument('-p', '--port', help='scan the port or port range')

args = parser.parse_args()

pool = ThreadPoolExecutor(20)

if args.port:
    port = re.split(r'[:\s-]\s*', args.port)
    if len(port) == 2:
        start_p = int(port[0])
        end_p = int(port[1])

        print('Start scan {}:{}-{} ...\n'.format(args.host, start_p, end_p))

        for p in range(start_p, end_p + 1):
            future = pool.submit(scan, args.host, p)

        pool.shutdown()
        print('\nFinish scan')

    else:
        print('Start scan {}:{} ...\n'.format(args.host, args.port))
        future = pool.submit(scan, args.host, int(args.port))
        pool.shutdown()
        print('\nFinish scan')

else:
    print('Start normal scan for {} ...\n'.format(args.host))
    for p in range(1, 10001):
        future = pool.submit(scan, args.host, p)

    pool.shutdown()
    print('\nFinish scan')
