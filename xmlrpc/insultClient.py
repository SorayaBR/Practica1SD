import xmlrpc.client

insultServer = xmlrpc.client.ServerProxy("http://localhost:8000")

# Afegir insults
print(insultServer.add_insult("Tonto"))
print(insultServer.add_insult("Cabrón"))
print(insultServer.add_insult("Canana"))
print(insultServer.add_insult("Tonto"))
print(insultServer.add_insult("Bobo"))

# Obtenir llista d'insults
print("Llista d'insults: ", insultServer.get_insult())