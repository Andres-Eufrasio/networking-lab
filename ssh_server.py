import paramiko
import socket
import threading
import subprocess
import sys

# Set up logging
paramiko.util.log_to_file("ssh_server.log")

# Define the server host key
host_key = paramiko.RSAKey(filename="/etc/ssh/ssh_host_rsa_key", password="password")

# Create a handler class for SSH commands
class SSHServerHandler(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "testuser" and password == "password":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        # Implement public key authentication if needed
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_exec_request(self, channel, command):
        try:
            output = subprocess.check_output(command, shell=True)
            channel.send(output)
        except Exception as e:
            channel.send(f"Failed to execute command: {str(e)}")
        channel.close()
        return True

# Set up the server
def start_ssh_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 2222))
    server_socket.listen(100)
    
    print("SSH Server listening on port 2222...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        ssh_transport = paramiko.Transport(client_socket)
        ssh_transport.add_server_key(host_key)
        
        server = SSHServerHandler()
        try:
            ssh_transport.start_server(server=server)
        except paramiko.SSHException as e:
            print(f"SSH negotiation failed: {str(e)}")
            continue

        channel = ssh_transport.accept()
        if channel is None:
            print("No channel.")
            continue

        print("Authenticated!")

        while True:
            try:
                command = channel.recv(1024).decode("utf-8")
                if not command:
                    break
                print(f"Received command: {command}")
                if command.strip() == "exit":
                    print("Client disconnected")
                    break
                output = subprocess.check_output(command, shell=True)
                channel.send(output)
            except Exception as e:
                print(f"Exception: {str(e)}")
                channel.send(f"Error: {str(e)}\n")
        channel.close()
        ssh_transport.close()

if __name__ == "__main__":
    start_ssh_server()

        
        
        