import json
import matplotlib.pyplot as plt

# Cargar los resultados del archivo JSON
with open("results_insultServers.json", "r") as f:
    results = json.load(f)

# Graficar los resultados de speedup
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Iterar sobre los nodos
for idx, nodes in enumerate([1, 2, 3]):
    ax = axes[idx]
    
    # Iterar sobre las tecnologías (XMLRPC y PYRO)
    for tech, nodes_data in results.items():
        if str(nodes) in nodes_data:
            # Obtener los valores de clientes y speedup para esta tecnología y número de nodos
            clients = list(nodes_data[str(nodes)].keys())
            speedup = [
                nodes_data[str(nodes)][client].get("speedup", 1.0)  # Si no hay speedup, usar 1.0 como valor por defecto
                for client in clients
            ]
            
            # Graficar los resultados
            ax.plot(clients, speedup, marker="o", linestyle="-", label=tech)

    # Configurar el gráfico
    ax.set_xlabel("Número de Clientes")
    ax.set_ylabel("Speedup")
    ax.set_title(f"Speedup con {nodes} nodo(s)")
    ax.legend()
    ax.grid(True)

# Ajustar el diseño
plt.tight_layout()
plt.show()
