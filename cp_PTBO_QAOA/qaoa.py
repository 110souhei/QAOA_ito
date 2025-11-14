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
import time

#最大使用メモリの測定
import psutil
import threading
import os




def optimize_qaoa(N : int, G : nx, qaoa_status : dict, answer : list) -> dict:
    start_time = time.time() #全体の実行時間
    PQC_time_sum = 0.0 #実行時間のうち量子回路の実行時間の総和
    max_memory = 0 #最大のメモリ使用量 (量子回路を実行する際に確認する)
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
        trajectory[trajectory_size] = theta_
        trajectory_size += 1

    #量子回路の実行時間を計測する用の関数(optimaizaの評価関数をこれにしてね)
    def timed_objective(betagamma,N,G,answer) -> float:
        nonlocal PQC_time_sum, max_memory
        start_PQC = time.time()
        cost = PQC.get_objective(betagamma,N,G,answer)
        end_PQC = time.time()
        PQC_time_sum += end_PQC - start_PQC
        return cost
    
    #メモリの使用率を監視する関数(0.01秒ごとにメモリの値をとっている)
    max_mem = 0
    process = psutil.Process(os.getpid())
    def monitor_mem(initial_time,event):
        nonlocal max_mem
        while not event.wait(0.01):
            mem = process.memory_info().rss
            if( max_mem < mem):
                max_mem = mem
 
    event = threading.Event()
    initial_time = time.time()

    moniter_mem_start = threading.Thread(target=monitor_mem,args=((start_time,event)))
    moniter_mem_start.start()# メモリ使用量の測定開始


    #Step1
    OPTIONS = {"maxiter" : 100000, "disp" : False}
    ARGS = (N,G,answer)
    #print("start optimize")
    result = minimize(timed_objective,x0 =  betagamma, method= Method_name, args = ARGS, options = OPTIONS, tol = TOL,callback=record_path)
    
    #記録
    Record['nfev'] = int(result.nfev)
    Record['ans'] = float(result.fun)
    Record['trajectory'] = trajectory[:trajectory_size].tolist()
    
    end_time = time.time()
    Record['qaoa_time'] = end_time - start_time
    Record['PQC_time'] = PQC_time_sum

    #print(max_mem)
    event.set() #メモリ計測の終了

    Record['max_mem'] = max_mem
    return Record



def solver(G : nx, qaoa_status: dict, answer : list) -> dict:
    print("start solve")
    Record = optimize_qaoa(len(G.nodes),G, qaoa_status, answer) #結果をdictで受け取る
    return Record
