import pika
import redis
import re
import sys

# Obtener el ID del worker desde los argumentos
worker_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
completion_queue = "completion_queue"  # Cola de finalización

# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Configurar RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar las colas
queue_name = "work_queue"
channel.queue_declare(queue=queue_name)
channel.queue_declare(queue=completion_queue)  # Cola de finalización

insult_list = "INSULTS"
result_list = "RESULTS"

print(f"InsultFilter {worker_id} (RabbitMQ) is running...")

def callback(ch, method, properties, body):
    text = body.decode()
    insults = client.lrange(insult_list, 0, -1)

    # Reemplazo de insultos
    for insult in insults:
        text = re.sub(rf'\b{re.escape(insult)}\b', "CENSORED", text, flags=re.IGNORECASE)

    # Agregar worker_id al resultado filtrado
    processed_text = f"[Worker {worker_id}] {text}"

    client.rpush(result_list, processed_text)  # Guardar texto filtrado
    #print(f"Filtered by Worker {worker_id}: {processed_text}")

    # Enviar señal a la cola de finalización
    channel.basic_publish(exchange='', routing_key=completion_queue, body=f"Worker {worker_id} done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("Waiting for texts to filter...")
channel.start_consuming()