#common.py
"""
Funciones de utilidad para el proyecto. y comundes

"""
SERVER_IP='127.0.0.1'
SERVER_PORT=5050

def send_line(sock, line):
  """Envía una línea a través del socket, asegurando que termina con un salto de línea."""
  if not line.endswith('\n'):
    line += '\n'
  sock.sendall(line.encode('utf-8'))

def recv_line(sock):
    """
    Recibe datos del socket hasta encontrar un salto de línea (\n).
    Decodifica la línea completa como UTF-8, soportando caracteres especiales.
    """
    buffer = bytearray()
    while True:
        try:
            char = sock.recv(1)
        except ConnectionResetError:
            return None
        if not char:
            return None
        buffer += char
        if char == b'\n':
            break
    try:
        return buffer.decode('utf-8').rstrip('\r\n')
    except UnicodeDecodeError:
        return None