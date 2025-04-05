import json
import matplotlib.pyplot as plt
from datetime import datetime

# Leer el archivo JSON
with open('worker_scaling_events.json', 'r') as file:
    data = json.load(file)

# Procesar los datos
times = [datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S") for entry in data]
workers = [entry["workers"] for entry in data]

# Crear la gráfica
plt.figure(figsize=(10, 5))
plt.plot(times, workers, color="hotpink", marker="o", linestyle='-')
plt.title("Dynamic Scale")
plt.xlabel("Time")
plt.ylabel("num Workers")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Mostrar
plt.show()