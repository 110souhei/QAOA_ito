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



def optimize_qaoa(N : int, G : np.ndarray) -> dict:
    OPTIONS = {"maxiter" : 10000, "disp" : False}
    ARGS = (N,G)
    betagamma = np.zeros(1*2)
    
    result = minimize(go.get_objective,x0 =  betagamma, method= "CG", args = ARGS, options = OPTIONS, tol = 1e-4)
    d = {}
    d['ans'] = -result.fun
    d['nfev'] = result.nfev
    return d



def solver(num_node: int , num_degree: int, number: int):
    file_name = str(num_node) + "_node_" + str(num_degree) + "_degree/" + str(number)
    json_open = open('../in/' + file_name + 'in.json','r')
    json_load = json.load(json_open)
    #print(json_load)
    G = nx.readwrite.json_graph.adjacency_graph(json_load)
    res = optimize_qaoa(len(G.nodes),G)
    f = open('out/CG/' + file_name + 'out.json','w')
    
    json.dump(res,f,ensure_ascii=False)
    

if __name__ == "__main__":
    
    for num_node in range(8,17):
        for num_degree in range(5,10):
            for number in range(1):
                solver(num_node,num_degree,number)
