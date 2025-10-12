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
import math



def jacobi(n, a):
    x0 = [1.0] * n
    while True:
        x1 = [0.0] * n

        f = False
        for i in range(n):
            x1[i] = 0.0
            for j in range(n):
                x1[i] += a[i][j] * x0[j]

        absx = 0.0
        for i in range(n):
            absx += x1[i] * x1[i]
        absx = math.sqrt(absx)

        for i in range(n):
            if abs(abs(x1[i] / absx) - abs(x0[i])) > 1e-10:
                f = True

        for i in range(n):
            x0[i] = x1[i] / absx

        #print(" ".join(str(v) for v in x0))
        if not f:
            break
    return x0


def vAv(v, A):
    n = len(v)
    res = 0.0
    for i in range(n):
        for j in range(n):
            res += v[i] * A[i][j] * v[j]
    return res


def vv(v):
    return sum(val * val for val in v)


def VV(v):
    n = len(v)
    V = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            V[i][j] = v[i] * v[j]
    return V


trajectory = []
def record_path(xk):
    trajectory.append(np.copy(xk))

def optimize_qaoa(N : int, G : np.ndarray) -> dict:
    global trajectory
    trajectory = []
    OPTIONS = {"maxiter" : 10000, "disp" : False}
    ARGS = (N,G)
    betagamma = np.random.uniform(0, np.pi, 16)

    result = minimize(go.get_objective,x0 =  betagamma, method= "Nelder-Mead", args = ARGS, options = OPTIONS, tol = 1e-4,callback=record_path)
    D = {}
    D['ans'] = -result.fun
    D['nfev'] = result.nfev

    traj_array = np.array(trajectory)

    iris_data = traj_array

    N_samples = len(iris_data)
    M_features = len(iris_data[0])

    # --- 1. 平均値の計算 (Means) ---
    means = [0.0] * M_features
    for j in range(M_features):
        feature_sum = 0.0
        for i in range(N_samples):
            feature_sum += iris_data[i][j]
        means[j] = feature_sum / N_samples

    #print("--- 1. 平均値 (Means) ---")
    #print([f"{m:.4f}" for m in means])
    #print("-------------------------")

    # --- 2. データの中心化 (Centered Data) ---
    centered_data = []
    for i in range(N_samples):
        sample = []
        for j in range(M_features):
            sample.append(iris_data[i][j] - means[j])
        centered_data.append(sample)

# --- 3. 共分散行列の計算 (Covariance Matrix) ---
    covariance_matrix = [[0.0] * M_features for _ in range(M_features)]
    denominator = N_samples - 1 # 分母は N-1 (標本共分散)

    for i in range(M_features):
        for j in range(M_features):
            sum_of_products = 0.0
            # C[i][j] = sum_{k=1}^N (X[k][i] * X[k][j]) / (N-1)
            for k in range(N_samples):
                # i列目のデータとj列目のデータの積の和
                sum_of_products += centered_data[k][i] * centered_data[k][j]
        
            covariance_matrix[i][j] = sum_of_products / denominator

# --- 4. 結果の出力 ---
    #print("\n--- 2. 共分散行列 (Covariance Matrix) ---")
    #for row in covariance_matrix:
    #    print([f"{val:.4f}" for val in row])
    #print("------------------------------------------")


    n = M_features
    d = covariance_matrix
    p = []
    r_list = []
    for i in range(n):
        p.append(jacobi(n, d))
        r = vAv(p[i], d)
        #print("r", r)
        r_list.append(r)

        V = VV(p[i])
        for ii in range(n):
            for jj in range(n):
                d[ii][jj] -= V[ii][jj] * r

    #for i in r_list:
    #    print(i/sum(r_list))

    D['pca'] = float((r_list[0] + r_list[1])/sum(r_list))
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
                print(number)
    print(trajectory)

