import Pyro4

# Connexió amb servidor Pyro
insult_service = Pyro4.Proxy("PYRONAME:insult.server")

# Afegir insults
print(insult_service.add_insult("Tonto"))
print(insult_service.add_insult("Bobo"))
print(insult_service.add_insult("Canana"))
print(insult_service.add_insult("Tonto"))

# Obtenir llista d'insults
print("Stored insults: ", insult_service.get_insults())

# Rebre insults
print("\nReceiving 5 random insults:")
for _ in range(5):
    print(insult_service.insult_me())

