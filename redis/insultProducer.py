import redis
import random
import time

# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "work_queue"

texts = ["Eres un Tonto.", "Qué Canana eres.", "Hola, buen día.", "Eres más tonto que una piedra!", "¡Estás más perdido que un pulpo en un garaje!", "¡Vas a tropezar, idiota, no ves por dónde caminas!"]

print("Text Producer (Redis) is running...")

while True:
    text = random.choice(texts)
    client.rpush(queue_name, text)  # Enviar texto a la cola de trabajo
    print(f"Sent text: {text}")
    
