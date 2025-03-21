import subprocess
import time

def start_server(command):
    return subprocess.Popen(command, shell=True)

def start_servers(n_nodes):
    processes = []
    starting_port = 8000

    for i in range(n_nodes):
        port = starting_port + i
        processes.append(start_server(f"python -m Pyro4.naming"))
        processes.append(start_server(f"python xmlrpc/insultServer.py {port}"))
        time.sleep(2)
        processes.append(start_server(f"python pyro/insultServer.py"))
        time.sleep(2)
        #processes.append(start_server(f"python redis/insultServer.py"))
        #time.sleep(2)
        #processes.append(start_server(f"python RabbitMQ/insultServer.py"))
        #time.sleep(2)
        processes.append(start_server(f"python xmlrpc/insultFilter.py"))
        time.sleep(2)
        processes.append(start_server(f"python pyro/insultFilter.py"))
        #time.sleep(2)
        #processes.append(start_server(f"python redis/insultFilter.py"))
        #time.sleep(2)
        #processes.append(start_server(f"python RabbitMQ/insultFilter.py"))
        #time.sleep(2)
    time.sleep(5)
    return processes

def stop_servers(processes):
    for process in processes:
        process.terminate()

if __name__ == "__main__":
    for nodes in [1,2,3]:
        print(f"Running test with {nodes} nodes...")
        processes = start_servers(nodes)
        
        input("Press Enter to stop servers...")
        stop_servers(processes)