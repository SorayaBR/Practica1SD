import xmlrpc.client

insultServer = xmlrpc.client.ServerProxy("http://localhost:8000")

# Afegir insults
print(insultServer.add_insult("Tonto"))
print(insultServer.add_insult("Cabrón"))
print(insultServer.add_insult("Canana"))
print(insultServer.add_insult("Tonto"))
print(insultServer.add_insult("Bobo"))

# Obtenir llista d'insults
print("Llista d'insults: ", insultServer.get_insults())

# Rebre insults
print("\nReceiving 5 random insults:")
for _ in range(5):
    print(insultServer.insult_me())