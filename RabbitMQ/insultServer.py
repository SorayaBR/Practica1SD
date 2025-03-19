import random
import pika
import redis
import time
import threading

# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Configurar RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar la cola de insultos (para recibir insultos)
queue_name = "insult_queue"
channel.queue_declare(queue=queue_name)

# Declarar el exchange de broadcast (para enviar insultos a suscriptores cada 5s)
exchange_name = "insult_exchange"
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

insult_list = "INSULTS"

print("InsultService (RabbitMQ) is running...")

def store_insults():
    """Recibe insultos y los almacena en Redis (evitando duplicados)"""
    def callback(ch, method, properties, body):
        insult = body.decode()
        existing_insults = client.lrange(insult_list, 0, -1)

        if insult not in existing_insults:
            client.rpush(insult_list, insult)
            print(f"Insult stored: {insult}")
        else:
            print(f"Duplicate insult ignored: {insult}")

        ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirmar mensaje procesado

    # Configurar consumidor
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("Waiting for insults...")
    channel.start_consuming()

def broadcast_insults():
    """Publica un insulto aleatorio cada 5 segundos"""
    while True:
        insults = client.lrange(insult_list, 0, -1)
        if insults:
            insult = random.choice(insults)  # Seleccionar un insulto aleatorio
            channel.basic_publish(exchange=exchange_name, routing_key='', body=insult)
            print(f"Broadcasted insult: {insult}")
        time.sleep(5)  # Espera 5 segundos antes de la próxima publicación

def get_insults():
    """Devuelve la lista completa de insultos almacenados en Redis"""
    return client.lrange(insult_list, 0, -1)

# Iniciar ambas funciones en hilos separados
threading.Thread(target=store_insults, daemon=True).start()
#threading.Thread(target=broadcast_insults, daemon=True).start()

# Mantener el programa en ejecución
while True:
    time.sleep(1)
