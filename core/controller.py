from core.client import ChatClient

class ChatController:
    def __init__(self, gui):
        self.gui = gui
        self.client = ChatClient(on_message=self.gui.display_message)

    def send_message(self, msg):
        self.client.send(msg)