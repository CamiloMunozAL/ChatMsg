import tkinter as tk
from tkinter import scrolledtext, filedialog
import ftplib
import os

class MainWindow(tk.Tk):
    """
    Ventana principal de la aplicación de chat.
    Permite enviar mensajes y archivos tanto al chat global como a chats privados.
    Muestra la lista de usuarios conectados y gestiona ventanas de chat privado.
    """
    def __init__(self, controller):
        """
        Inicializa la ventana principal y todos sus componentes gráficos.
        :param controller: Controlador principal de la aplicación (ChatController)
        """
        super().__init__()
        self.controller = controller
        self.title("ChatMsg - Global Chat")
        self.geometry("500x400")

        # Frame principal que contiene todo
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Panel lateral muestra la lista de usuarios conectados
        self.user_frame= tk.Frame(frame, width=100, bg="#abdefc")
        self.user_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self.user_frame, text="Usuarios", bg="#abdefc").pack(pady=5)
        self.users_listbox = tk.Listbox(self.user_frame)
        self.users_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.users_listbox.bind("<Double-1>", self._on_user_double_click)
        self.private_chats = {} # diccionario user_id -> {'window': ventana, 'chat_area': chat_area}

        # Área de chat global mensajes y archivos
        self.chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state="disabled", height=20)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.tag_configure("server", foreground="blue", justify="center", lmargin1=100, lmargin2=100, rmargin=100)
        self.chat_area.tag_configure("self", foreground="green", justify="right")
        self.chat_area.tag_configure("other", foreground="black", justify="left")

        # Frame inferior entrada de texto y botones de enviar
        bottom_frame = tk.Frame(frame)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        # Entrada de texto para mensajes globales
        self.msg_entry = tk.Entry(bottom_frame)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Botón enviar mensaje global
        self.send_btn = tk.Button(bottom_frame, text="Enviar", command=self._on_send)
        self.send_btn.pack(side=tk.RIGHT)

        # Botón enviar archivo global
        def enviar_archivo_global():
            file_path=filedialog.askopenfilename()
            if file_path:
                self.controller.send_file_global(file_path)
                self.display_message(f"Tú enviaste un archivo: {os.path.basename(file_path)}", sender="self")
        self.file_btn_global = tk.Button(bottom_frame, text="Enviar Archivo Global", command=enviar_archivo_global)
        self.file_btn_global.pack(side=tk.RIGHT, padx=5)

        # Actualizar lista de usuarios cada segundo
        self.after_id=self.after(1000, self.update_user_list)

        # Manejar cierre de ventana principal
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _on_send(self):
        """
        Envía el mensaje escrito en la entrada de texto al chat global.
        """
        msg = self.msg_entry.get().strip()
        if msg:
            self.controller.send_message(msg)
            self.display_message(f"Tú: {msg}", sender="self")
            self.msg_entry.delete(0, tk.END)


    def display_message(self, message, sender="other"):
        """
        Muestra un mensaje en el área de chat global.
        Si el mensaje es un archivo, muestra un botón para descargarlo.
        :param message: Texto del mensaje
        :param sender: Etiqueta del remitente ("self", "other", "server")
        """
        self.chat_area.configure(state="normal")
        # si el mensaje es un archivo, mostrar botón descargar
        if message.startswith("Tú enviaste un archivo:") or "/file " in message:
            filename = message.split(" ",1)[1]
            def descargar():
                """
                Descarga el archivo desde el servidor FTP y lo guarda donde el usuario indique.
                """
                save_path = filedialog.asksaveasfilename(initialfile=filename)
                if save_path:
                    FTP_HOST="127.0.0.1"
                    FTP_PORT=2121
                    FTP_USER="user"
                    FTP_PASS="12345"
                    try:
                        with ftplib.FTP() as ftp:
                            ftp.connect(FTP_HOST, FTP_PORT)
                            ftp.login(FTP_USER, FTP_PASS)
                            with open(save_path, 'wb') as file:
                                ftp.retrbinary(f'RETR {filename}', file.write)
                        self.chat_area.insert(tk.END, f"Archivo '{filename}' descargado y guardado en: {save_path}\n", "other")
                    except Exception as e:
                        print(f"Error al descargar archivo: {e}")
            btn=tk.Button(self.chat_area, text=f"Descargar archivo: {filename}", command=descargar)
            self.chat_area.window_create(tk.END, window=btn)
            self.chat_area.insert(tk.END, "\n")
        else:
            self.chat_area.insert(tk.END, f"{message}\n", sender)
        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)

    def display_private_message(self, from_id,message):
        """
        Muestra un mensaje en la ventana de chat privado correspondiente.
        Si el mensaje es un archivo, muestra un botón para descargarlo.
        :param from_id: ID del remitente
        :param message: Texto del mensaje
        """
        if from_id not in self.private_chats:
            self.open_private_chat(from_id)
        chat_area = self.private_chats[from_id]['chat_area']
        chat_area.configure(state="normal")
        if message.startswith("/file "):
            filename = message.split(" ",1)[1]
            def descargar():
                """
                Descarga el archivo desde el servidor FTP y lo guarda donde el usuario indique.
                """
                save_path = filedialog.asksaveasfilename(initialfile=filename)
                if save_path:
                    FTP_HOST="127.0.0.1"
                    FTP_PORT=2121
                    FTP_USER="user"
                    FTP_PASS="12345"

                    try:
                        with ftplib.FTP() as ftp:
                            ftp.connect(FTP_HOST, FTP_PORT)
                            ftp.login(FTP_USER, FTP_PASS)
                            with open(save_path, 'wb') as file:
                                ftp.retrbinary(f'RETR {filename}', file.write)
                        chat_area.insert(tk.END, f"Archivo '{filename}' descargado y guardado en: {save_path}\n", "other")
                    except Exception as e:
                        print(f"Error al descargar archivo: {e}")
            btn=tk.Button(chat_area, text=f"Descargar archivo: {filename}", command=descargar)
            chat_area.window_create(tk.END, window=btn)
            chat_area.insert(tk.END, "\n")
        else:
            chat_area.insert(tk.END, f"{from_id}: {message}\n", "other")
        chat_area.configure(state="disabled")
        chat_area.see(tk.END)

    def update_user_list(self):
        """
        Actualiza la lista de usuarios conectados en la interfaz.
        """
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
        """
        Abre una ventana de chat privado al hacer doble clic en un usuario de la lista.
        """
        selection = self.users_listbox.curselection()
        if selection:
            idx= selection[0]
            user= self.filtered_users[idx]
            user_id= user['id']
            self.open_private_chat(user_id)


    
    def open_private_chat(self, user_id):
        """
        Abre una ventana de chat privado con el usuario especificado.
        Si ya existe, la trae al frente.
        :param user_id: ID del usuario con el que se chatea
        """
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
            """
            Envía un mensaje privado al usuario y lo muestra en la ventana.
            """
            msg = entry.get()
            self.controller.send_private_message(user_id, msg)
            chat_area.configure(state="normal")
            chat_area.insert(tk.END, f"Tú: {msg}\n", "self")
            chat_area.configure(state="disabled")
            entry.delete(0, tk.END)
        send_btn = tk.Button(chat_window, text="Enviar", command=enviar)
        send_btn.pack(side=tk.RIGHT, padx=10, pady=5)


        def enviar_archivo():
            """
            Abre un diálogo para seleccionar un archivo y lo envía por FTP al usuario privado.
            """
            file_path=filedialog.askopenfilename()
            if file_path:
                self.controller.send_file(user_id,file_path)
                chat_area.configure(state="normal")
                chat_area.insert(tk.END, f"Tú enviaste un archivo: {os.path.basename(file_path)}\n", "self")
                chat_area.configure(state="disabled")
        file_btn = tk.Button(chat_window, text="Enviar Archivo", command=enviar_archivo)
        file_btn.pack(side=tk.RIGHT, padx=10, pady=5)

        self.private_chats[user_id] = {'window': chat_window, 'chat_area': chat_area}

        def on_close():
            """
            Cierra la ventana de chat privado y elimina la referencia.
            """
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
        """
        Maneja el cierre de la ventana principal: detiene actualizaciones y cierra la app.
        """
        if self.after_id:
            self.after_cancel(self.after_id)
        self.controller.close()
        self.destroy()