from qiskit import QuantumCircuit,QuantumRegister
from qiskit_aer import StatevectorSimulator,QasmSimulator
from qiskit.converters import circuit_to_instruction
import numpy as np
import networkx as nx



def get_cost_circuit(N : int, G : np.ndarray, gamma : np.double) -> QuantumCircuit:
    qc = QuantumCircuit(N,1)
    for a,b in G.edges:
        qc.cx(a,b)
        qc.rz(gamma,b)
        qc.cx(a,b)
    return qc
def get_mixer_circuit(N : int, beta: np.double) -> QuantumCircuit:
    qc = QuantumCircuit(N,1)
    for j in range(N):
        qc.rx(2*beta,j)
    return qc


def get_qaoa_circuit(N : int, G : np.ndarray, beta: np.ndarray, gamma: np.ndarray) -> QuantumCircuit:
    p = len(beta)
    qc = QuantumCircuit(N,1)
    qc.h([i for i in range(N)])
    #print(p)
    for i in range(p): 
        
        qc.compose(get_cost_circuit(N,G,gamma[i]), inplace = True)
        qc.barrier()
        qc.compose(get_mixer_circuit(N,beta[i]), inplace = True)    
        qc.barrier()
    #print("compleat makeing quantm circit")
    #print(beta,gamma)
    #print(qc)
    return qc



#cost cal


def cal_cost(N: int, G: nx.Graph,count) -> float:
    res = 0.0
    #print(len(count))
    p = len(np.asarray(count))
    for i in range(p):
        t = (count[i].real ** 2 + count[i].imag**2)
        # print(i,t)
        for a,b in G.edges:
            if((i>>(a))&(1) != (i>>(b))&(1)):
                res += t
    return res


def get_objective(theta: np.ndarray, N : int,G: nx.graph) -> float:
    p = int(len(theta)/2)
    beta = theta[:p]
    gamma = theta[p:]
    qc = get_qaoa_circuit(N,G,beta,gamma)
    #print("state vector")
    sim = StatevectorSimulator()
    job = sim.run(qc)
    result = job.result().get_statevector()
    cost = cal_cost(N,G,result)
    print(cost)
    return -cost