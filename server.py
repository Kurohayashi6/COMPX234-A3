import socket
import threading
import sys
import time

tuple_space = {}

sta = {
    'total_clients': 0,
    'total_ops': 0,
    'total_reads': 0,
    'total_gets': 0,
    'total_puts': 0,
    'total_errors': 0
}

lock = threading.Lock()


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        last = sock.recv(n - len(data))
        if not last:
            return None
        data.extend(last)
    return data.decode('utf8')



