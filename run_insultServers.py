import subprocess
import time
import os
import signal

def start_server(command):
    return subprocess.Popen(command, shell=True)

def add_servers(n_nodes, processes):
    ports_xmlrpc = [8000, 8001, 8002]
    ports_pyro = [9091, 9092, 9093]
    ports_redis = [6379, 6380, 6381]
    
    pyro_name = f"insultService{n_nodes}"

    if n_nodes == 1:
        xmlrpc_port = ports_xmlrpc[0]
        pyro_port = ports_pyro[0]
        redis_port = ports_redis[0]
        processes.append(start_server(f"python xmlrpc/insultServer.py {xmlrpc_port}"))
        time.sleep(3)
        processes.append(start_server(f"python pyro/insultServer.py {pyro_port} {pyro_name}"))
        time.sleep(3)
        processes.append(start_server(f"python redis/insultServer.py {redis_port}"))
        time.sleep(3)
    elif n_nodes == 2:
        xmlrpc_port = ports_xmlrpc[1]
        pyro_port = ports_pyro[1]
        redis_port = ports_redis[1]
        processes.append(start_server(f"python xmlrpc/insultServer.py {xmlrpc_port}"))
        time.sleep(3)
        processes.append(start_server(f"python pyro/insultServer.py {pyro_port} {pyro_name}"))
        time.sleep(3)
        processes.append(start_server(f"python redis/insultServer.py {redis_port}"))
        time.sleep(3)
    elif n_nodes == 3:
        xmlrpc_port = ports_xmlrpc[2]
        pyro_port = ports_pyro[2]
        redis_port = ports_redis[2]
        processes.append(start_server(f"python xmlrpc/insultServer.py {xmlrpc_port}"))
        time.sleep(3)
        processes.append(start_server(f"python pyro/insultServer.py {pyro_port} {pyro_name}"))
        time.sleep(3)
        processes.append(start_server(f"python redis/insultServer.py {redis_port}"))
        time.sleep(3)
    return processes

def stop_servers(processes):
    for process in processes:
        os.kill(process.pid, signal.SIGTERM) 
        process.wait()
    print("Servers stopped...")


if __name__ == "__main__":
    processes = []
    processes.append(start_server(f"python -m Pyro4.naming"))
    time.sleep(5)
    print(f"Running test with 1 node...")
    processes = add_servers(1, processes)

    input("Press Enter to add a second server...")
    add_servers(2, processes)

    input("Press Enter to add a third server...")
    add_servers(3, processes)

    input("Press Enter to stop servers...") 
    stop_servers(processes)