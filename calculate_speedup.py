import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Función para cargar y graficar los datos
def plot_speedup_from_json(file_name, figure_title):
    # Cargar los resultados del archivo JSON
    with open(file_name, "r") as f:
        results = json.load(f)
    
    technologies = ["XMLRPC", "PYRO"]
    num_nodes = [1, 2, 3]

    # Crear una figura para este archivo JSON
    fig, axes = plt.subplots(1, len(technologies), figsize=(15, 5), sharey=False)
    fig.suptitle(figure_title)
    
    if len(technologies) == 1:
        axes = [axes]  # Asegurarse de que sea iterable si solo hay una tecnología

    # Iterar sobre cada tecnología
    for i, tech in enumerate(technologies):
        speedups = []
        
        for nodes in num_nodes:
            if str(nodes) in results.get(tech, {}):
                # Tomamos el máximo speedup de los clientes en cada configuración de nodos
                max_speedup = max(
                    (data.get("speedup", 1.0) for data in results[tech][str(nodes)].values()),
                    default=1.0
                )
                speedups.append(max_speedup)
            else:
                speedups.append(1.0)  # Si no hay datos, asumimos speedup de 1

        # Graficar los resultados en la subgráfica correspondiente
        axes[i].plot(num_nodes, speedups, marker="o", linestyle="-", label=tech)
        axes[i].set_title(tech)
        axes[i].set_xlabel("Número de Nodos")
        if i == 0:
            axes[i].set_ylabel("Speedup")
        
        # Ajustes para que los valores se aprecien mejor
        axes[i].grid(True)
        axes[i].legend()
        
        # Asegurar que los números no se superpongan
        for tick in axes[i].get_xticklabels():
            tick.set_rotation(45) 
        for tick in axes[i].get_yticklabels():
            tick.set_fontsize(10) 

    # Ajustar el espacio entre las subgráficas
    plt.tight_layout()
    plt.subplots_adjust(top=0.85) 

# Graficar los resultados de los dos archivos JSON
plot_speedup_from_json("results_insultServers.json", "Speedup InsultServers")
plot_speedup_from_json("results_insultFilters.json", "Speedup InsultFilters")

# Mostrar las gráficas
plt.show()
