#server.py
# server.py
# Servidor principal que gestiona los clientes y la comunicación en el chat distribuido
import socket
import threading
from core.common import send_line, recv_line, SERVER_IP, SERVER_PORT
from core.clientHandler import ClientHandler

class ChatServer:
  """
  Clase que representa el servidor de chat.
  Se encarga de aceptar conexiones, gestionar clientes y enviar mensajes.
  """
  def __init__(self, host='localhost', port=5000):
    """
    Inicializa el servidor con la IP y puerto indicados.
    """
    self.host = host
    self.port = port
    self.identifiers = [f'c{i+1}' for i in range(100)]  # Lista de identificadores disponibles para clientes
    self.clients = {}  # Diccionario: identificador -> handler del cliente
    self.running = True  # Bandera para saber si el servidor está activo
    self.lock = threading.Lock()  # Lock para acceso seguro a la lista de clientes

  def start(self):
    """
    Inicia el servidor, acepta conexiones y lanza un hilo por cada cliente.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((self.host, self.port))
    server.listen()
    print(f'[SERVIDOR] El servidor está escuchando en {self.host}:{self.port}')

    while self.running:
      client_socket, client_address = server.accept()
      if not self.identifiers:
        print('[SERVIDOR] No hay identificadores disponibles. Rechazando conexión.')
        client_socket.close()
        continue
      handler = ClientHandler(client_socket, client_address, self)
      thread = threading.Thread(target=handler.handle, daemon=True)
      thread.start()

  def assign_identifier(self, handler):
    """
    Asigna un identificador único a un cliente nuevo.
    """
    with self.lock:
      for identifier in self.identifiers:
        if identifier not in self.clients:
          self.clients[identifier] = handler
          return identifier

  def register_client(self, handler):
    """
    Registra un cliente en el servidor y le asigna un identificador.
    """
    identifier = self.assign_identifier(handler)
    if identifier:
      print(f'[SERVIDOR] Cliente {handler.id()} registrado con identificador {identifier}')
    return identifier

  def unregister_client(self, handler):
    """
    Elimina un cliente de la lista de conectados.
    """
    with self.lock:
      for identifier, h in list(self.clients.items()):
        if h == handler:
          del self.clients[identifier]
          print(f'[SERVIDOR] Cliente {handler.id()} con identificador {identifier} desconectado')
          break

  def broadcast(self, message, exclude_handler=None):
    """
    Envía un mensaje a todos los clientes conectados.
    """
    print(f'[MENSAJE BROADCAST] {message}')
    with self.lock:
      for handler in self.clients.values():
        # Todos reciben el mensaje, incluido el remitente
        try:
          send_line(handler.client_socket, message)
        except Exception as e:
          print(f'[SERVIDOR] Error al enviar mensaje a {handler.id()}: {e}')

  def send_private_message(self, from_id, to_id, message):
    """
    Envía un mensaje privado de un cliente a otro.
    """
    with self.lock:
      target = self.clients.get(to_id)
      if target:
        print(f'[MENSAJE PRIVADO] de {from_id} a {to_id}: {message}')
        send_line(target.client_socket, f'[PRIVADO de {from_id}] {message}')
      else:
        sender = self.clients.get(from_id)
        if sender:
          send_line(sender.client_socket, f'[SERVIDOR] El usuario con identificador {to_id} no existe o no está conectado.')


# Punto de entrada principal del servidor
if __name__ == "__main__":
  chat_server = ChatServer(SERVER_IP, SERVER_PORT)
  chat_server.start()