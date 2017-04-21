import socket
from multiprocessing import Pool
import argparse

socket.setdefaulttimeout(10)

# core
def scan(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            s.close()
            print('The {} port should be opened!'.format(port))
        except socket.error:
            pass

# Argument
parser = argparse.ArgumentParser(description = 'a python version nmap')
parser.add_argument('host', help = 'scan the host')

args = parser.parse_args()

#start scan
if args.host:
    print('Start scan {}...'.format(args.host))
    p = Pool(4)

    for port in range(1, 1025):
        p.apply_async(scan, args = (args.host, port))

    p.close()
    p.join()
