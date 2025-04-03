import subprocess
import time
import pika
import redis
import json

# Función para medir el tiempo de ejecución
def measure_time(max_workers, num_messages):
    # Conectar con Redis
    client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    queue_name = "work_queue"
    completion_queue = "completion_queue"  # Cola de finalización

    # Conectar con RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declarar la cola de trabajo y la cola de finalización
    channel.queue_declare(queue=queue_name)
    channel.queue_declare(queue=completion_queue)

    # Lista para almacenar los procesos de los trabajadores
    procesos = []
    tiempos = []  # Lista para almacenar los tiempos de ejecución de cada conjunto de trabajadores

    for num_workers in range(1, max_workers + 1):
        # Iniciar los trabajadores (workers)
        print(f"Iniciando {num_workers} trabajador(es)...")
        for i in range(1, num_workers + 1):
            process = subprocess.Popen(["python", "RabbitMQ/insultFilter.py", str(i)])  # Iniciar cada trabajador
            procesos.append(process)

        time.sleep(1)  # Esperar un segundo para asegurarse de que los trabajadores estén listos

        # Medir el tiempo de inicio (antes de ejecutar el productor)
        start_time = time.time()

        # Ejecutar el productor para enviar todos los mensajes primero
        print(f"Ejecutando insultProducer para enviar {num_messages} mensajes con {num_workers} trabajador(es)...")
        subprocess.run(["python", "RabbitMQ/insultProducer.py", str(num_messages)])  # Ejecuta el productor (envía los mensajes)
        
        # Esperar hasta que todos los mensajes sean procesados
        #print("Esperando a que todos los trabajadores terminen...")
        messages_received = 0
        while messages_received < num_messages:
            # Obtener los mensajes de la cola de finalización
            method_frame, header_frame, body = channel.basic_get(completion_queue, auto_ack=True)
            if body:
                messages_received += 1


        # Medir el tiempo cuando todos los mensajes han sido procesados
        end_time = time.time()

        # Calcular el tiempo total de ejecución
        total_time = end_time - start_time
        tiempos.append(total_time)  # Guardar el tiempo para el número actual de trabajadores

    # Finalizar los procesos de los workers
    for process in procesos:
        process.terminate()

    return tiempos

# Número de mensajes a enviar (puedes cambiar esto según lo que necesites)
num_messages = 2000

# Ejecutar con 1, 2 y 3 trabajadores
tiempos = measure_time(3, num_messages)

# Calcular el speedup
speedup_1 = tiempos[0] / tiempos[0]  # Speedup con 1 trabajador (siempre 1.0)
speedup_2 = tiempos[0] / tiempos[1]  # Speedup con 2 trabajadores
speedup_3 = tiempos[0] / tiempos[2]  # Speedup con 3 trabajadores

# Mostrar los resultados
print(f"Tiempo con 1 trabajador: {tiempos[0]} segundos")
print(f"Tiempo con 2 trabajadores: {tiempos[1]} segundos")
print(f"Tiempo con 3 trabajadores: {tiempos[2]} segundos")

print(f"Speedup con 2 trabajadores: {speedup_2}")
print(f"Speedup con 3 trabajadores: {speedup_3}")

# Crear el JSON de RabbitMQ con el número de mensajes en la clave
rabbitmq_result = {
    "RabbitMQ": {
        "1": {
            str(num_messages): {
                "rate": tiempos[0],
                "speedup": speedup_1
            }
        },
        "2": {
            str(num_messages): {
                "rate": tiempos[1],
                "speedup": speedup_2
            }
        },
        "3": {
            str(num_messages): {
                "rate": tiempos[2],
                "speedup": speedup_3
            }
        }
    }
}

# Guardar resultados en JSON
with open("results_RabbitMQ_insultFilters.json", "w") as f:
    json.dump(rabbitmq_result, f, indent=4)
