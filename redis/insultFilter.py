import redis
import re
import sys

# Obtener el ID del worker desde los argumentos
worker_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "work_queue"
insult_list = "INSULTS"
result_list = "RESULTS"

print(f"InsultFilter {worker_id} (Redis) is running...")

while True:
    task = client.blpop(queue_name, timeout=0)  # Espera un mensaje
    if task:
        text = task[1]
        insults = client.lrange(insult_list, 0, -1)

        # Reemplazo de insultos
        for insult in insults:
            text = re.sub(rf'\b{re.escape(insult)}\b', "CENSORED", text, flags=re.IGNORECASE)

        processed_text = f"[Worker {worker_id}] {text}"
        client.rpush(result_list, processed_text)  # Guardar texto filtrado
        print(f"Filtered by Worker {worker_id}: {processed_text}")
