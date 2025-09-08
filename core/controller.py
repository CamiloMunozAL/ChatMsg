from core.client import Client
from core.common import SERVER_IP, SERVER_PORT

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
        else:
            self.gui.display_message(message, sender="other")

    def get_connected_users(self):
        return self.client.get_connected_users()
    
    def send_private_message(self, to_user, message):
        self.client.send_private_message(to_user, message)

