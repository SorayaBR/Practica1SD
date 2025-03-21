import xmlrpc.server
import redis
import time
import threading
import random
import sys

# Connexió amb Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class InsultService:
    def __init__(self):
        self.insult_list = "INSULTS"
    
    def add_insult(self, insult):
        print(f"Received insult: {insult}")
        #Afegir insult a la llista si no està ja
        existing_insults = client.lrange(self.insult_list, 0, -1)
        if insult not in existing_insults:
            client.rpush(self.insult_list, insult)
            return "Insult afegit:" + insult
        else:
            return "Insult ja existent:" + insult
    
    def get_insult(self):
        # Retorna la llista d'insults emmagatzemats
        return client.lrange(self.insult_list, 0, -1)
    
    def insult_me(self):
        # Retorna un insult aleatori
        insults = client.lrange(self.insult_list, 0, -1)
        if insults: 
            return random.choice(insults)
        return "No hay insultos en la lista"

def run_server(port):
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", port), allow_none=True)
    service = InsultService()
    server.register_instance(service)
    
    print("InsultServer (xmlrpc) is running in port ", port)
    server.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000  # Por defecto, puerto 8000
    run_server(port)