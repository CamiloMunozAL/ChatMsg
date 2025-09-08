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

    def send_message(self, msg):
        self.client.send_message(msg)

    def close(self):
        self.client.close()

    def _on_message(self, message):
        if message.startswith("[SERVIDOR]"):
            self.gui.display_message(message, sender="server")
        elif message.startswith("Tú:"):
            self.gui.display_message(message, sender="self")
        else:
            self.gui.display_message(message, sender="other")

