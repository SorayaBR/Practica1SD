import Pyro4
import redis
import sys
import random
import re

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@Pyro4.expose
class InsultFilter:
    def __init__(self, port):
        self.insults = "INSULTS"
        self.result_list = "RESULTS"
        self.port = port

    def filter_text(self, text):
        # Filtrar els insults en un text per substituir-los per CENSORED
        #print(f"Received text: {text}")
        insults = client.lrange(self.insults, 0, -1)
        for insult in insults:
            text = re.sub(rf'\b{re.escape(insult)}\b', "CENSORED", text, flags=re.IGNORECASE)
        
        client.rpush(self.result_list, text)
        #print(f"Filtered text: {text}")
        return text
    
    def get_filtered_texts(self):
        # Retorna la llista de textos amb els insults filtrats
        return client.lrange(self.result_list, 0, -1)


def run_server(port, name):
    Pyro4.config.SERIALIZERS_ACCEPTED.add("pickle")
    daemon = Pyro4.Daemon(port=int(port))
    ns = Pyro4.locateNS()
    uri = daemon.register(InsultFilter(port))
    ns.register(name, uri)

    print(f"**InsultFilter (pyro) is running in port {port}. The name is {name} and uri is: {uri}**")
    daemon.requestLoop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python insultFilter.py <puerto> <nombre>")
        sys.exit(1)

    port = sys.argv[1]
    name = sys.argv[2]  
    run_server(port, name)