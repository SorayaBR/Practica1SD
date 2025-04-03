import pika
import sys
import random

# Conectar con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar la cola de trabajo
queue_name = "work_queue"
channel.queue_declare(queue=queue_name)

texts = ["Hola, eres un Tonto.", "Qué buen día.", "Eres un Canana.", "Vamos al cine?"]

def produce_messages(num_messages):
    print(f"Text Producer (RabbitMQ) is running and will send {num_messages} messages...")
    for i in range(num_messages):
        text = random.choice(texts)  # Elegir un texto aleatorio de la lista
        channel.basic_publish(exchange='', routing_key=queue_name, body=text)
        #print(f"Sent text: {text}")
    connection.close()

if __name__ == "__main__":
    num_messages = int(sys.argv[1])  # Obtener el número de mensajes desde los argumentos de la línea de comandos
    produce_messages(num_messages)