import redis
import random
import time
import threading

# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

insults = ["Tonto", "Canana", "Friki", "NPC", "Inútil"]
channel_name = "insult_channel"

print("Insult Client (Redis) is running...")

def send_insults():
    """Envía insultos a la cola cada 3 segundos"""
    while True:
        insult = random.choice(insults)
        client.rpush("insult_queue", insult)  # Enviar insulto a la cola
        print(f"Sent insult: {insult}")
        time.sleep(3)

def receive_insults():
    """Escucha insultos desde el broadcast de Redis"""
    pubsub = client.pubsub()
    pubsub.subscribe(channel_name)

    print(f"Listening for broadcast insults on {channel_name}...")

    for message in pubsub.listen():
        if message["type"] == "message":
            print(f"Received broadcast insult: {message['data']}")

# Iniciar hilos separados
threading.Thread(target=send_insults, daemon=True).start()
threading.Thread(target=receive_insults, daemon=True).start()

# Mantener el programa activo
while True:
    time.sleep(1)
