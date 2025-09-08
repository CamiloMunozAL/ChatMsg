#client.py
# client.py
# Clase que define el comportamiento del cliente en el chat distribuido
import socket
import threading
import json
from core.common import send_line, recv_line, SERVER_IP, SERVER_PORT

class Client:
  """
  Clase que representa un cliente que se conecta al servidor de chat.
  Permite enviar y recibir mensajes, así como gestionar el nombre de usuario y la conexión.
  """
  def __init__(self, host=SERVER_IP, port=SERVER_PORT,on_message=None):
    """
    Inicializa el cliente con la dirección y puerto del servidor.
    """
    self.host = host  # Dirección IP o nombre del servidor
    self.port = port  # Puerto del servidor
    self.socket = None  # Socket para la conexión
    self.running = False  # Bandera para saber si el cliente está activo
    self.username = None  # Nombre de usuario del cliente
    self.on_message = on_message  # callback hacia GUI
    self.connected_users = []  # Lista de usuarios conectados

  def connect(self):
    """
    Conecta el cliente al servidor y lanza un hilo para recibir mensajes.
    """
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.host, self.port))
    print(f'[CLIENTE] Conectado al servidor en {self.host}:{self.port}')
    print('Comandos: /salir, /priv <id> <mensaje>, /users')
    self.running = True
    # Iniciar hilo para recibir mensajes del servidor
    thread = threading.Thread(target=self.receive_messages, daemon=True)
    thread.start()

  def receive_messages(self):
    """
    Hilo que recibe mensajes del servidor y los muestra por pantalla.
    """
    while self.running:
      message = recv_line(self.socket)
      if message is None:
        print('[CLIENTE] Conexión cerrada por el servidor.')
        self.running = False
        break

      if message.startswith("/users "):
        try: 
          users_json = message[len("/users "): ]
          self.connected_users = json.loads(users_json)
        except Exception as e:
          print(f'[CLIENTE] Error al parsear la lista de usuarios: {e}')
        continue

      if self.on_message:
        self.on_message(message)
      print(f'\n{message}\n> ', end='', flush=True)

  def send_message(self, message):
    """
    Envía un mensaje al servidor.
    """
    if self.socket:
      send_line(self.socket, message)

  def send_private_message(self, user_id, message):
    """
    Envía un mensaje privado a otro usuario.
    """
    if self.socket:
      self.send_message(f'/priv {user_id} {message}')

  def set_username(self, username):
    """
    Asigna el nombre de usuario al cliente.
    """
    self.username = username

  def close(self):
    """
    Cierra la conexión del cliente con el servidor.
    """
    self.running = False
    if self.socket:
      self.socket.close()
      print(f'[CLIENTE:{self.username}] Conexión cerrada.')

  def get_users(self):
    """
    Solicita al servidor la lista de usuarios conectados.
    """
    self.send_message('/users')

  def get_connected_users(self):
      # Envía un comando especial al servidor y espera la lista
      self.send_message("/users")
      # Aquí deberías esperar la respuesta del servidor y devolver la lista
      # Por simplicidad, puedes mantener una lista local actualizada con los mensajes del servidor
      return self.connected_users
