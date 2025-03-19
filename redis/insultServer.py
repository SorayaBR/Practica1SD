import redis
import time
import random
import threading

# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

insult_list = "INSULTS"
channel_name = "insult_channel"

print("InsultService (Redis) is running...")

def store_insults():
    """Recibe insultos y los almacena en Redis (evitando duplicados)"""
    while True:
        insult = client.blpop("insult_queue", timeout=0)  # Espera hasta recibir un insulto
        if insult:
            insult_text = insult[1]
            existing_insults = client.lrange(insult_list, 0, -1)

            if insult_text not in existing_insults:
                client.rpush(insult_list, insult_text)
                print(f"Insult stored: {insult_text}")
            else:
                print(f"Duplicate insult ignored: {insult_text}")

def broadcast_insults():
    """Publica un insulto aleatorio cada 5 segundos"""
    while True:
        insults = client.lrange(insult_list, 0, -1)
        if insults:
            insult = random.choice(insults)  # Seleccionar un insulto aleatorio
            client.publish(channel_name, insult)
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
