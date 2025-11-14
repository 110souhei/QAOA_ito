import json
import matplotlib.pyplot as plt
import numpy as np

# データ格納用リスト
nfev_nm = []
nfev_pca_p1 = []
nfev_pca_p2 = []
nfev_pca_p3 = []

for i in range(100):
    try:
        # Nelder-Mead
        with open(f"out/Nelder-Mead/8/{i}out.json", "r") as f1:
            data_nm = json.load(f1)
        nfev_nm.append(data_nm.get("nfev", np.nan))

        # Nelder-PCA
        with open(f"out/Nelder-pca/8/{i}out.json", "r") as f2:
            data_pca = json.load(f2)

        p1 = data_pca.get("nfev-p1", 0)
        p2 = data_pca.get("nfev-p2", 0)
        p3 = data_pca.get("nfev-p3", 0)

        # 累積値として保存
        nfev_pca_p1.append(p1)
        nfev_pca_p2.append(p1 + p2)
        nfev_pca_p3.append(p1 + p2 + p3)

    except Exception as e:
        print(f"skip {i}: {e}")
        nfev_nm.append(np.nan)
        nfev_pca_p1.append(np.nan)
        nfev_pca_p2.append(np.nan)
        nfev_pca_p3.append(np.nan)

# ===== 箱ひげ図の作成 =====
plt.figure(figsize=(8,6))
plt.boxplot(
    [nfev_nm, nfev_pca_p1, nfev_pca_p2, nfev_pca_p3],
    labels=["Nelder-Mead", "PCA p1", "PCA p2", "PCA p3"],
    patch_artist=True,
    boxprops=dict(facecolor='lightgreen', color='black'),
    medianprops=dict(color='red', linewidth=2),
    whiskerprops=dict(color='black'),
    capprops=dict(color='black')
)

plt.ylabel("Execution count / time")
plt.title("Distribution of execution time (nfev) for Nelder-Mead and PCA")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
