import redis
import sys

def produce_messages(num_messages):
    client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    queue_name = "work_queue"

    for i in range(num_messages):
        text = f"Insulto {i + 1}"
        client.rpush(queue_name, text)  # Enviar texto a la cola de trabajo

if __name__ == "__main__":
    num_messages = int(sys.argv[1])  # Obtener el número de mensajes desde los argumentos de la línea de comandos
    produce_messages(num_messages)