import xmlrpc.client

filterService = xmlrpc.client.ServerProxy("http://localhost:8001")

# Filtrar textos
print(filterService.filter_text("Eres un Tonto."))
print(filterService.filter_text("Qué Canana eres."))
print(filterService.filter_text("Hola, buen día."))  

# Obtenir textos filtrats
print("Filtered texts:", filterService.get_filtered_texts())