import qaoa
import json
import networkx as nx

#正直ファイルの読み込みとかはすべてここで完結させたい感はあるよね


if __name__ == "__main__":


    out_file_name = "Neldermead_Parameters_20"
    graph_file_name = "random/random_7/20"
    qaoa_status = {}
    qaoa_status['Parameters'] = 20 # QAOAのパラメータ数(量子回路の深さ*2)
    qaoa_status['Method_name'] = "Nelder-Mead" #使用する最適化アルゴリズム
    qaoa_status['Tol'] = 1e-3#収束精度
    qaoa_status['betagamma'] = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

    for number in range(300):
    



        json_open = open('in/' + graph_file_name + '/' + str(number) + 'in.json','r')
        json_load = json.load(json_open)
        G = nx.readwrite.json_graph.adjacency_graph(json_load)

        Record = qaoa.solver(G,qaoa_status) #グラフ、QAOAのステータスを渡す

        f = open('out/'+ out_file_name + "/" + graph_file_name + '/' + str(number) + 'out.json','w')
        json.dump(Record,f,ensure_ascii=False)








