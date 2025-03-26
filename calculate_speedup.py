import json
import matplotlib.pyplot as plt

# Cargar los resultados del archivo JSON
with open("results_insultServers.json", "r") as f:
    results = json.load(f)

# Preparar los datos
technologies = ["XMLRPC", "PYRO"]
num_nodes = [1, 2, 3]

plt.figure(figsize=(8, 5))

# Iterar sobre cada tecnología
for tech in technologies:
    speedups = []
    
    for nodes in num_nodes:
        if str(nodes) in results[tech]:
            # Tomamos el máximo speedup de los clientes en cada configuración de nodos
            max_speedup = max(
                (data.get("speedup", 1.0) for data in results[tech][str(nodes)].values()),
                default=1.0
            )
            speedups.append(max_speedup)
        else:
            speedups.append(1.0)  # Si no hay datos, asumimos speedup de 1

    plt.plot(num_nodes, speedups, marker="o", linestyle="-", label=tech)

# Configurar el gráfico
plt.xlabel("Número de Nodos")
plt.ylabel("Speedup")
plt.title("Speedup InsultServers")
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()
