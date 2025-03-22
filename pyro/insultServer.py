import Pyro4
import redis
import sys
import random

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@Pyro4.expose
class InsultServer:
    def __init__(self, port):
        self.insults = "INSULTS"
        self.port = port

    def add_insult(self, insult):        
        print(f"Received insult: {insult} (port: {self.port})")
        #Afegir insult a la llista si no està ja
        existing_insults = client.lrange(self.insults, 0, -1)
        if insult not in existing_insults:
            client.rpush(self.insults, insult)
            return "Insult afegit:" + insult
        else:
            return "Insult ja existent:" + insult

    def get_insults(self):
        # Retorna la llista d'insults
        insults = client.lrange(self.insults, 0, -1)
        print(f"Send insults: {insults} (port: {self.port})")
        return insults

    def insult_me(self):
        # Retorna un insult aleatori
        insults = client.lrange(self.insults, 0, -1)
        if insults: 
            insult = random.choice(insults)
            print(f"Send insult: {insult} (port: {self.port})")
            return insult
        return "No hay insultos en la lista"

def run_server(port, name):
    Pyro4.config.SERIALIZERS_ACCEPTED.add("pickle")
    daemon = Pyro4.Daemon(port=int(port))
    ns = Pyro4.locateNS()
    uri = daemon.register(InsultServer(port))
    ns.register(name, uri)

    print(f"**InsultServer (pyro) is running in port {port}. The name is {name} and uri is: {uri}**")
    daemon.requestLoop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python insultServer.py <puerto> <nombre>")
        sys.exit(1)

    port = sys.argv[1]
    name = sys.argv[2]  
    run_server(port, name)