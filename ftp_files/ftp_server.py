# ftp_server.py
# Servidor FTP simple para pruebas de chat
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Configuración básica
FTP_USER = 'user'
FTP_PASSWORD = '12345'
FTP_DIRECTORY = './ftp_files'
FTP_PORT = 2121

if __name__ == '__main__':
    import os
    os.makedirs(FTP_DIRECTORY, exist_ok=True)
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('0.0.0.0', FTP_PORT), handler)
    print(f'Servidor FTP escuchando en puerto {FTP_PORT} (usuario: {FTP_USER}, pass: {FTP_PASSWORD})')
    server.serve_forever()
