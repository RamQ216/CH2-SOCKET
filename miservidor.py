import socket
import threading

HOST = "0.0.0.0"
PORT = 55555

SERVIDOR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVIDOR.bind((HOST, PORT))
SERVIDOR.listen()

CONECTADOS = []

def chat_global(mensaje, emisor):
    # Usamos una copia de la lista para evitar errores si alguien se desconecta justo ahora
    for usuario in list(CONECTADOS):
        try:
            # Enviamos a todos excepto a quien lo envió (opcional)
            if usuario != emisor:
                usuario.send(mensaje)
        except:
            # Si falla el envío, detectamos que el socket está MUERTO
            eliminar_usuario(usuario)

def eliminar_usuario(usuario):
    if usuario in CONECTADOS:
        CONECTADOS.remove(usuario)
        usuario.close()
        print("¡Un cliente se fue! Lista actualizada.")

def atencion_cliente(usuario):
    while True:
        try:
            mensaje = usuario.recv(1024)
            if not mensaje: # Si recibimos un mensaje vacío, el cliente se desconectó
                raise Exception("Cliente desconectado")
            chat_global(mensaje, usuario)
        except:
            # Manejamos la desconexión con elegancia
            eliminar_usuario(usuario)
            break

def iniciar():
    print("SERVIDOR ESTABLE CORRIENDO...")
    while True:
        try:
            usuario, ubi = SERVIDOR.accept()
            CONECTADOS.append(usuario)
            thread = threading.Thread(target=atencion_cliente, args=(usuario,))
            thread.start()
        except Exception as e:
            print(f"Error aceptando conexión: {e}")

iniciar()