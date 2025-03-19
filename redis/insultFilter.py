import redis
import re

# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "work_queue"
insult_list = "INSULTS"
result_list = "RESULTS"

print("InsultFilter (Redis) is running...")

while True:
    task = client.blpop(queue_name, timeout=0)  # Espera un mensaje
    if task:
        text = task[1]
        insults = client.lrange(insult_list, 0, -1)

        # Reemplazo de insultos
        for insult in insults:
            text = re.sub(rf'\b{re.escape(insult)}\b', "CENSORED", text, flags=re.IGNORECASE)

        client.rpush(result_list, text)  # Guardar texto filtrado
        print(f"Filtered: {text}")
