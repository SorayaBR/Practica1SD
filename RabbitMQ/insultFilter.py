import pika
import redis
import re

# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Configurar RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar la cola de trabajo
queue_name = "work_queue"
channel.queue_declare(queue=queue_name)

insult_list = "INSULTS"
result_list = "RESULTS"

print("InsultFilter (RabbitMQ) is running...")

def callback(ch, method, properties, body):
    text = body.decode()
    insults = client.lrange(insult_list, 0, -1)

    for insult in insults:
        text = re.sub(rf'\b{re.escape(insult)}\b', "CENSORED", text, flags=re.IGNORECASE)

    client.rpush(result_list, text)  # Guardar texto filtrado
    print(f"Filtered: {text}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("Waiting for texts to filter...")
channel.start_consuming()
