#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
import socket
import argparse
import re

socket.setdefaulttimeout(1)

# core
def scan(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print('The {} port should be opened!'.format(port))
        except socket.error:
            pass

# Argument
parser = argparse.ArgumentParser(description='a python version nmap')
parser.add_argument('host', help='scan the host')
parser.add_argument('-a', '--all', action='store_true',
                    help="scan all port (WARNING: It will use a lot of time!)")
parser.add_argument('-p', '--port', help='scan the port or port range')

args = parser.parse_args()

pool = ThreadPoolExecutor(20)

if args.port:
    port = re.split(r'[:\s-]\s*', args.port)
    if len(port) == 2:
        start_p = int(port[0])
        end_p = int(port[1])

        print('Start scan {}:{}-{} ...'.format(args.host, start_p, end_p))

        for p in range(start_p, end_p + 1):
            future = pool.submit(scan, args.host, p)

    else:
        future = pool.submit(scan, args.host, int(args.port))

elif args.all:
    print('Start full scan for {} ...'.format(args.host))
    for p in range(1, 65536):
        future = pool.submit(scan, args.host, p)

else:
    print('Start normal scan for {} ...'.format(args.host))
    for p in range(1, 10001):
        future = pool.submit(scan, args.host, p)
