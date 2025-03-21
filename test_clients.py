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
pyro_names = ["PYRO:insultService1@localhost:9000", "PYRO:insultService2@localhost:9001", "PYRO:insultService3@localhost:9002"]
rabbitmq_host = "localhost"
redis_host = "localhost"

# Funciones para crear clientes de cada tecnología
def create_xmlrpc_client(server_load, nodes):
    available_ports = xmlrpc_ports[:nodes]

    selected_port = min(available_ports, key=lambda port: server_load[port])  # Puerto con menos carga
    server_load[selected_port] += 1
    print(f"🔗 Cliente conectado a http://localhost:{selected_port}")

    return xmlrpc.client.ServerProxy(f"http://localhost:{selected_port}")

def create_pyro_client(server_load, nodes):
    available_names = pyro_names[:nodes]
    selected_name = min(available_names, key=lambda name: server_load[name])  # Seleccionar el servicio con menos carga
    server_load[selected_name] += 1
    print(f"🔗 Cliente conectado a {selected_name}")

    return Pyro4.Proxy(selected_name)
#def create_rabbitmq_client():
#    conn = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
#    return conn.channel()

#def create_redis_client():
#    return redis.StrictRedis(host=redis_host, port=6379, decode_responses=True)

# Función para probar cada servicio con un conjunto de peticiones
def test_service(client, method):
    for _ in range(5):  # Se hacen 10 llamadas por cliente
        insult = random.choice(insults)
        method(client, insult)

# Función específica para XMLRPC
def xmlrpc_insult(client, insult):
    client.add_insult(insult)
    client.get_insult()
    client.insult_me()

def pyro_insult(client, insult):
    client.add_insult(insult)
    client.get_insult()
    client.insult_me()

# Función que ejecuta los clientes en paralelo para cada tecnología y número de nodos
def client_process(tech, nodes, server_load):
    if tech == "XMLRPC":
        client = create_xmlrpc_client(server_load, nodes)
        test_service(client, xmlrpc_insult)
    elif tech == "PYRO":
        client = create_pyro_client(server_load, nodes)
        test_service(client, pyro_insult)

if __name__ == "__main__":
    num_clients = [2,3,6]  # Ahora probamos con 1 a 6 clientes simultáneos
    technologies = ["XMLRPC", "PYRO"]  # Probamos con XMLRPC y Pyro
    results = {tech: {str(nodes): {} for nodes in [1, 2, 3]} for tech in technologies}

    for nodes in [1, 2, 3]:  # Primero con 1 nodo, luego 2 y luego 3
        input(f"\n➡️  Levanta {nodes} nodo(s) y presiona Enter para continuar...")

        for tech in technologies:  # Evaluamos cada tecnología
            print(f"\n⏳ Ejecutando pruebas para {tech} con {nodes} nodo(s)...")

           # Usamos Manager para compartir el contador de clientes entre procesos
            with multiprocessing.Manager() as manager:
                # Inicializamos el diccionario de carga con 0 clientes por puerto
                server_load = manager.dict({port: 0 for port in xmlrpc_ports})

                for clients in num_clients:
                    processes = []
                    start_time = time.time()

                    for _ in range(clients):  # Ejecutamos varios clientes simultáneamente
                        p = multiprocessing.Process(target=client_process, args=(tech, nodes, server_load))
                        p.start()
                        processes.append(p)

                    for p in processes:
                        p.join()

                    elapsed_time = time.time() - start_time
                    results[tech][str(nodes)][str(clients)] = elapsed_time
                    print(f"✅ {tech} - {nodes} nodos - {clients} clientes: {elapsed_time:.2f} segundos")

    # Guardar resultados en JSON
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("\n📊 Resultados guardados en 'results.json'")