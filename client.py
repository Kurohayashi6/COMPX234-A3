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

    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((hostname, port))

        for line in lines:
            line = line.strip()

            parts = line.split(' ', 2)
            cmd = parts[0]
            key = parts[1] if len(parts) > 1 else ""
            val = parts[2] if len(parts) > 2 else ""

            if cmd == 'PUT':
                collated_size = len(f"{key} {val}")
                if collated_size > 970:
                    print(f"Error: collated size exceeds 970 characters for line: {line}.")
                    continue

            if cmd == 'PUT':
                body = f"P {key} {val}"
            elif cmd == 'GET':
                body = f"G {key}"
            elif cmd == 'READ':
                body = f"R {key}"
            else:
                print(f"Error: Unknown command {cmd}")
                continue

            msg = f"{len(body) + 4:03d} {body}"
            client_socket.sendall(msg.encode('utf-8'))

            nnn = recvall(client_socket, 3)
            response = recvall(client_socket, int(nnn) - 3)
            print(f"{line}:{response}")
    except Exception as e:
        print(f"Error for {filename}: {e}")

    finally:
        if client_socket:
            client_socket.close()

def main(m):
    clients = []
    for i in range(m):
        t = threading.Thread(target=client_task, args=(f"test-workload/client_{i + 1}.txt",))
        clients.append(t)
        t.start()
        time.sleep(0.1)
    for t in clients:
        t.join()


if __name__ == "__main__":
    n = input("Enter the number of clients: ")
    main(int(n))
    sys.exit(0)

