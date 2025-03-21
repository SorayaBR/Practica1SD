import xmlrpc.server
import redis
import re

# Connexió amb Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class InsultFilter:
    def __init__(self):
        self.insult_list = "INSULTS"
        self.result_list = "RESULTS"
    
    def filter_text(self, text):
        # Filtrar els insults en un text per substituir-los per CENSORED
        insults = client.lrange(self.insult_list, 0, -1)
        for insult in insults:
            text = re.sub(rf'\b{re.escape(insult)}\b', "CENSORED", text, flags=re.IGNORECASE)
        
        client.rpush(self.result_list, text)
        return text

    def get_filtered_texts(self):
        # Retorna la llista de textos amb els insults filtrats
        return client.lrange(self.result_list, 0, -1)

def run_server():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8001), allow_none=True)
    filter_service = InsultFilter()
    server.register_instance(filter_service)
    
    print("InsultFilter (xmlrpc) is running...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()