from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


# The port the FTP server will listen on.
# This must be greater than 1023 unless you run this script as root.
FTP_PORT = 2121

# The name of the FTP user that can log in.
FTP_USER = "serdma"

# The FTP user's password.
FTP_PASSWORD = "password"

# The directory the FTP user will have full read/write access to.
FTP_DIRECTORY = "ftp_files"


def main():
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions.
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Set the specific IP address and port.
    address = ('10.0.2.15', FTP_PORT)  # Replace with your IP address
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()



if __name__ == '__main__':
    main()