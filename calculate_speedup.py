import json
import matplotlib.pyplot as plt

with open("results.json", "r") as f:
    results = json.load(f)

speedup_results = {}

for tech, nodes_data in results.items():
    speedup_results[tech] = {}
    for nodes, clients_data in nodes_data.items():
        base_time = clients_data["2"]
        speedup_results[tech][nodes] = {int(clients): base_time / time for clients, time in clients_data.items()}

# Graficar resultados
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, nodes in enumerate([1, 2, 3]):
    ax = axes[idx]
    for tech, values in speedup_results.items():
        clients = list(values[str(nodes)].keys())
        speedup = list(values[str(nodes)].values())
        ax.plot(clients, speedup, marker="o", linestyle="-", label=tech)

    ax.set_xlabel("Número de Clientes")
    ax.set_ylabel("Speedup")
    ax.set_title(f"Speedup con {nodes} nodos")
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()
