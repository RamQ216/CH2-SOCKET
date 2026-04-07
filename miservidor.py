import socket#libreria para crear los sockets
import threading#libreria para crear los hilos

HOST = "0.0.0.0"#nuestra direccion IP en la red, 0.0.0.0 escucha en todas las interfaces
PORT = 55555#nuestro puerto para acceder al servicio

SERVIDOR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#af_inet familia de direcciones tipo ipv4 y protoclo tcp 
SERVIDOR.bind((HOST, PORT))#vinculamos con el socket la ip y el puerto
SERVIDOR.listen()#haces que escuch o mejor dicho que espere conexiones

CONECTADOS = []#aqui se encontraran los clientes conectados

def chat_global(mensaje, emisor):
    # Usamos una copia de la lista para evitar errores si alguien se desconecta justo ahora
    for usuario in list(CONECTADOS):#creamo una copia superficial para un beun manejo de rrores
        try:
            # Enviamos a todos excepto a quien lo envió (opcional)
            if usuario != emisor:
                usuario.send(mensaje) 
        except:
            # Si falla el envío, detectamos que el socket está MUERTO
            eliminar_usuario(usuario)

def eliminar_usuario(usuario):#cuando un cliente se desconecta, lo eliminamos de la lista de conectados y cerramos su socket
    if usuario in CONECTADOS:
        CONECTADOS.remove(usuario)
        usuario.close()
        print("¡Un cliente se fue! Lista actualizada.")

def atencion_cliente(usuario):#funcion que se ejecuta en un hilo para cada cliente conectado, se encarga de recibir mensajes y enviarlos a los demas clientes
    while True:
        try:
            mensaje = usuario.recv(1024)#blocking, espera a recibir un mensaje del cliente, el 1024 es el tamaño del buffer
            if not mensaje: # Si recibimos un mensaje vacío, el cliente se desconectó
                raise Exception("Cliente desconectado")#lanzamos una excepción para salir del bucle y manejar la desconexión
            chat_global(mensaje, usuario)
        except:
            # Manejamos la desconexión con elegancia
            eliminar_usuario(usuario)
            break

#obs= el servidor no tiene daemon para siempre este activo, esto maneja la multiples conexiones de clientes
def iniciar():
    print("SERVIDOR ESTABLE CORRIENDO...")
    while True:
        try:
            usuario, ubi = SERVIDOR.accept()#el socket del cliente y puerto e IP
            CONECTADOS.append(usuario)
            thread = threading.Thread(target=atencion_cliente, args=(usuario,))#le damos al hilo una funcion y su argumento
            thread.start()#iniciamos el hilo para atender al cliente
        except Exception as e:
            print(f"Error aceptando conexión: {e}")

iniciar()#iniciamos el servidor y comenzamos a aceptar conexiones de clientes