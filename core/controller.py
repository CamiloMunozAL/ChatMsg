from core.client import Client
from core.common import SERVER_IP, SERVER_PORT
import ftplib
import os

class ChatController:
    def __init__(self, gui, host=None, port=None):
        self.gui = gui
        # Cliente se conecta y envía mensajes a la GUI cuando recibe algo
        self.client = Client(host or SERVER_IP,
            port or SERVER_PORT,
            on_message=self._on_message)
        self.client.connect()

    def get_client(self):
        return self.client

    def send_message(self, msg):
        self.client.send_message(msg)

    def send_file(self, to_user, file_path):
        FTP_HOST="127.0.0.1"
        FTP_PORT=2121
        FTP_USER="user"
        FTP_PASS="12345"

        filename=os.path.basename(file_path)
        try:
            with ftplib.FTP() as ftp:
                ftp.connect(FTP_HOST, FTP_PORT)
                ftp.login(FTP_USER, FTP_PASS)
                with open(file_path, 'rb') as file:
                    ftp.storbinary(f'STOR {filename}', file)
            self.send_private_message(to_user, f"/file {filename}")
        except Exception as e:
            print(f"Error al enviar archivo: {e}")

    def send_file_global(self, file_path):
        FTP_HOST="127.0.0.1"
        FTP_PORT=2121
        FTP_USER="user"
        FTP_PASS="12345"

        filename=os.path.basename(file_path)
        try:
            with ftplib.FTP() as ftp:
                ftp.connect(FTP_HOST, FTP_PORT)
                ftp.login(FTP_USER, FTP_PASS)
                with open(file_path, 'rb') as file:
                    ftp.storbinary(f'STOR {filename}', file)
            self.send_message(f"/file {filename}")
        except Exception as e:
            print(f"Error al enviar archivo: {e}")

    def close(self):
        self.client.close()

    def _on_message(self, message):
        if message.startswith("[SERVIDOR]"):
            self.gui.display_message(message, sender="server")
        elif message.startswith("[PRIVADO de "):
            #extraer el id del remitente
            try:
                prefix = "[PRIVADO de "
                end_idx = message.find("]")
                from_id = message[len(prefix):end_idx]
                priv_msg= message[end_idx+2:]  # +2 para saltar "] "
                self.gui.display_private_message(from_id, priv_msg)
            except Exception:
                self.gui.display_message(message, sender="other") 
        elif message.startswith("Tú:"):
            self.gui.display_message(message, sender="self")
        elif message.startswith(f"[{self.client.get_identifier()}"):
            print("Mensaje enviado por mí mismo, no se muestra en la GUI.")
        else:
            self.gui.display_message(message, sender="other")

    def get_connected_users(self):
        return self.client.get_connected_users()
    
    def send_private_message(self, to_user, message):
        self.client.send_private_message(to_user, message)

