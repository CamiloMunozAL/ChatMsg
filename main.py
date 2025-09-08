from GUI.main_window import MainWindow
from core.controller import ChatController
import tkinter as tk
from tkinter import simpledialog

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal mientras se pide el nombre de usuario
    username = simpledialog.askstring("Nombre de usuario", "Por favor, ingresa tu nombre de usuario:", parent=root)
    app= MainWindow(controller=None)
    controller= ChatController(app)
    app.controller= controller
    controller.client.set_username(username)
    controller.client.send_message(username)  # Envía el nombre de usuario al servidor
    app.title(f"Chat - {username}")
    app.mainloop()