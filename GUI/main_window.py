import tkinter as tk
from tkinter import scrolledtext

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("ChatMsg - Global Chat")
        self.geometry("500x400")

        # Frame principal
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state="disabled", height=20)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.tag_configure("server", foreground="blue", justify="center", lmargin1=100, lmargin2=100, rmargin=100)
        self.chat_area.tag_configure("self", foreground="green", justify="right")
        self.chat_area.tag_configure("other", foreground="black", justify="left")

        # Frame inferior (entrada + botón)
        bottom_frame = tk.Frame(frame)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        # Entrada de texto
        self.msg_entry = tk.Entry(bottom_frame)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Botón enviar
        self.send_btn = tk.Button(bottom_frame, text="Enviar", command=self._on_send)
        self.send_btn.pack(side=tk.RIGHT)

    def _on_send(self):
        msg = self.msg_entry.get().strip()
        if msg:
            self.controller.send_message(msg)
            self.display_message(f"Tú: {msg}", sender="self")
            self.msg_entry.delete(0, tk.END)


    def display_message(self, message, sender="other"):
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, f"{message}\n", sender)
        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)


        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)
