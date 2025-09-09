# ChatMsg

**ChatMsg** es una aplicación de chat distribuido con soporte para mensajes públicos, privados y envío de archivos usando FTP. Está desarrollada en Python con una interfaz gráfica basada en Tkinter y un servidor de chat multicliente.

---

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Uso de la Aplicación](#uso-de-la-aplicación)
- [Comandos Disponibles](#comandos-disponibles)
- [Envío y Recepción de Archivos](#envío-y-recepción-de-archivos)
- [Notas de Desarrollo](#notas-de-desarrollo)
- [Licencia](#licencia)

---

## Características

- Chat global (todos los usuarios)
- Chat privado entre usuarios
- Lista de usuarios conectados en tiempo real
- Envío y descarga de archivos usando un servidor FTP integrado
- Interfaz gráfica intuitiva con Tkinter
- Servidor multicliente basado en hilos

---

## Requisitos

- Python 3.10 o superior
- Paquetes Python:
  - `pyftpdlib` (para el servidor FTP)
  - `tkinter` (incluido en la mayoría de instalaciones de Python)
- Sistema operativo: Windows, Linux o MacOS

Instala dependencias con:

```bash
pip install pyftpdlib
```

---

## Instalación

1. **Clona el repositorio o descarga los archivos** en una carpeta local.
2. Asegúrate de tener Python instalado y accesible desde la terminal.
3. Instala las dependencias necesarias (ver arriba).

---

## Ejecución

### 1. Inicia el servidor FTP

El servidor FTP es necesario para el envío y descarga de archivos.

```bash
python ftp_files/ftp_server.py
```

Esto iniciará el servidor FTP en el puerto `2121` con usuario `user` y contraseña `12345`.

### 2. Inicia el servidor de chat

En otra terminal, ejecuta:

```bash
python -m core.server
```

Esto iniciará el servidor de chat en el puerto `5050` (por defecto).

### 3. Inicia el cliente (interfaz gráfica)

En otra terminal, ejecuta:

```bash
python main.py
```

Puedes abrir varias instancias para simular varios usuarios.

---

## Arquitectura del Proyecto

```
chatmsg/
│
├── core/
│   ├── client.py           # Lógica del cliente
│   ├── clientHandler.py    # Manejador de clientes en el servidor
│   ├── common.py           # Funciones comunes (envío/recepción de mensajes)
│   ├── controller.py       # Controlador principal entre GUI y cliente
│   ├── server.py           # Servidor de chat
│   └── __init__.py
│
├── GUI/
│   ├── main_window.py      # Interfaz gráfica principal (Tkinter)
│   └── __init__.py
│
├── ftp_files/
│   └── ftp_server.py       # Servidor FTP para archivos
│
├── main.py                 # Punto de entrada del cliente
└── README.md
```

---

## Uso de la Aplicación

1. **Ingresa tu nombre de usuario** al iniciar el cliente.
2. **Chat global:** Escribe mensajes en la caja inferior y presiona "Enviar".
3. **Chat privado:** Haz doble clic en un usuario de la lista para abrir un chat privado.
4. **Enviar archivos:** Usa el botón "Enviar Archivo Global" para compartir archivos con todos, o "Enviar Archivo" en un chat privado para enviar archivos a un usuario específico.
5. **Descargar archivos:** Haz clic en el botón "Descargar archivo" que aparece junto a los mensajes de archivo.

---

## Comandos Disponibles

Puedes escribir estos comandos en el chat (además de usar la interfaz):

- `/salir`  
  Cierra la sesión y desconecta del servidor.

- `/users`  
  Muestra la lista de usuarios conectados.

- `/priv <id> <mensaje>`  
  Envía un mensaje privado al usuario con identificador `<id>`.

---

## Envío y Recepción de Archivos

- **Envío:**  
  Al pulsar "Enviar Archivo Global" o "Enviar Archivo" en un chat privado, selecciona el archivo a enviar. El archivo se sube al servidor FTP y se notifica a los usuarios.

- **Recepción:**  
  Cuando recibas un mensaje de archivo, aparecerá un botón "Descargar archivo: nombre.ext". Haz clic y elige dónde guardar el archivo.

- **Configuración FTP por defecto:**  
  - Host: `127.0.0.1`
  - Puerto: `2121`
  - Usuario: `user`
  - Contraseña: `12345`
  - Carpeta: `ftp_files/`

---

## Notas de Desarrollo

- El servidor y el cliente usan sockets TCP para la comunicación de mensajes.
- El envío de archivos se realiza por FTP para simplificar la transferencia y evitar bloquear el chat.
- Puedes modificar los puertos y credenciales en los archivos de configuración si lo necesitas.
- El sistema está pensado para pruebas y aprendizaje, no para producción.

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT.  
¡Siéntete libre de usarlo, modificarlo y compartirlo!

---

**Desarrollado por [Camilo Muñoz, Sergio Castellanos, Juan Pablo Medina]**