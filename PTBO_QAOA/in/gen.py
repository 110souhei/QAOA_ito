import networkx as nx
import json
import numpy as np

def gen_graph(num_nodes : int, number : int):
    
    d = {}
    
    # ランダムグラフの生成
    G = nx.erdos_renyi_graph(num_nodes,0.7)
    print(num_nodes,number)
    #d = nx.readwrite.json_graph.adjacency_data(G)
    
    file_name = str(num_nodes) + "/" + str(number) + "in.json"
    f = open(file_name,'w')
    
    d = nx.readwrite.json_graph.adjacency_data(G)
    json.dump(d,f,ensure_ascii=False)


if __name__ == "__main__":
    
    for num_nodes in range(9,21):
        for number in np.arange(0,300):
                gen_graph(num_nodes,number)