import socket#libreria para crear los sockets
import threading#libreria para crear los hilos
import time

def conectar():
    while True:
        try:
            nuevo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creamos un socket con la familia de direcciones ipv4 y el protocolo tcp
            # Intentamos conectar
            nuevo_socket.connect(('127.0.0.1', 55555))#conectamos al servidor con la ip local y el puerto del servidor 
            print("[SISTEMA] ¡Conexión establecida!")
            return nuevo_socket
        except:
            print("[SISTEMA] Servidor caído. Reintentando en 5 segundos...")
            time.sleep(5)

def buzon(cliente_actual):
    while True:
        try:
            mensaje = cliente_actual.recv(1024).decode('utf-8')#decode transforma el recv en str y utf-8 el estandar de codificacion de caracteres, el 1024 es el tamaño del buffer
            if not mensaje:
                raise Exception("Servidor cerrado")#para que no este esperando infinitamente
            print(f"\n{mensaje}")
        except:#si el servidor se cae o se cierra, lo detectamos y reiniciamos el cliente
            print("\n[!] El servidor se ha desconectado.")
            cliente_actual.close()
            reiniciar_cliente()
            break

def enviar(cliente_actual):#funcion para enviar mensajes al servidor, se ejecuta en el hilo principal
    while True:
        try:
            texto = input("CHAT:")#input es bloqueante, espera a que el usuario escriba algo y presione enter
            cliente_actual.send(f"{NOMBRE}: {texto}".encode('utf-8'))
        except:
          
            break

def reiniciar_cliente():#si el servidor se cae, reiniciamos el cliente para que intente reconectar
    global CLIENTE
    CLIENTE = conectar()


NOMBRE = input("TU NOMBRE: ")
CLIENTE = conectar()
#el hilo de cliente si tiene daemnon para que no se queden los procesos colgando y tener un cierre limpio
threading.Thread(target=buzon, args=(CLIENTE,), daemon=True).start()#iniciamos un hilo para escuchar los mensajes del servidor, el daemon=True hace que el hilo se cierre cuando el programa principal termine

enviar(CLIENTE)#iniciamos la funcion de enviar mensajes al servidor en el hilo principal, esto es porque el input es bloqueante y no queremos que el hilo de buzon se quede esperando a que el usuario escriba algo para mostrar los mensajes del servidor