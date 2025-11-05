from qiskit import QuantumCircuit,QuantumRegister
import matplotlib.pyplot as plt
from qiskit.visualization import plot_state_city
from qiskit_aer import StatevectorSimulator,QasmSimulator
from qiskit.converters import circuit_to_instruction
from scipy.optimize import minimize
import numpy as np
import json
import networkx as nx
import PQC  #パラメータ付量子回路
import math





def optimize_qaoa(N : int, G : np.ndarray) -> dict:


    Record = {} #計算記録を保存する
    #初期値,問題設定、

    #########################
    Parameters = 16 # QAOAのパラメータ数(量子回路の深さ*2)
    Method_name = "Nelder-Mead" #使用する最適化アルゴリズム
    TOL = 1e-3 #収束精度

    betagamma = np.random.uniform(0, np.pi, Parameters)
    #betagamma = np.zeros(Parameters,dtype = float) #初期値を固定
    ########################



    #最適化経路を保存する 
    trajectory = np.zeros((100000,Parameters),dtype = float)
    trajectory_size = 0
    #最適化経路を保存するローカル関数
    def record_path(xk):
        #print(xk)
        nonlocal trajectory, trajectory_size
        trajectory[trajectory_size] = xk
        trajectory_size += 1

    #Step1
    OPTIONS = {"maxiter" : 50000, "disp" : False}
    ARGS = (N,G)
    result = minimize(PQC.get_objective,x0 =  betagamma, method= Method_name, args = ARGS, options = OPTIONS, tol = TOL,callback=record_path)
    
    #記録
    Record['nfev'] = int(result.nfev)
    Record['ans'] = float(result.fun)

    return Record



def solver(num_node: int , number: int):
    #problem(解きたいグラフ)の情報をload
    file_name = str(num_node) + "/" + str(number)
    json_open = open('in/' + file_name + 'in.json','r')
    json_load = json.load(json_open)
    G = nx.readwrite.json_graph.adjacency_graph(json_load)
    
    Record = optimize_qaoa(len(G.nodes),G) #結果をdictで受け取る
    f = open('out/Nelder-pca/' + file_name + 'out.json','w') 
    json.dump(Record,f,ensure_ascii=False)
    

if __name__ == "__main__":
    for num_node in range(16,17):
            for number in range(1):
                solver(num_node,number)
                #print(number)
    #print(trajectory)

