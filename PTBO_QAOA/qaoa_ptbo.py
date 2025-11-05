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
from sklearn.decomposition import PCA




#評価関数
def get_objective_pca (theta: np.ndarray, N : int,G: nx.graph, pca : PCA) -> float:

    theta = pca.inverse_transform(theta.reshape(1,-1))[0] #パラメータを逆変換する
    #print(theta)
    p = int(len(theta)/2)


    beta = theta[:p]
    gamma = theta[p:]
    qc = PQC.get_qaoa_circuit(N,G,beta,gamma)
    sim = StatevectorSimulator()
    job = sim.run(qc)
    result = job.result().get_statevector()
    cost = PQC.cal_cost(N,G,result)
    return -cost

def optimize_qaoa(N : int, G : np.ndarray) -> dict:


    Record = {} #記録を保存する
    #初期値,問題設定、

    Parameters = 8 # QAOAのパラメータ(量子回路の深さ*2)
    Parameters_PCA = 2 #PCAを使って次元を削減した後のパラメータ
    Method_name = "Nelder-Mead" #使用する最適化アルゴリズム
    TOL = 1e-3 #収束精度
    Maxiter_Step1 = 200 #Step1の回数


    #最適化経路を保存する 
    trajectory = np.zeros((100000,Parameters),dtype = float)
    trajectory_size = 0
    #最適化経路を保存するローカル関数
    def record_path(theta_):
        #print(xk)
        nonlocal trajectory, trajectory_size
        trajectory[trajectory_size] = theta_
        trajectory_size += 1

    betagamma = np.random.uniform(0, np.pi, Parameters)
    #betagamma = np.zeros(Parameters,dtype = float) #初期値を固定


    #Step1
    OPTIONS = {"maxiter" : Maxiter_Step1, "disp" : False}
    ARGS = (N,G)
    result = minimize(PQC.get_objective,x0 =  betagamma, method= Method_name, args = ARGS, options = OPTIONS, tol = TOL,callback=record_path)
    
    #記録
    Record['nfev-p1'] = int(result.nfev)
    Record['ans-p1'] = float(result.fun)

    print(Record['nfev-p1'],trajectory_size)
    print(Record['ans-p1'])
    #Step2
    OPTIONS = {"maxiter" : 5000, "disp" : False}
    pca = PCA(n_components=Parameters_PCA) #使用する主成分の本数を決定
    trajectory_sub = trajectory[:trajectory_size] #最適化経路分だけ取り出す
    pca.fit(trajectory_sub) #最適化経路をPCAを使って分析

    betagamma = pca.explained_variance_ #初期パラメータとして主成分の固有値に設定する場合
    #betagamma = pca.transform(betagamma.reshape(1,-1))[0] #step1パラメータを流用する場合 (多次元配列なので、

    print(betagamma)
    ARGS = (N,G,pca) # 
    result = minimize(get_objective_pca,x0 =  betagamma, method= Method_name, args = ARGS, options = OPTIONS, tol = TOL)

    #記録
    Record['nfev-p2'] = int(result.nfev)
    Record['ans-p2'] = float(result.fun)
    print(Record['nfev-p2'])
    print(Record['ans-p2'])


    #Step3
    OPTIONS = {"maxiter" : 5000, "disp" : False}
    ARGS = (N,G)
    betagamma = pca.inverse_transform(betagamma.reshape(1,-1))[0] #パラメータを逆変換する
    result = minimize(PQC.get_objective,x0 =  betagamma, method= Method_name, args = ARGS, options = OPTIONS, tol = TOL)
    
    #記録
    Record['nfev-p3'] = int(result.nfev)
    Record['ans-p3'] = float(result.fun)
    
    print(Record['nfev-p3'])
    print(Record['ans-p3'])
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
    for num_node in range(8,9):
            for number in range(1):
                solver(num_node,number)
                #print(number)
    #print(trajectory)

