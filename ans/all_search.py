import networkx as nx
import json
import numpy as np

def get_graph(num_nodes : int, edge_prob : int, number : int) :
    
    d = {}
    
    # ランダムグラフの生成
    #print(num_nodes,edge_prob,number)
    #d = nx.readwrite.json_graph.adjacency_data(G)
    file_name = str(num_nodes) + "_node_" + str(edge_prob) + "_degree/" + str(number)
    json_open = open("../in/" + file_name + "in.json",'r')
    #print(file_name)
    json_load = json.load(json_open)
    #print(json_load)
    G = nx.readwrite.json_graph.adjacency_graph(json_load)
    
    N = len(G.nodes)
    
    max_res = 0
    for i in range((1<<N)):
        res = 0
        for a,b in G.edges:
            if((i>>(a))&(1) != (i>>(b)&(1))):
                res += 1
        
        if(res > max_res):
            max_res = res
    
    json_write = open(file_name + "out.json",'w')
    d['ans'] = max_res
    json.dump(d,json_write,ensure_ascii=False)
    return


if __name__ == "__main__":
    
    for num_nodes in range(8,17):
        for edge_prob in range(5,10):
            for number in range(100):
                get_graph(num_nodes,edge_prob,number)
