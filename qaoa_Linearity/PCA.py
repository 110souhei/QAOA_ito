import numpy as np
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

def PCA(trajectory):
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
    return (r_list, p, means)

def tr(x,means,p,m):
    y = []
    n = int(len(x))
    for i in range(m):
        c = 0.0
        for j in range(n):
            c += (x[j] - means[j]) * p[i][j]
        y.append(c)
    return y

def inv(y,p,means):
    n = int(len(means))
    m = int(len(y))

    x = []

    for i in range(n):

        c = 0.0
        for j in range(m):
            c += y[j] * p[j][i]
        x.append(means[i] + c)

    return x

def pca_proter(means,p):

    #地域については考察する必要がある

    for i in range(200):
        for j in range(200):
            