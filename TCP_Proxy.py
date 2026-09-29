import socket
import threading

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        results = []
        for i in range(0, len(src), length):
            word = src[i:i+length]
            hexa = ' '.join([f'{b:02X}' for b in word])
            printable = ''.join([chr(b) if 32 <= b < 127 else '.' for b in word])
            results.append(f'{i:04x}  {hexa:<{length*3}}  {printable}')
        if show:
            for line in results:
                print(line)
        else:
            return results
    else:
        raise ValueError("Input must be bytes.")


def forward_data(src_socket, dest_socket):
    try:
        while True:
            data = src_socket.recv(4096)
            if not data:
                break
            dest_socket.sendall(data)
            hexdump(data)  # Optional: Print hex dump of data being forwarded
    except Exception as e:
        print(f"Forwarding error: {e}")
    finally:
        src_socket.close()
        dest_socket.close()
    print("Connection closed")


def handle_client(client_socket, remote_host, remote_port):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        
        client_thread = threading.Thread(target=forward_data, args=(client_socket, remote_socket))
        remote_thread = threading.Thread(target=forward_data, args=(remote_socket, client_socket))
        
        client_thread.start()
        remote_thread.start()
        
        client_thread.join()
        remote_thread.join()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def simple_proxy(local_host, local_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))
    server.listen(5)
    print(f"Listening on {local_host}:{local_port}")

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"Received incoming connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port))
            client_handler.start()
        except Exception as e:
            print(f"Accept error: {e}")


if __name__ == "__main__":
    simple_proxy('10.0.2.15', 2223, '10.0.2.15', 2121)
