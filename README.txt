PARA EJECUTAR INSULT SERVER TEST:
XMLRPC/PYRO
1. run_xmlrpc_pyro_insultServers.py
2. test_xmlrpc_pyro_insultServers.py 
Los anteriores van intercalados, primero se ejecuta con 1 nodo los servidores, luego se va a clientes y se ejecutan, una vez haya 
acabado se vuelve a los servidores y con un ENTER se ejecutan 2, luego vuelves a clients y le das a ENTER para que se ejecuten para 
2 nodos y así hasta 3!!!!!
REDDIS/RABBITMQ
3. run_reddis_insultFilter.py
4. run_RabbitMQ_insultFilter.py

PARA EJECUTAR INSULT Filter TEST (Solo xmlrpc y pyro):
5. run_xmlrpc_pyro_insultFilters.py
6. test_xmlrpc_pyro_insultFilter.py
Los anteriores van intercalados, primero se ejecuta con 1 nodo los servidores, luego se va a clientes y se ejecutan, una vez haya 
acabado se vuelve a los servidores y con un ENTER se ejecutan 2, luego vuelves a clients y le das a ENTER para que se ejecuten para 
2 nodos y así hasta 3!!!!!

PARA VER LOS RESULTADOS DE LOS JSON:
7. calculate_speedup.py

PARA EJECUTAR DYNAMIC SCALE RABBITMQ:
8. dinamic_scaler_RabbitMQ.py
9. Dentro de la carpeta RabbitMQ --> insultProducer_Oleadas.py

PARA VER LOS RESULTADOS DE LOS JSON:
7. dinamic_scaler_RabbitMQ.py