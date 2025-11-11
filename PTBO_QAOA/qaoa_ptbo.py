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

import time




#メモリの使用率の計測はしていません(いつかしたい)
def optimize_qaoa(N : int, G : nx, qaoa_status) -> dict:

    start_time = time.time()
    Record = {} #記録を保存する
    PQC_time_sum = 0.0
    max_memory = 0
    PCA_time = 0.0 #PCAの実行時間
    Parameters_transfer_time = 0.0 #パラメータを変換するのにかかる時間
    #初期値,問題設定、


    #########################
    Parameters = qaoa_status['Parameters'] # QAOAのパラメータ数(量子回路の深さ*2)
    Method_name = qaoa_status['Method_name'] #使用する最適化アルゴリズム
    TOL = qaoa_status['Tol'] #収束精度
    betagamma = []
    if qaoa_status['betagamma'][0] == -1: 
        betagamma = np.random.uniform(0, np.pi, Parameters)
    else:
        betagamma = np.array(qaoa_status['betagamma'])

    Parameters_PCA = qaoa_status['Parameter_PCA']
    Maxiter_Step1 = qaoa_status['Maxiter_Step1'] 
    #betagamma = np.zeros(Parameters,dtype = float) #初期値を固定
    ########################


    #最適化経路を保存する 
    trajectory = np.zeros((100000,Parameters),dtype = float)
    trajectory_onPTBO = np.zeros((100000,Parameters_PCA), dtype = float)
    trajectory_size = 0
    trajectory_onPTBO_size = 0
    #最適化経路を保存するローカル関数
    def record_path(theta_):
        #print(xk)
        nonlocal trajectory, trajectory_size, trajectory_onPTBO,trajectory_onPTBO_size
        if(Parameters == len(theta_)):
            trajectory[trajectory_size] = theta_
            trajectory_size += 1
        else:
             trajectory_onPTBO[trajectory_onPTBO_size] = theta_
             trajectory_onPTBO_size +=1
    #betagamma = np.zeros(Parameters,dtype = float) #初期値を固定



    #評価関数(なんと時間計測機能付き)
    def get_objective_pca (theta: np.ndarray, N : int,G: nx.graph, pca : PCA) -> float:

        #theta = pca.inverse_transform(theta.reshape(1,-1))[0] #パラメータを逆変換する
        nonlocal Parameters_transfer_time, PQC_time_sum

        p = int(len(pca.components_[0])/2) #元のパラメータ数
        theta_ptbo = np.zeros(p*2)

        start_Parameter_transfer = time.time()
        #theat_ptbo = PCAで分析した固有ベクトル * パラメータ(theta)
        for pca_comp_number in range(len(pca.components_)): #何番目の固有ベクトル
             for i in range(p*2): #元の空間のどこのパラメータか
                  theta_ptbo[i] += pca.components_[pca_comp_number][i] * theta[pca_comp_number]
        end_Parameter_transfer = time.time()
        Parameters_transfer_time += end_Parameter_transfer - start_Parameter_transfer 

        start_PQC = time.time()
        beta = theta_ptbo[:p]
        gamma = theta_ptbo[p:]
        qc = PQC.get_qaoa_circuit(N,G,beta,gamma)
        sim = StatevectorSimulator()
        job = sim.run(qc)
        result = job.result().get_statevector()
        cost = PQC.cal_cost(N,G,result)
        end_PQC = time.time()
        PQC_time_sum = end_PQC - start_PQC
        return -cost

    #PQCパートの時間を計測する 
    def timed_objective(betagamma,N,G) -> float:
        nonlocal PQC_time_sum, max_memory
        start_PQC = time.time()
        cost = PQC.get_objective(betagamma,N,G)
        end_PQC = time.time()
        PQC_time_sum += end_PQC - start_PQC
        return cost
    


    #Step1
    OPTIONS = {"maxiter" : Maxiter_Step1, "disp" : False}
    ARGS = (N,G)
    result = minimize(timed_objective,x0 =  betagamma, method= Method_name, args = ARGS, options = OPTIONS, tol = TOL,callback=record_path)
    
    #記録
    Record['nfev-p1'] = int(result.nfev)
    Record['ans-p1'] = float(result.fun)

    #Step2
    OPTIONS = {"maxiter" : 100000, "disp" : False}

    start_PCA = time.time()
    pca = PCA(n_components=Parameters_PCA) #使用する主成分の本数を決定
    trajectory_sub = trajectory[:trajectory_size] #最適化経路分だけ取り出す
    pca.fit(trajectory_sub) #最適化経路をPCAを使って分析
    end_PCA = time.time()
    PCA_time += end_PCA - start_PCA
    Record['PCA_components'] = pca.components_.tolist()
    Record['PCA_variance'] = pca.explained_variance_.tolist()

    betagamma = pca.explained_variance_ #初期パラメータとして主成分の固有値に設定する場合
    #betagamma = pca.transform(betagamma.reshape(1,-1))[0] #step1パラメータを流用する場合 (多次元配列なので、

    print(betagamma)
    ARGS = (N,G,pca) # 
    result = minimize(get_objective_pca,x0 =  betagamma, method= Method_name, args = ARGS, options = OPTIONS, tol = TOL, callback = record_path)

    #記録
    Record['nfev-p2'] = int(result.nfev)
    Record['ans-p2'] = float(result.fun)


    #Step3
    OPTIONS = {"maxiter" : 100000, "disp" : False}
    ARGS = (N,G)
    
    #betagamma = pca.inverse_transform(betagamma.reshape(1,-1))[0] #パラメータを逆変換する

    start_Parameter_transfer = time.time()
    betagamma_ = np.zeros(Parameters) # 新しいbetagammaを用意(後で入れ替える)
    for pca_comp_number in range(len(pca.components_)): #何番目の固有ベクトル
         for i in range(Parameters): #元の空間のどこのパラメータか
                betagamma_[i] += pca.components_[pca_comp_number][i] * betagamma[pca_comp_number]
    betagamma = betagamma_ #最後に元の空間で探索する用のbetagamma
    end_Parameter_transfer = time.time()
    Parameters_transfer_time += end_Parameter_transfer - start_Parameter_transfer

    result = minimize(timed_objective,x0 =  betagamma, method= Method_name, args = ARGS, options = OPTIONS, tol = TOL,callback = record_path)
    
    #記録
    Record['nfev-p3'] = int(result.nfev)
    Record['ans-p3'] = float(result.fun)
    Record['trajectory'] = trajectory[:trajectory_size].tolist()
    Record['trajectory_onPTBO'] = trajectory_onPTBO[:trajectory_onPTBO_size].tolist()



    Record['PQC_time'] = PQC_time_sum
    Record['Parameter_transfer_time'] = Parameters_transfer_time
    Record['PCA_time'] = PCA_time
    end_time = time.time()
    Record['time'] = end_time - start_time
    return Record



def solver(G : nx , qaoa_status : dict) -> dict:
    Record = optimize_qaoa(len(G.nodes),G,qaoa_status) #結果をdictで受け取る
    return Record