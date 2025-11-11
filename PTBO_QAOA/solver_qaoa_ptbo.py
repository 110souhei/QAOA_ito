import qaoa_ptbo
import json
import networkx as nx

#正直ファイルの読み込みとかはすべてここで完結させたい感はあるよね


if __name__ == "__main__":


    out_file_name = "Neldermead_Parameters_8_PTBO_2"
    graph_file_name_list = ["random/random_7/10"]#,"random/random_7/9","random/random_7/10"]#,"random/random_7/9","random/random_7/10","random/random_7/11","random/random_7/12"] #,"regular/regular_3/10","regular/regular_3/12"]#"regular/regular_3/14"]#,"regular/regular_3/16","regular/regular_3/18"]
    
    qaoa_status = {}
    qaoa_status['Parameters'] = 8 # QAOAのパラメータ数(量子回路の深さ*2)
    qaoa_status['Method_name'] = "Nelder-Mead" #使用する最適化アルゴリズム
    qaoa_status['Tol'] = 1e-3#収束精度
    qaoa_status['betagamma'] = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]#,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    qaoa_status['Parameter_PCA'] = 2
    qaoa_status['Maxiter_Step1'] = 200
    

    for graph_file_name in graph_file_name_list:    
        for number in range(148,300):
            print(graph_file_name,number)
            json_open = open('in/' + graph_file_name + '/' + str(number) + 'in.json','r')
            json_load = json.load(json_open)
            G = nx.readwrite.json_graph.adjacency_graph(json_load)

            Record = qaoa_ptbo.solver(G,qaoa_status) #グラフ、QAOAのステータスを渡す

            f = open('out/'+ out_file_name + "/" + graph_file_name + '/' + str(number) + 'out.json','w')
            json.dump(Record,f,ensure_ascii=False)








