from core.client import Client
from core.common import SERVER_IP, SERVER_PORT

class ChatController:
    def __init__(self, gui, host=None, port=None):
        self.gui = gui
        # Cliente se conecta y envía mensajes a la GUI cuando recibe algo
        self.client = Client(host or SERVER_IP,
            port or SERVER_PORT,
            on_message=self.gui.display_message)
        self.client.connect()

    def send_message(self, msg):
        self.client.send_message(msg)

    def close(self):
        self.client.close()
