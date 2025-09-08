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

        # Panel lateral (usuarios)
        self.user_frame= tk.Frame(frame, width=100, bg="#abdefc")
        self.user_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self.user_frame, text="Usuarios", bg="#abdefc").pack(pady=5)
        self.users_listbox = tk.Listbox(self.user_frame)
        self.users_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.users_listbox.bind("<Double-1>", self._on_user_double_click)
        self.private_chats = {}

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

        # Actualizar lista de usuarios cada 100 milisegundos
        self.after_id=self.after(1000, self.update_user_list)

        # Manejar cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.on_close)

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

    def display_private_message(self, from_id,message):
        if from_id not in self.private_chats:
            self.open_private_chat(from_id)
        chat_area = self.private_chats[from_id]['chat_area']
        chat_area.configure(state="normal")
        chat_area.insert(tk.END, f"{from_id}: {message}\n", "other")
        chat_area.configure(state="disabled")
        chat_area.see(tk.END)

    def update_user_list(self):
        users = self.controller.get_connected_users()
        my_id = None
        for user in users:
            if user['username'] == self.controller.client.username:
                my_id = user['id']
                break
        self.filtered_users = [user for user in users if user['id'] != my_id]
        self.users_listbox.delete(0, tk.END)
        for user in self.filtered_users:
            display_name = f"{user['id']}: {user['username']}"
            self.users_listbox.insert(tk.END, display_name)
        self.after_id=self.after(1000, self.update_user_list)

    def _on_user_double_click(self, event):
        selection = self.users_listbox.curselection()
        if selection:
            idx= selection[0]
            user= self.filtered_users[idx]
            user_id= user['id']
            self.open_private_chat(user_id)


    
    def open_private_chat(self, user_id):
        if user_id in self.private_chats:
            try:
                self.private_chats[user_id].lift()
                return
            except tk.TclError:
                del self.private_chats[user_id]
        chat_window = tk.Toplevel(self)
        chat_window.title(f"Chat Privado con {user_id}")
        chat_window.geometry("400x300")
        chat_area = scrolledtext.ScrolledText(chat_window, wrap=tk.WORD, state="disabled", height=15)
        chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        chat_area.tag_configure("self", foreground="green", justify="right")
        chat_area.tag_configure("other", foreground="black", justify="left")

        entry = tk.Entry(chat_window)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)

        def enviar():
            msg = entry.get()
            self.controller.send_private_message(user_id, msg)
            chat_area.configure(state="normal")
            chat_area.insert(tk.END, f"Tú: {msg}\n", "self")
            chat_area.configure(state="disabled")
            entry.delete(0, tk.END)
        send_btn = tk.Button(chat_window, text="Enviar", command=enviar)
        send_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        self.private_chats[user_id] = {'window': chat_window, 'chat_area': chat_area}

        def on_close():
            del self.private_chats[user_id]
            chat_window.destroy()
        chat_window.protocol("WM_DELETE_WINDOW", on_close)

    def _on_send(self):
        msg = self.msg_entry.get().strip()
        if msg:
            self.controller.send_message(msg)
            self.display_message(f"Tú: {msg}", sender="self")
            self.msg_entry.delete(0, tk.END)

    def on_close(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.controller.close()
        self.destroy()