## Consola principal para interactuar con el chat distribuido y el servidor FTP.
## Permite enviar mensajes, subir/descargar/listar archivos por FTP y gestionar el usuario.
from client import Client
from common import SERVER_IP, SERVER_PORT, send_line
from ftplib import FTP

def main():
    """
    Función principal que inicia el cliente, gestiona el login y los comandos de usuario.
    """
    client = Client(SERVER_IP, SERVER_PORT)
    client.connect()

    # Solicitar nombre de usuario y enviarlo al servidor
    username = input("Ingresa tu nombre de usuario: ")
    client.set_username(username)
    send_line(client.socket, username)

    # Configuración del servidor FTP
    FTP_HOST = 'localhost'  # Cambia si tu servidor FTP está en otra IP
    FTP_PORT = 2121
    FTP_USER = 'user'
    FTP_PASS = '12345'

    def enviar_ftp(ruta):
        """
        Sube un archivo al servidor FTP y notifica al chat.
        """
        try:
            with FTP() as ftp:
                ftp.connect(FTP_HOST, FTP_PORT)
                ftp.login(FTP_USER, FTP_PASS)
                nombre_archivo = ruta.split("/")[-1]
                with open(ruta, 'rb') as f:
                    ftp.storbinary(f'STOR {nombre_archivo}', f)
            print(f'[FTP] Archivo enviado: {ruta}')
            # Notificar a todos en el chat
            client.send_message(f"[FTP] El usuario {client.username} subió el archivo {nombre_archivo}")
        except Exception as e:
            print(f'[FTP] Error al enviar archivo: {e}')

    def descargar_ftp(nombre):
        """
        Descarga un archivo del servidor FTP.
        """
        try:
            with FTP() as ftp:
                ftp.connect(FTP_HOST, FTP_PORT)
                ftp.login(FTP_USER, FTP_PASS)
                with open(nombre, 'wb') as f:
                    ftp.retrbinary(f'RETR {nombre}', f.write)
            print(f'[FTP] Archivo descargado: {nombre}')
        except Exception as e:
            print(f'[FTP] Error al descargar archivo: {e}')

    def listar_ftp():
        """
        Lista los archivos disponibles en el servidor FTP.
        """
        try:
            with FTP() as ftp:
                ftp.connect(FTP_HOST, FTP_PORT)
                ftp.login(FTP_USER, FTP_PASS)
                archivos = ftp.nlst()
            print('[FTP] Archivos en el servidor:')
            for a in archivos:
                print('  ', a)
        except Exception as e:
            print(f'[FTP] Error al listar archivos: {e}')

    # Bucle principal de la consola
    while client.running:
        message = input("> ")
        # Comando para salir del chat
        if message.lower() == "/salir":
            client.send_message("/salir")
            client.close()
            break
        # Comando para subir archivo por FTP
        elif message.startswith("/subir "):
            ruta = message.split(" ", 1)[1]
            enviar_ftp(ruta)
        # Comando para descargar archivo por FTP
        elif message.startswith("/descargar "):
            nombre = message.split(" ", 1)[1]
            descargar_ftp(nombre)
        # Comando para listar archivos por FTP
        elif message.strip() == "/listar":
            listar_ftp()
        # Cualquier otro mensaje se envía al chat
        else:
            client.send_message(message)

if __name__ == "__main__":
    main()
