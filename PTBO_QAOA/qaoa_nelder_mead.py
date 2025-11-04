from qiskit import QuantumCircuit,QuantumRegister
import matplotlib.pyplot as plt
from qiskit.visualization import plot_state_city
from qiskit_aer import StatevectorSimulator,QasmSimulator
from qiskit.converters import circuit_to_instruction
from scipy.optimize import minimize
import numpy as np
import json
import networkx as nx
import get_objective as go
import PCA as pc
import math




trajectory = []
def record_path(xk):
    trajectory.append(np.copy(xk))

def get_objective_pca (theta: np.ndarray, N : int,G: nx.graph, P,means,m) -> float:
    p = pc.inv(theta,P,means)
    p = int(len(theta)/2)
    beta = theta[:p]
    gamma = theta[p:]
    qc = go.get_qaoa_circuit(N,G,beta,gamma)
    #print("state vector")
    sim = StatevectorSimulator()
    job = sim.run(qc)
    result = job.result().get_statevector()
    cost = go.cal_cost(N,G,result)
    return -cost

def optimize_qaoa(N : int, G : np.ndarray) -> dict:
    global trajectory
    trajectory = []
    
    OPTIONS = {"maxiter" : 5000, "disp" : False}
    ARGS = (N,G)
    betagamma = np.random.uniform(0, np.pi, 8)

    result = minimize(go.get_objective,x0 =  betagamma, method= "Nelder-Mead", args = ARGS, options = OPTIONS, tol = 1e-3,callback=record_path)
    D ={}
    D['ans'] = result.fun
    D['nfev'] = result.nfev    

    return D



def solver(num_node: int , number: int):
    file_name = str(num_node) + "/" + str(number)
    json_open = open('in/' + file_name + 'in.json','r')
    json_load = json.load(json_open)
    #print(json_load)
    G = nx.readwrite.json_graph.adjacency_graph(json_load)
    res = optimize_qaoa(len(G.nodes),G)
    f = open('out/Nelder-Mead/' + file_name + 'out.json','w')
    
    json.dump(res,f,ensure_ascii=False)
    

if __name__ == "__main__":
    for num_node in range(8,9):
            for number in range(100):
                solver(num_node,number)
                #print(number)
    #print(trajectory)

