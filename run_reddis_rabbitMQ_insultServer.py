import subprocess
import time

num_workers = 3
processes = []

for i in range(1, num_workers + 1):
    process = subprocess.Popen(["python", "redis/insultFilter.py", str(i)])
    processes.append(process)
    input(f"Presiona Enter para añadir otro worker {i}...")

# Opcional: Esperar que terminen
for process in processes:
    process.wait()