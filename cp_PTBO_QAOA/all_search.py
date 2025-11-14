import networkx as nx
import json
import numpy as np

def all_search(G : nx) :
    
    result = {}  #結果の保存
    
    N = len(G.nodes)
    Max_cut_value = np.zeros(1<<(N)).tolist()
    max_res = 0
    for i in range((1<<N)):
        res = 0
        for a,b in G.edges:
            if((i>>(a))&(1) != (i>>(b)&(1))):
                res += 1
        
        if(res > max_res):
            max_res = res
        Max_cut_value[i] = res
    
    result['Max_cut_value'] = Max_cut_value
    result['ans'] = max_res
    
    return result


if __name__ == "__main__":
    #入力ファイル

    #graph_file_name_list = ["random/random_7/8","random/random_7/9","random/random_7/10","random/random_7/11","random/random_7/12"] #,"regular/regular_3/10","regular/regular_3/12"]#"regular/regular_3/14"]#,"regular/regular_3/16","regular/regular_3/18"]
    #input_file_name_list =  ["regular/regular_3/8","regular/regular_3/10","regular/regular_3/12","regular/regular_3/14","regular/regular_3/16","regular/regular_3/18"]
    for input_file_name in input_file_name_list:
        for i in range(300):
            json_open = open("in/" + input_file_name + "/" +  str(i) + "in.json",'r')
            print(input_file_name +'/'+ str(i))
            json_load = json.load(json_open)
            G = nx.readwrite.json_graph.adjacency_graph(json_load)
            result = all_search(G)
            json_write = open("out/all_search/" + input_file_name + "/" + str(i) + "out.json",'w')
            json.dump(result,json_write,ensure_ascii=False)