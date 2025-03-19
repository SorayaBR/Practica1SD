import time
import random
import json
import multiprocessing
import xmlrpc.client
import Pyro4
import pika
import redis

insults = ["Tonto", "Cabrón", "Canana", "Bobo", "Gili", "Cretino", "Idiota", "Zopenco", "Zote", "Zanguango"]
texts = ["Eres un Tonto", "Hoy hace buen día", "Canana, no me hagas esto", "Me encanta la uni"]

xmlrpc_ports = [8000, 8001, 8002]
pyro_names = ["PYRO:insultService1@localhost:9000", "PYRO:insultService2@localhost:9001", "PYRO:insultService3@localhost:9002"]
rabbitmq_host = "localhost"
redis_host = "localhost"

def create_xmlrpc_client(port):
    return xmlrpc.client.ServerProxy(f"http://localhost:{port}")

def create_pyro_client(name):
    return Pyro4.Proxy(name)

def create_rabbitmq_client():
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    return conn.channel()

def create_redis_client():
    return redis.StrictRedis(host=redis_host, port=6379, decode_responses=True)

def test_service(client, method):
    for _ in range(10):
        insult = random.choice(insults)
        method(client, insult)

def xmlrpc_insult(client, insult):
    client.add_insult(insult)
    client.get_insult()
    client.insult_me()

def client_process(tech, nodes):
    if tech == "XMLRPC":
        client = create_xmlrpc_client(random.choice(xmlrpc_ports[:nodes]))
        test_service(client, xmlrpc_insult)

if __name__ == "__main__":
    num_clients = [10, 20]
    technologies = ["XMLRPC", "PYRO", "RabbitMQ", "Redis"]
    results = {tech: {nodes: {} for nodes in [1, 2, 3]} for tech in technologies}

    for nodes in [1, 2, 3]:
        for tech in technologies:
            for clients in num_clients:
                processes = []
                start_time = time.time()

                for _ in range(clients):
                    p = multiprocessing.Process(target=client_process, args=(tech, nodes))
                    p.start()
                    processes.append(p)

                for p in processes:
                    p.join()

                elapsed_time = time.time() - start_time
                results[tech][nodes][clients] = elapsed_time
                print(f"{tech} - {nodes} nodos - {clients} clientes: {elapsed_time:.2f} segundos")

    with open("results.json", "w") as f:
        json.dump(results, f)