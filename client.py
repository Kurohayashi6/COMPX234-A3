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


