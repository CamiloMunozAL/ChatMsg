# clientHandler.py
# Manejador de clientes individuales desde el servidor
import threading
from common import send_line, recv_line
import json

class ClientHandler:
  """
  Clase que representa el manejador de un cliente conectado al servidor.
  Se encarga de recibir y procesar los mensajes de un cliente específico.
  """
  def __init__(self, client_socket, client_address, server):
    """
    Inicializa el handler con el socket, dirección y referencia al servidor.
    """
    self.client_socket = client_socket  # Socket del cliente
    self.client_address = client_address  # Dirección IP y puerto del cliente
    self.server = server  # Referencia al servidor principal
    self.identifier = None  # Identificador único del cliente
    self.username = None  # Nombre de usuario del cliente
    self.running = True  # Bandera para saber si el handler está activo

  def id(self):
    """
    Devuelve una cadena identificadora del cliente (nombre@ip:puerto).
    """
    return f"{self.username}@{self.client_address[0]}:{self.client_address[1]}" if self.username else f"{self.client_address[0]}:{self.client_address[1]}"

  def handle(self):
    """
    Maneja el ciclo principal de recepción y procesamiento de mensajes del cliente.
    """
    self.identifier = self.server.register_client(self)
    if not self.identifier:
      send_line(self.client_socket, '[SERVIDOR] No hay identificadores disponibles. Conexión rechazada.')
      self.client_socket.close()
      return
    send_line(self.client_socket, f'[SERVIDOR] Bienvenido! Tu identificador es {self.identifier}.')
    self.username = recv_line(self.client_socket)
    if self.username is None:
      self.close()
      return

    # Notificar a todos que un nuevo usuario se ha unido
    self.server.broadcast(f'[SERVIDOR] {self.username} se ha unido al chat.', exclude_handler=self)

    while self.running:
      message = recv_line(self.client_socket)
      if message is None:
        break
      if message.startswith('/salir'):
        self.close()
        break
      elif message.startswith('/users'):
        # Enviar lista de usuarios conectados
        users=[
          {"id": id, "username": handler.username or ""}
          for id, handler in self.server.clients.items()
        ]
        send_line(self.client_socket, "/users " + json.dumps(users))
      elif message.startswith('/priv '):
        # Mensaje privado a otro usuario
        parts = message.split(' ', 2)
        if len(parts) < 3:
          send_line(self.client_socket, '[SERVIDOR] Uso incorrecto del comando /priv. Uso: /priv <identificador> <mensaje>')
        else:
          target_id, priv_message = parts[1], parts[2]
          self.server.send_private_message(self.identifier, target_id, priv_message)
      else:
        # Mensaje público al chat
        self.server.broadcast(f'[{self.identifier}:{self.username}] {message}', exclude_handler=self)
    self.close()

  def close(self):
    """
    Cierra la conexión del cliente y lo elimina del servidor.
    """
    if self.running:
      self.running = False
      self.server.unregister_client(self)
      try:
        self.client_socket.close()
      except Exception as e:
        print(f'[SERVIDOR] Error al cerrar el socket del cliente {self.id()}: {e}')
      self.server.broadcast(f'[SERVIDOR] {self.username} se ha desconectado.', exclude_handler=self)
    

