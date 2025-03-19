import time
import xmlrpc.client
import random
import matplotlib.pyplot as plt

# Connexió amb els servidors
xmlrpc_service = xmlrpc.client.ServerProxy("http://localhost:8000")
xmlrpc_filter = xmlrpc.client.ServerProxy("http://localhost:8001")

# Dades de prova
insults = ["Tonto", "Cabrón", "Canana", "Bobo", "Gili", "Cretino", "Idiota", "Zopenco", "Zote", "Zanguango"]
texts = ["Eres un Tonto", "Hoy hace buen día", "Canana, no me hagas esto", "Me encanta la uni"]

def test_service(service, name):
    start_time = time.time()
    for _ in range(10):
        insult = random.choice(insults)
        service.add_insult(insult)
        service.get_insult()
        service.insult_me()
    elapsed_time = time.time() - start_time
    return elapsed_time

def test_filter(filter_service, name):
    start_time = time.time()
    for _ in range(10):
        text = random.choice(texts)
        filter_service.filter_text(text)
        filter_service.get_filtered_texts()
    elapsed_time = time.time() - start_time
    return elapsed_time

# Proves
nodes = [1, 2, 3]
speedup_results = {"XMLRPC": []}
speedup_filter_results = {"XMLRPC": []}

for n in nodes:
    requests = 10 * n  # Augmentem la carrega per a cada prova

    print(f"\nExecutant prova amb {n} nodes...")

    # XMLRPC
    time_elapsed = test_service(xmlrpc_service, "XMLRPC")
    speedup_results["XMLRPC"].append(time_elapsed)


    # Proves de filtrat
    time_filtred_elapsed = test_filter(xmlrpc_filter, "XMLRPC")
    speedup_filter_results["XMLRPC"].append(time_filtred_elapsed)

# Calcular Speedup
speedup_values = {key: [speedup_results[key][0] / t for t in speedup_results[key]] for key in speedup_results}
speedup_filter_values = {key: [speedup_filter_results[key][0] / t for t in speedup_filter_results[key]] for key in speedup_filter_results}
print (speedup_values)
print (speedup_filter_values)

# Gràfica de resultats
fig, ax = plt.subplots(1, 2, figsize=(15, 5))
for key, values in speedup_values.items():
    ax[0].plot(nodes, values, marker='x', label=key)
ax[0].set_xlabel("Número de nodos")
ax[0].set_ylabel("Speedup")
ax[0].set_title("Speedup en almacenamiento de insultos")
ax[0].legend()

print("Speed en almacenamiento de insultos")

for key, values in speedup_filter_values.items():
    ax[1].plot(nodes, values, marker='x', label=key)
ax[1].set_xlabel("Número de nodos")
ax[1].set_ylabel("Speedup")
ax[1].set_title("Speedup en filtrado de textos")
ax[1].legend()

print("Speed en filtrado de textos")

plt.tight_layout() 
plt.show()