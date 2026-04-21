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

            
def handle_client(client_socket, addr):
    print(f"New client connected from {addr}.")

    with lock:
        sta['total_clients'] += 1
    with client_socket:
        while True:
            NNN = recvall(client_socket, 3)
            if not NNN:
                break

            msg_len = int(NNN)
            msg_body = recvall(client_socket, msg_len - 3)
            if not msg_body:
                break

            parts = msg_body.strip().split(' ', 2)
            cmd = parts[0]
            key = parts[1]
            val = parts[2] if len(parts) > 2 else ""

            with lock:
                sta['total_ops'] += 1

                if cmd == 'R':
                    sta['total_reads'] += 1
                    if key in tuple_space:
                        response_body = f"OK ({key}, {tuple_space[key]}) read"
                    else:
                        sta['total_errors'] += 1
                        response_body = f"ERR {key} does not exist"
                elif cmd == 'G':
                    sta['total_gets'] += 1
                    if key in tuple_space:
                        pv = tuple_space.pop(key)
                        response_body = f"OK ({key}, {pv}) removed"
                    else:
                        response_body = f"ERR {key} does not exist"
                elif cmd == 'P':
                    sta['total_puts'] += 1
                    if key in tuple_space:
                        sta['total_errors'] += 1
                        response_body = f"ERR {key} already exists"
                    else:
                        tuple_space[key] = val
                        response_body = f"OK ({key}, {val}) added"

            response_len = len(response_body) + 4
            response = f"{response_len:03d} {response_body}"
            client_socket.sendall(response.encode('utf8'))

    print(f"Connection with {addr} closed.")

def start_server():
    host = 'localhost'
    port = 9090
    sta_thread = threading.Thread(target=print_server_sta, daemon=True)
    sta_thread.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Server is running and ready to accept multiple clients...")
