import json
import matplotlib.pyplot as plt
import numpy as np
import os

ratios_nm = []       # Nelder-Mead
ratios_pca_p1 = []   # PCA ans-p1
ratios_pca_p2 = []   # PCA ans-p2
ratios_pca_p3 = []   # PCA ans-p3

for i in range(100):  # 問題番号 0~99
    try:
        # ファイル読み込み
        with open(f"out/Nelder-Mead/8/{i}out.json", "r") as f1:
            data_nm = json.load(f1)
        with open(f"out/ans/8/{i}out.json", "r") as f2:
            data_ans = json.load(f2)
        with open(f"out/Nelder-pca/8/{i}out.json", "r") as f3:
            data_pca = json.load(f3)

        # ----------------------------
        # Nelder-Mead 比率
        nm_val = np.array(data_nm["ans"], dtype=float)
        ans_val = np.array(data_ans["ans"], dtype=float)
        ratio_nm = np.mean(-nm_val / ans_val)
        ratios_nm.append(ratio_nm)

        # ----------------------------
        # PCA 比率
        for key, lst in zip(
            ["ans-p1", "ans-p2", "ans-p3"],
            [ratios_pca_p1, ratios_pca_p2, ratios_pca_p3]
        ):
            if key in data_pca:
                pca_val = np.array(data_pca[key], dtype=float)
                ratio_pca = np.mean(-pca_val / ans_val)  # 正解は ans_val
                lst.append(ratio_pca)
            else:
                lst.append(np.nan)  # データがなければ nan

    except Exception as e:
        print(f"skip {i}: {e}")

# ===== 箱ひげ図 =====
plt.figure(figsize=(8,6))
plt.boxplot(
    [ratios_nm, ratios_pca_p1, ratios_pca_p2, ratios_pca_p3],
    labels=["Nelder-Mead", "PCA p1", "PCA p2", "PCA p3"],
    patch_artist=True,
    boxprops=dict(facecolor='lightblue', color='black'),
    medianprops=dict(color='red', linewidth=2)
)
plt.ylabel("Solution / ans")
plt.title("Solution ratio distribution (Nelder-Mead vs PCA)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
