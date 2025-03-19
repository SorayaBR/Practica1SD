import pika
import random
import time
import threading

insults = ["Tonto", "Canana", "Friki", "NPC", "Inútil"]
queue_name = "insult_queue"
exchange_name = "insult_exchange"

print("Insult Client (RabbitMQ) is running...")

def send_insults():
    """Crea una nueva conexión y canal, y envía insultos cada 3 segundos"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)

    while True:
        insult = random.choice(insults)
        channel.basic_publish(exchange='', routing_key=queue_name, body=insult)
        print(f"Sent insult: {insult}")
        time.sleep(3)

def receive_insults():
    """Crea una nueva conexión y canal, y escucha insultos desde el broadcast"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    # Declarar el exchange de broadcast
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

    # Crear una cola temporal exclusiva para cada receptor
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name_broadcast = result.method.queue

    # Vincular la cola al exchange para recibir insultos
    channel.queue_bind(exchange=exchange_name, queue=queue_name_broadcast)

    def callback(ch, method, properties, body):
        print(f"Received broadcast insult: {body.decode()}")

    channel.basic_consume(queue=queue_name_broadcast, on_message_callback=callback, auto_ack=True)

    print(f"Listening for broadcast insults from {exchange_name}...")
    channel.start_consuming()

# Iniciar hilos separados con su propia conexión
threading.Thread(target=send_insults, daemon=True).start()
threading.Thread(target=receive_insults, daemon=True).start()

# Mantener el programa activo
while True:
    time.sleep(1)
