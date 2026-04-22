import socket
import sys
import threading
import time


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        last = sock.recv(n - len(data))
        if not last:
            return None
        data.extend(last)
    return data.decode('utf-8')

def client_task(filename):
    #if len(sys.argv) != 4:
        #print("Usage: python client.py <hostname> <port> <filename>")
        #sys.exit(1)

    if len(sys.argv) != 3:
        print("Usage: python client.py <hostname> <port>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    #filename = sys.argv[3]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)


