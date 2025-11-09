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





def optimize_qaoa(N : int, G : np.ndarray, qaoa_status : dict) -> dict:


    Record = {} #計算記録を保存する
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
    #betagamma = np.zeros(Parameters,dtype = float) #初期値を固定
    ########################



    #最適化経路を保存する 
    trajectory = np.zeros((100000,Parameters),dtype = float)
    trajectory_size = 0
    #最適化経路を保存するローカル関数
    def record_path(theta_):
        nonlocal trajectory, trajectory_size
        print(theta_)
        trajectory[trajectory_size] = theta_
        trajectory_size += 1

    #Step1
    OPTIONS = {"maxiter" : 100000, "disp" : False}
    ARGS = (N,G)
    print("start optimize")
    result = minimize(PQC.get_objective,x0 =  betagamma, method= Method_name, args = ARGS, options = OPTIONS, tol = TOL,callback=record_path)
    
    #記録
    Record['nfev'] = int(result.nfev)
    Record['ans'] = float(result.fun)
    Record['trajectory'] = trajectory.tolist()

    return Record



def solver(G : nx, qaoa_status: dict) -> dict:
    print("start solve")
    Record = optimize_qaoa(len(G.nodes),G, qaoa_status) #結果をdictで受け取る
    return Record
