import pika
import random
import time

# Conectar con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar la cola de trabajo
queue_name = "work_queue"
channel.queue_declare(queue=queue_name)

texts = ["Hola, eres un Tonto.", "Qué buen día.", "Eres un Canana.", "Vamos al cine?"]

print("Text Producer (RabbitMQ) is running...")

while True:
    text = random.choice(texts)
    channel.basic_publish(exchange='', routing_key=queue_name, body=text)
    print(f"Sent text: {text}")
    time.sleep(5)
