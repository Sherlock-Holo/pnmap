import socket
import sys
with open('r-file', 'rb') as r:
    c = r.read()
def send(host):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(c, (host, 5353))
while True:
    send(sys.argv[1])
