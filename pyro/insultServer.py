import Pyro4
import redis
import time
import random

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@Pyro4.expose
@Pyro4.oneway # Ho fem servir per al broadcast d'insults
class InsultServer:
    def __init__(self):
        self.insults = "INSULTS"

    def add_insult(self, insult):
        # Afegeix insults a la llista
        existing_insults = client.lrange(self.insults, 0, -1)
        if insult not in existing_insults:
            client.rpush(self.insults, insult)
            return "Insult added: " +insult
        else:
            return "Insult already exists: " +insult

    def get_insults(self):
        # Retorna la llista d'insults
        return client.lrange(self.insults, 0, -1)

    def insult_me(self):
        # Retorna un insult aleatori
        insults = client.lrange(self.insults, 0, -1)
        if insults: 
            return random.choice(insults)
        return "No hay insultos en la lista"

def run_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(InsultServer)
    ns.register("insult.server", uri)

    print("InsultService running at "+ str(uri))
    daemon.requestLoop()

if __name__ == "__main__":
    run_server()