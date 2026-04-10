import socket
import threading
import time

# Variables globales para que todas las funciones vean lo mismo
NOMBRE = input("TU NOMBRE: ")
CLIENTE = None

def buzon(socket_actual):
    """Esta función corre en un hilo aparte y solo escucha."""
    while True:
        try:
            # Esperamos mensaje del servidor
            mensaje = socket_actual.recv(1024).decode('utf-8')
            if not mensaje:
                break # Si no hay mensaje, el servidor se cerró
            print(f"\n{mensaje}")
        except:
            break # Si hay error, salimos del bucle para avisar
    
    print("\n[!] Conexión perdida con el servidor.")

def conectar_al_servidor():
    """Intenta conectar hasta que lo logre."""
    while True:
        try:
            nuevo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            nuevo_socket.connect(('127.0.0.1', 55555))
            print("[SISTEMA] ¡Conexión establecida!")
            return nuevo_socket
        except:
            print("[SISTEMA] Servidor no encontrado. Reintentando en 3 segundos...")
            time.sleep(3)

def flujo_principal():
    """Esta es la función que controla la vida del cliente."""
    global CLIENTE
    
    while True:
        # 1. Intentamos conectar
        CLIENTE = conectar_al_servidor()
        
        # 2. Creamos el hilo para recibir mensajes (Buzón)
        # IMPORTANTE: Pasamos el socket actual para que el hilo sepa cuál usar
        hilo_recibir = threading.Thread(target=buzon, args=(CLIENTE,), daemon=True)
        hilo_recibir.start()
        
        # 3. Bucle para enviar mensajes
        while True:
            try:
                texto = input("CHAT (Escribe algo): ")
                # Enviamos el mensaje
                CLIENTE.send(f"{NOMBRE}: {texto}".encode('utf-8'))
            except:
                # Si fallamos al enviar, significa que el socket murió
                print("[SISTEMA] Error al enviar. Reiniciando todo...")
                CLIENTE.close() #cerramos el socket muerto
                break # Rompe este bucle interno para volver a conectar arriba

# Arrancamos el programa
flujo_principal()

#solucion de reintentos
#fue gracias al  CLIENTE = conectar_al_servidor()
#Al estar dentro del bucle por cada conexion actualiza el puerto
#tambien crea un nuevo hilo