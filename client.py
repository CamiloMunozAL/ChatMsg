#client.py
# client.py
# Clase que define el comportamiento del cliente en el chat distribuido
import socket
import threading
from common import send_line, recv_line, SERVER_IP, SERVER_PORT

class Client:
  """
  Clase que representa un cliente que se conecta al servidor de chat.
  Permite enviar y recibir mensajes, así como gestionar el nombre de usuario y la conexión.
  """
  def __init__(self, host='localhost', port=5000):
    """
    Inicializa el cliente con la dirección y puerto del servidor.
    """
    self.host = host  # Dirección IP o nombre del servidor
    self.port = port  # Puerto del servidor
    self.socket = None  # Socket para la conexión
    self.running = False  # Bandera para saber si el cliente está activo
    self.username = None  # Nombre de usuario del cliente

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
      print(f'\n{message}\n> ', end='', flush=True)

  def send_message(self, message):
    """
    Envía un mensaje al servidor.
    """
    if self.socket:
      send_line(self.socket, message)

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


