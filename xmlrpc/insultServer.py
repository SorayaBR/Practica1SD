import xmlrpc.server
import redis
import time
import threading
import random

# Connexió amb Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class InsultService:
    def __init__(self):
        self.insult_list = "INSULTS"
    
    def add_insult(self, insult):
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
        insults = client.lrange(self.insults, 0, -1)
        if insults: 
            return random.choice(insults)
        return "No hay insultos en la lista"

def run_server():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    service = InsultService()
    server.register_instance(service)
    
    print("Servidor XML-RPC escoltant a localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    run_server()