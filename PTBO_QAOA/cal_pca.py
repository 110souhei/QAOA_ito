import json
import os
import numpy as np

def average_pca(num_node: int):
    base_dir = f"out/Nelder-Mead/{num_node}/"
    pca_values = []

    for i in range(100):
        file_path = os.path.join(base_dir, f"{i}out.json")
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} が見つかりません。スキップします。")
            continue
        
        with open(file_path, "r") as f:
            data = json.load(f)
            if 'pca' in data:
                pca_values.append(data['pca'])
            else:
                print(f"Warning: {file_path} に'pca'がありません。")

    if pca_values:
        avg_pca = np.mean(pca_values)
        print(f"{num_node}ノードにおける平均PCA値: {avg_pca:.6f}")
        return avg_pca
    else:
        print("有効なデータがありません。")
        return None

if __name__ == "__main__":
    average_pca(8)
