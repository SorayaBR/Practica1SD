import Pyro4
import redis
import time

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@Pyro4.expose
class InsultServer:
    def __init__(self):
        self.insults = "INSULTS"

    def add_insult(self, insult):
        # Afegeix insults a la llista
        existing_insults = client.lrange(self.insults, 0, -1)
        if insult not in existing_insults:
            client.rpush(self.insults, insult)
            return "Insult added: {insult}"
        else:
            return "Insult already exists: {insult}"

    def get_insults(self):
        # Retorna la llista d'insults
        return client.lrange(self.insults, 0, -1)

    def broadcast_insults(self):
        # Envia insults a tots els clients cada 5 segons
        while True:
            insults = client.lrange(self.insults, 0, -1)
            for insult in insults:
                print(f"Broadcasting insult: {insult}")
                time.sleep(5)

def run_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(InsultServer)
    ns.register("insult.server", uri)

    print("InsultService running at {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    run_server()