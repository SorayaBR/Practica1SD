import json
import subprocess
import time
import math
import pika
import signal

# Configuración de sistema
average_processing_time = 0.0040  # Tiempo medio por mensaje (segundos)
worker_capacity = 1 / average_processing_time  # Mensajes/segundo que puede procesar un worker
target_response_time = 1  # Tiempo objetivo de respuesta (segundos)

worker_processes = []

# Función para calcular número de trabajadores necesarios
def calculate_workers(message_rate, worker_capacity, backlog):
    N = math.ceil((backlog + (message_rate * target_response_time)) / worker_capacity)
    return N

# Obtener longitud actual de la cola
def get_queue_length(channel, queue_name):
    queue_info = channel.queue_declare(queue=queue_name, passive=True)
    return queue_info.method.message_count

# Crear o eliminar workers según necesidad
def adjust_workers(target_num):
    global worker_processes
    current_num = len(worker_processes)

    if target_num > current_num:
        for i in range(current_num, target_num):
            proc = subprocess.Popen(["python", "RabbitMQ/insultFilter.py", str(i)])
            worker_processes.append(proc)
            print(f"[+] Started Worker {i + 1}")
    elif target_num < current_num:
        for i in range(current_num - target_num):
            proc = worker_processes.pop()
            proc.send_signal(signal.SIGTERM)
            print("[-] Stopped a worker")

# Función principal de escalado dinámico
def dynamic_scaling():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    queue_name = "work_queue"

    print("⚙️  Dynamic scaling system started...")

    previous_queue_length = get_queue_length(channel, queue_name)
    previous_time = time.time()

    log_data = []  # Para guardar los resultados
    scaling_events = []  # Para guardar cambios de número de workers
    last_required_workers = len(worker_processes)

    try:
        while True:
            time.sleep(5)

            current_queue_length = get_queue_length(channel, queue_name)
            current_time = time.time()

            delta_msgs = max(0, current_queue_length - previous_queue_length)
            delta_time = current_time - previous_time

            message_rate = delta_msgs / delta_time if delta_time > 0 else 0
            required_workers = calculate_workers(message_rate, worker_capacity, current_queue_length)

            print(f"[=] Queue: {current_queue_length} | ΔMsgs: {delta_msgs} | Rate: {message_rate:.2f} msg/s | Target workers: {required_workers} | Running: {len(worker_processes)}")

            # Guardar resultado en el log
            log_data.append({
                "message_rate": round(message_rate, 2),
                "required_workers": required_workers
            })

            with open("scaling_log.json", "w") as f:
                json.dump(log_data, f, indent=4)

            # Registrar cambio de número de workers si hay cambio
            if required_workers != last_required_workers:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                scaling_events.append({
                    "timestamp": timestamp,
                    "workers": required_workers
                })

                with open("worker_scaling_events.json", "w") as f:
                    json.dump(scaling_events, f, indent=4)

                last_required_workers = required_workers

            adjust_workers(required_workers)

            previous_queue_length = current_queue_length
            previous_time = current_time

    except KeyboardInterrupt:
        print("\n⛔ Ctrl+C detected. Terminating all workers...")
        for proc in worker_processes:
            proc.terminate()
        print("✅ All workers terminated.")

# Ejecutar si se llama como script principal
if __name__ == "__main__":
    dynamic_scaling()
