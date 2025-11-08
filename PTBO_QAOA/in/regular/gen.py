import networkx as nx
import json
import numpy as np
import os

def gen_graph(num_nodes : int,regular : int ,number : int):
    
    d = {}
    
    # ランダムグラフの生成
    G = nx.random_regular_graph(regular,num_nodes)
    print(num_nodes,number)
    #d = nx.readwrite.json_graph.adjacency_data(G)
    
    file_name = "regular_" + str(regular) + "/" + str(num_nodes)+ "/" + str(number) + "in.json"
    
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            f.write("新しいファイルを作成しました。\n")
        print(f"{file_name} を作成しました。")
    else:
        print(f"{file_name} はすでに存在します。")


    f = open(file_name,'w')
    
    d = nx.readwrite.json_graph.adjacency_data(G)
    json.dump(d,f,ensure_ascii=False)


if __name__ == "__main__":
    
    for num_nodes in range(7,21):
        for regular in range(3,num_nodes):
            if((num_nodes * regular)%2 == 0):
                for number in np.arange(0,300):
                    gen_graph(num_nodes,regular,number)