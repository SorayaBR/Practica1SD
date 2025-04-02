import time
import random
import json
import multiprocessing
import xmlrpc.client
import Pyro4
import pika
import redis

# Lista de insultos y textos de prueba
insults = ["Tonto", "Cabrón", "Canana", "Bobo", "Gili", "Cretino", "Idiota", "Zopenco", "Zote", "Zanguango"]

# Configuración de puertos y direcciones
xmlrpc_ports = [8000, 8001, 8002]
pyro_names = ["insultService1", "insultService2", "insultService3"]
redis_host = "localhost"

# Funciones para crear clientes de cada tecnología
def create_xmlrpc_client(server_load, nodes):
    available_ports = xmlrpc_ports[:nodes]

    selected_port = min(available_ports, key=lambda port: server_load[port])  # Puerto con menos carga
    server_load[selected_port] += 1
    print(f"🔗 Cliente conectado a http://localhost:{selected_port}")

    return xmlrpc.client.ServerProxy(f"http://localhost:{selected_port}")

def create_pyro_client(server_load, nodes):
    ns = Pyro4.locateNS()  
    available_names = pyro_names[:nodes]

    selected_name = min(available_names, key=lambda name: server_load[name])  
    server_load[selected_name] += 1
    uri = ns.lookup(selected_name)  

    print(f"🔗 Cliente Pyro conectado a {selected_name} ({uri})")
    return Pyro4.Proxy(uri)

# Función para probar cada servicio con un conjunto de peticiones
def test_service(client, method, num_messages):
    start_time = time.time()
    for _ in range(num_messages): 
        insult = random.choice(insults)
        method(client, insult)
    total_time = time.time() - start_time
    return num_messages / total_time # Devuelve mensajes por segundo

# Función específica para XMLRPC
def xmlrpc_insult(client, insult):
    client.insult_me()

def pyro_insult(client, insult):
    client.insult_me()

# Función que ejecuta los clientes en paralelo para cada tecnología y número de nodos
def client_process(tech, nodes, server_load_xmlrpc, server_load_pyro, process_id, manager_dict, num_messages):
    if tech == "XMLRPC":
        client = create_xmlrpc_client(server_load_xmlrpc, nodes)
    elif tech == "PYRO":
        client = create_pyro_client(server_load_pyro, nodes)
    
    time.sleep(6)
    start_time = time.time()
    if tech == "XMLRPC":
        R = test_service(client, xmlrpc_insult, num_messages)
    elif tech == "PYRO":
        R = test_service(client, pyro_insult, num_messages)

    manager_dict[process_id] = R

if __name__ == "__main__":
    num_clients = 5  # Ahora probamos con 1 a 6 clientes simultáneos
    technologies = ["XMLRPC", "PYRO"]  # Probamos con XMLRPC y Pyro
    baseline_rates = {}
    results = {tech: {str(nodes): {} for nodes in [1, 2, 3]} for tech in technologies}

    for nodes in [1, 2, 3]:  # Primero con 1 nodo, luego 2 y luego 3
        input(f"\n Levanta {nodes} nodo(s) y presiona Enter para continuar...")

        for tech in technologies:  # Evaluamos cada tecnología
            num_messages = 50 if tech == "XMLRPC" else 3000
            print(f"\n**Ejecutando pruebas para {tech} con {nodes} nodo(s)**")

           # Usamos Manager para compartir el contador de clientes entre procesos
            with multiprocessing.Manager() as manager:
                # Inicializamos el diccionario de carga con 0 clientes por puerto
                server_load_xmlrpc = manager.dict({port: 0 for port in xmlrpc_ports})
                server_load_pyro = manager.dict({name: 0 for name in pyro_names})
                processes = []
                manager_dict = manager.dict()

                for process_id in range(num_clients):  # Ejecutamos varios clientes simultáneamente
                    p = multiprocessing.Process(target=client_process, args=(tech, nodes, server_load_xmlrpc, server_load_pyro, process_id, manager_dict, num_messages))
                    p.start()
                    processes.append(p)

                for p in processes:
                    p.join()
                    
                R_N = sum(manager_dict.values())  # Sumamos el rendimiento de todos los clientes
                results[tech][str(nodes)][str(num_clients)] = {"rate": R_N}
                print(f"--> {tech} - {nodes} nodos - messages: {num_messages} - {num_clients} clientes: {R_N:.2f} msg/seg")

                # Guardamos T1 (cuando nodes=1) para calcular Speedup
                if nodes == 1:
                    baseline_rates[tech] = R_N

                # Calcular Speedup para cada configuración
                R_1 = baseline_rates.get(tech, None)
                if R_1 and R_N:
                    speedup = R_N / R_1
                    results[tech][str(nodes)][str(num_clients)]["speedup"] = round(speedup, 5)
                    print(f" Speedup {tech} - {nodes} nodos - messages: {num_messages} - {num_clients} clientes: {R_N}/{R_1}={speedup:.5f}")

    # Guardar resultados en JSON
    with open("results_insultServers.json", "w") as f:
        json.dump(results, f, indent=4)

    print("\n-----Resultados guardados en 'results_insultServers.json------'")