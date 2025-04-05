import time
import pika
import random

# Conectar con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar la cola
queue_name = "work_queue"
channel.queue_declare(queue=queue_name)

texts = ["Hola, eres un Tonto.", "Qué buen día.", "Eres un Canana.", "Vamos al cine?"]

def produce_wave(rate, duration):
    total_messages = int(rate * duration)
    interval = 1.0 / rate  # Tiempo entre mensajes para respetar la tasa

    print(f"🚀 Enviando {total_messages} mensajes a {rate} msg/s durante {duration} segundos...")
    for _ in range(total_messages):
        text = random.choice(texts)
        channel.basic_publish(exchange='', routing_key=queue_name, body=text)
        time.sleep(interval)

def simulate_load():
    rate = 100  # Tasa inicial de mensajes por segundo
    duration = 5  # Duración de cada oleada (segundos)

    for wave in range(4):
        produce_wave(rate, duration)
        rate += 200  # Incrementamos la tasa para la siguiente oleada
        print(f"✅ Finalizó ola {wave + 1}\n")
        time.sleep(3)  # Pausa entre oleadas

    connection.close()
    print("🏁 Simulación finalizada.")

if __name__ == "__main__":
    simulate_load()