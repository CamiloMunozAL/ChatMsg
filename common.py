#common.py
"""
Funciones de utilidad para el proyecto. y comundes

"""
SERVER_IP='192.168.0.13'
SERVER_PORT=5000

def send_line(sock, line):
  """Envía una línea a través del socket, asegurando que termina con un salto de línea."""
  if not line.endswith('\n'):
    line += '\n'
  sock.sendall(line.encode('utf-8'))


def recv_line(sock):
  # Recibir hasta saltar de línea
  buffer =[]
  while True:
    try:
      char = sock.recv(1).decode('utf-8') # aqui se recibe byte a byte
    except ConnectionResetError:
      return None
    if not char:
      return None
    if char == '\n':
      break
    buffer.append(char)
  return ''.join(buffer) # Unir la lista de caracteres en una cadena y devolverla