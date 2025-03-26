import xmlrpc.server
import redis
import re
import sys

# Connexió amb Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class InsultFilter:
    def __init__(self, port):
        self.insult_list = "INSULTS"
        self.result_list = "RESULTS"
        self.port = port
    
    def filter_text(self, text):
        # Filtrar els insults en un text per substituir-los per CENSORED
        print(f"Received text: {text}")
        insults = client.lrange(self.insult_list, 0, -1)
        for insult in insults:
            text = re.sub(rf'\b{re.escape(insult)}\b', "CENSORED", text, flags=re.IGNORECASE)
        
        client.rpush(self.result_list, text)
        print(f"Filtered text: {text}")
        return text

    def get_filtered_texts(self):
        # Retorna la llista de textos amb els insults filtrats
        return client.lrange(self.result_list, 0, -1)

def run_server(port):
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", port), allow_none=True)
    filter_service = InsultFilter(port)
    server.register_instance(filter_service)
    
    print(f"**InsultFilter (xmlrpc) is running in port {port}**")
    server.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8003  # Por defecto, puerto 8003
    run_server(port)