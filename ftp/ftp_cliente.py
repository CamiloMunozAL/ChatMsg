# ftp_cliente.py
from ftplib import FTP
import os

class FTPClient:
    def __init__(self, host='localhost', port=2121, user='user', password='12345'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def subir_archivo(self, ruta_local):
        nombre_archivo = os.path.basename(ruta_local)
        with FTP() as ftp:
            ftp.connect(self.host, self.port)
            ftp.login(self.user, self.password)
            with open(ruta_local, 'rb') as f:
                ftp.storbinary(f'STOR {nombre_archivo}', f)
        print(f"[FTP] Archivo subido: {nombre_archivo}")
        return nombre_archivo

    def descargar_archivo(self, nombre_archivo, ruta_destino):
        with FTP() as ftp:
            ftp.connect(self.host, self.port)
            ftp.login(self.user, self.password)
            with open(ruta_destino, 'wb') as f:
                ftp.retrbinary(f'RETR {nombre_archivo}', f.write)
        print(f"[FTP] Archivo descargado: {nombre_archivo} -> {ruta_destino}")

    def listar_archivos(self):
        with FTP() as ftp:
            ftp.connect(self.host, self.port)
            ftp.login(self.user, self.password)
            archivos = ftp.nlst()
        print("[FTP] Archivos disponibles:", archivos)
        return archivos