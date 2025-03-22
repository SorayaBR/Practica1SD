import subprocess
import time

def start_server(command):
    return subprocess.Popen(command, shell=True)

def start_servers(n_nodes):
    processes = []
    starting_port_xmlrpc = 8000
    starting_port_pyro = 9091
    processes.append(start_server(f"python -m Pyro4.naming"))
    time.sleep(5)

    for i in range(n_nodes):
        xmlrpc_port = starting_port_xmlrpc + i
        pyro_port = starting_port_pyro + i
        pyro_name = f"insultService{i+1}"
        processes.append(start_server(f"python xmlrpc/insultServer.py {xmlrpc_port}"))
        time.sleep(5)
        processes.append(start_server(f"python pyro/insultServer.py {pyro_port} {pyro_name}"))
        time.sleep(5)
        #processes.append(start_server(f"python redis/insultServer.py"))
        #time.sleep(2)
        #processes.append(start_server(f"python RabbitMQ/insultServer.py"))
        #time.sleep(2)
    time.sleep(5)
    return processes

def stop_servers(processes):
    for process in processes:
        process.terminate()
        process.wait()
    print("Servers stopped...")

if __name__ == "__main__":
    for nodes in [1,2,3]:
        print(f"Running test with {nodes} nodes...")
        processes = start_servers(nodes)
        
        input("Press Enter to stop servers...")
        stop_servers(processes)