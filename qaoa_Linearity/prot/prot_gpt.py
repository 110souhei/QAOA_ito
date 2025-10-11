import matplotlib.pyplot as plt
import no_deg as nd
import numpy as np


def x_node_comparison_grouped_colored(num_degree: int, methods: list, nodes: list):
    """
    ノードごとに手法の結果を比較する箱ひげ図を描画し、手法ごとに色を付ける。
    
    :param num_degree: int - 次数（degree）
    :param methods: list - 手法の名前のリスト
    :param nodes: list - ノード番号のリスト
    """
    all_data = []
    positions = []
    colors = ['lightblue', 'lightgreen', 'salmon']  # 手法ごとの色
    flattened_data = []
    
    # データ収集とポジション計算
    for i, node in enumerate(nodes):
        for j, method in enumerate(methods):
            data = nd.deg_no_ans(num_degree, method)[i]  # ノードに対応するデータを取得
            flattened_data.append(data)
            positions.append(i * (len(methods) + 1) + j + 1)

    # 箱ひげ図を描画
    boxplots = plt.boxplot(flattened_data, positions=positions, patch_artist=True, widths=0.7)

    # 色を設定
    for patch, method_idx in zip(boxplots['boxes'], range(len(flattened_data))):
        color = colors[method_idx % len(methods)]
        patch.set_facecolor(color)

    # x軸ラベルを設定
    xticks = [np.mean(positions[i * len(methods):(i + 1) * len(methods)]) for i in range(len(nodes))]
    xticklabels = [f"Node {node}" for node in nodes]
    plt.xticks(ticks=xticks, labels=xticklabels, rotation=45)

    # 凡例を追加
    legend_handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]
    plt.legend(legend_handles, methods, title="Methods", loc="upper right")

    # グラフの装飾
    plt.title(f"Comparison of Methods Grouped by Nodes ({num_degree} Degree)")
    plt.ylabel("val/true_val")
    plt.xlabel("Nodes")
    plt.ylim(0.5, 1)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # グラフを表示
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    methods = ["Nelder-Mead", "CG", "Powell"]
    nodes = [8, 9, 10, 11, 12]
    x_node_comparison_grouped_colored(7, methods, nodes)
    x_node_comparison_grouped_colored(12, methods, nodes)
