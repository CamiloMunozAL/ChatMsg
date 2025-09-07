import tkinter as tk
from tkinter import scrolledtext

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ChatMsg - Global Chat")
        self.geometry("500x400")

        # Frame principal
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state="disabled", height=20)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

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
        msg = self.msg_entry.get()
        if msg.strip():
            self.display_message(f"Tú: {msg}")
            self.msg_entry.delete(0, tk.END)

    def display_message(self, msg):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)
