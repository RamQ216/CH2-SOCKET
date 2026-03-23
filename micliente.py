import socket
import threading
import time

def conectar():
    while True:
        try:
            nuevo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Intentamos conectar
            nuevo_socket.connect(('127.0.0.1', 55555))
            print("[SISTEMA] ¡Conexión establecida!")
            return nuevo_socket
        except:
            print("[SISTEMA] Servidor caído. Reintentando en 5 segundos...")
            time.sleep(5)

def buzon(cliente_actual):
    while True:
        try:
            mensaje = cliente_actual.recv(1024).decode('utf-8')
            if not mensaje:
                raise Exception("Servidor cerrado")
            print(f"\n{mensaje}")
        except:
            print("\n[!] El servidor se ha desconectado.")
            cliente_actual.close()
            reiniciar_cliente()
            break

def enviar(cliente_actual):
    while True:
        try:
            texto = input("CHAT:")
            cliente_actual.send(f"{NOMBRE}: {texto}".encode('utf-8'))
        except:
          
            break

def reiniciar_cliente():
    global CLIENTE
    CLIENTE = conectar()


NOMBRE = input("TU NOMBRE: ")
CLIENTE = conectar()

threading.Thread(target=buzon, args=(CLIENTE,), daemon=True).start()

enviar(CLIENTE)