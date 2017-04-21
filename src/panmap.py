import socket
import asyncio
import argparse

socket.setdefaulttimeout(10)

# core
def scan(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            s.close()
            return True
        except socket.error:
            return False

async def ascan(host, port):
    future = loop.run_in_executor(None, scan, host, port)
    result = await future
    return result

async def run(host, port):
    #print('Start scan {}:{}'.format(host, port))
    result = await ascan(host, port)
    if result:
        print('{}:{} should be opened!'.format(host, port))

# Argument
parser = argparse.ArgumentParser(description = 'a python version nmap')
parser.add_argument('host', help = 'scan the host')

args = parser.parse_args()

#start scan
if args.host:
    print('Start scan {}...'.format(args.host))
    tasks = []
    for p in range(1, 1025):
        tasks.append(run(args.host, p))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
