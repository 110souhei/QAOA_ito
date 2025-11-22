import os
import json
import matplotlib.pyplot as plt

def load_json_range(directory, start=0, end=300, target_key=None):
    values = []

    for i in range(start, end):
        fname = os.path.join(directory, f"{i}out.json")
        if not os.path.exists(fname):
            print(f"Warning: {fname} not found, skipping.")
            continue

        with open(fname, "r") as f:
            data = json.load(f)

        if target_key not in data:
            print(f"Warning: key '{target_key}' not in {fname}, skipping.")
            continue

        values.append(data[target_key])

    return values


def plot_box(values, key_name):
    plt.figure(figsize=(6, 4))
    plt.boxplot(values)
    plt.ylabel(key_name)
    plt.title(f"Boxplot of '{key_name}'")
    plt.grid(True)
    plt.show()


# -----------------------------
# 使用例
# -----------------------------
directory = "../out/Neldermead_Parameters_2/regular/regular_3/10"
target_key = "nfev"   # ← ここをプロットしたいキー名に変える

values = load_json_range(directory, start=0, end=300, target_key=target_key)

if values:
    plot_box(values, target_key)
else:
    print("No valid data found.")
