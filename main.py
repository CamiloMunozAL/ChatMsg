from GUI.main_window import MainWindow
from core.controller import ChatController

if __name__ == "__main__":
    app = MainWindow(controller=None)
    controller = ChatController(app)
    app.controller = controller
    app.mainloop()