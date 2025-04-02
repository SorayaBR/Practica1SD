import json
import matplotlib.pyplot as plt
import numpy as np

# Función para cargar y graficar los datos
def plot_speedup_from_json(file_names, figure_title):
    # Cargar los resultados del archivo JSON
    results = {}
    for file_name in file_names:
        with open(file_name, "r") as f:
            data = json.load(f)
            results.update(data)
    
    if figure_title == "Speedup InsultServers":
        technologies = ["XMLRPC", "PYRO"]
        fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=False)
    else:
        technologies = ["XMLRPC", "PYRO", "Redis"]
        fig, axes = plt.subplots(2, 2, figsize=(10, 10), sharey=False)
    
    fig.suptitle(figure_title)
    num_nodes = [1, 2, 3]
    colores = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"] 
    # Asegurar que los ejes son una lista bidimensional para iteración
    axes = np.array(axes).reshape(-1)  # Convertir en un array plano para acceder por índice

    # Iterar sobre cada tecnología y asignar su subplot
    for i, tech in enumerate(technologies):
        speedups = []
        
        for nodes in num_nodes:
            if str(nodes) in results.get(tech, {}):
                max_speedup = max(
                    (data.get("speedup", 1.0) for data in results[tech][str(nodes)].values()),
                    default=1.0
                )
                speedups.append(max_speedup)
            else:
                speedups.append(1.0)  # Si no hay datos, asumimos speedup de 1

        # Graficar en la subgráfica correspondiente
        ax = axes[i]  # Seleccionar el subplot correcto
        ax.plot(num_nodes, speedups, marker="o", linestyle="-", label=tech, color=colores[i])
        ax.set_title(tech, color=colores[i])
        ax.set_xlabel("Nodos")
        if i % 2 == 0:  # Primera columna
            ax.set_ylabel("Speedup")
        
        ax.grid(True)
        ax.legend()

    # Ajustar el espacio entre las subgráficas
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, hspace=0.5)

# Graficar los resultados de los dos archivos JSON
plot_speedup_from_json(["results_insultServers.json"], "Speedup InsultServers")
plot_speedup_from_json(["results_insultFilters.json", "results_Redis_insultFilters.json"], "Speedup InsultFilters")

# Mostrar las gráficas
plt.show()