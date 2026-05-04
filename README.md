Sistema de Chat Sockets (TCP)
Este proyecto implementa una arquitectura Cliente-Servidor para comunicación en tiempo real utilizando Sockets de Python y manejo de concurrencia mediante hilos (threading).

Estructura del Sistema
1. Servidor (miservidor.py)
Actúa como el nodo central que gestiona las conexiones y distribuye el tráfico.

Concurrencia: Utiliza hilos para atender a múltiples clientes de forma simultánea.

Broadcast: Reenvía los mensajes recibidos a todos los usuarios conectados, excepto al emisor original.

Gestión de Errores: Detecta desconexiones de sockets "muertos" y limpia automáticamente la lista de usuarios activos.

2. Cliente (micliente.py)
Interfaz de usuario para el envío y recepción de mensajes.

Persistencia: Implementa una lógica de reconexión automática en caso de que el servidor se caiga.

Multitarea: Separa la recepción de mensajes (buzón) del envío de datos mediante un hilo en segundo plano (daemon).

Variable Global: Maneja el socket como variable global para facilitar el reinicio de puertos tras una desconexión.

Componente,Detalle

Protocolo,"TCP (AF_INET, SOCK_STREAM)"

IP/Puerto,127.0.0.1 / 55555

Codificación,UTF-8

Buffer,1024 bytes

Iniciar el servidor:
python miservidor.py
Conectar uno o más clientes:
python micliente.py


Iniciar el servidor:
