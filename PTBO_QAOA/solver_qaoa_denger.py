import os
import qaoa
import json
import networkx as nx

if __name__ == "__main__":
    out_file_name = "Neldermead_Parameters_6"
    graph_file_name = "random/random_7/7"

    # QAOA設定
    qaoa_status = {
        'Parameters': 6,  # QAOAのパラメータ数(量子回路の深さ*2)
        'Method_name': "Nelder-Mead",  # 使用する最適化アルゴリズム
        'Tol': 1e-3,  # 収束精度
        'betagamma': [0.5] * 6  # 初期値
    }

    # 入力・出力のベースディレクトリ
    input_dir = os.path.join("in", graph_file_name)
    output_dir = os.path.join("out", out_file_name, graph_file_name)

    # 出力ディレクトリを自動生成（存在してもOK）
    os.makedirs(output_dir, exist_ok=True)

    for number in range(300):
        # 入力ファイルパス
        input_path = os.path.join(input_dir, f"{number}in.json")
        output_path = os.path.join(output_dir, f"{number}out.json")

        # 入力ファイルが存在しない場合はスキップ（安全対策）
        if not os.path.exists(input_path):
            print(f"⚠️ Skipped: {input_path} (not found)")
            continue

        # グラフをロード
        with open(input_path, 'r') as json_open:
            json_load = json.load(json_open)
            G = nx.readwrite.json_graph.adjacency_graph(json_load)

        # QAOAを実行
        Record = {} #failの生成だけを行う場合
        #Record = qaoa.solver(G, qaoa_status)

        # 結果を保存
        with open(output_path, 'w') as f:
            json.dump(Record, f, ensure_ascii=False)

        print(f"✅ Saved: {output_path}")
