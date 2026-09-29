import paramiko

def ssh_command(ip, port, user, password, cmd):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server
        client.connect(ip, port=port, username=user, passphrase=password)

        # Execute the command
        stdin, stdout, stderr = client.exec_command(cmd)

        # Print the output and error (if any)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))

        # Close the connection
        client.close()
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    ip = '10.0.2.15'
    port = 2222
    user = 'testuser'
    password = 'password'
    cmd = 'ls'
    ssh_command(ip, port, user, password, cmd)
