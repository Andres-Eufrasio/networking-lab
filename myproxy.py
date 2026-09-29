import socket
import threading




def port_forward(source_socket, destination_socket ):
    try:
        while True:
            data = source_socket.recv(4096)
            if not data:
                break
            destination_socket.sendall(data)
    except Exception as e: 
        print(e)
    finally:
        source_socket.close()
        destination_socket.close()
        print("sockets closed")




def handler(client_socket, remote_host, remote_port):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))

        remote_connection = threading.Thread(target=port_forward, args= (remote_socket, client_socket))
        client_connection = threading.Thread(target=port_forward, args= (client_socket, remote_socket))

        remote_connection.start()
        client_connection.start()

    except Exception as e:
        print(e)


def proxy(local_host, local_port, remote_host = '10.0.2.15', remote_port = 2121):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((local_host, local_port))
        server.listen(5)

        while True:
            client_socket, addr = server.accept()
            
            handle_client = threading.Thread(target=handler, args=(client_socket, remote_host, remote_port))
            handle_client.start()
    except Exception as e:
        print(e)
    finally:
        print("Proxy has closed")

        

if __name__ == '__main__':
    af = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    af.close()
    proxy('10.0.2.15',2225)