import redis
import random
import time

# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "work_queue"

texts = ["Hola, eres un Tonto.", "Qué buen día.", "Eres un Canana.", "Vamos al cine?"]

print("Text Producer (Redis) is running...")

while True:
    text = random.choice(texts)
    client.rpush(queue_name, text)  # Enviar texto a la cola de trabajo
    print(f"Sent text: {text}")
    time.sleep(5)
