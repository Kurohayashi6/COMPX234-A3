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

def print_server_sta():
    while True:
        time.sleep(10)
        with lock:
            num_tuples = len(tuple_space)
            if num_tuples > 0:
                avg_key_size = sum(len(k) for k in tuple_space.keys()) / num_tuples
                avg_val_size = sum(len(v) for v in tuple_space.values()) / num_tuples
                avg_tuple_size = avg_key_size + avg_val_size
            else:
                avg_key_size = avg_val_size = avg_tuple_size = 0.0

            print(f"Server Status Summary")
            print(f"Tuples in space: {num_tuples}")
            print(f"Avg tuple size: {avg_tuple_size:.2f} (Key: {avg_key_size:.2f}, Val: {avg_val_size:.2f})")
            print(f"Total clients connected: {sta['total_clients']}")
            print(f"Total operations: {sta['total_ops']} "
                  f"(READs: {sta['total_reads']}, GETs: {sta['total_gets']}, PUTs: {sta['total_puts']})")
            print(f"Total errors: {sta['total_errors']}")

            



