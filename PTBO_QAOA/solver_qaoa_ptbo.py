import qaoa_ptbo
import json
import networkx as nx
import time

#正直ファイルの読み込みとかはすべてここで完結させたい感はあるよね


if __name__ == "__main__":


    #out_file_name = "Neldermead_Parameters_8_PTBO_2"
    #graph_file_name_list = ["random/random_7/10"]#,"random/random_7/9","random/random_7/10"]#,"random/random_7/9","random/random_7/10","random/random_7/11","random/random_7/12"] #,"regular/regular_3/10","regular/regular_3/12"]#"regular/regular_3/14"]#,"regular/regular_3/16","regular/regular_3/18"]

    #11/10    
    #qaoa_status = {}
    #qaoa_status['Parameters'] = 8 # QAOAのパラメータ数(量子回路の深さ*2)
    #qaoa_status['Method_name'] = "Nelder-Mead" #使用する最適化アルゴリズム
    #qaoa_status['Tol'] = 1e-3#収束精度
    #qaoa_status['betagamma'] = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]#,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    #qaoa_status['Parameter_PCA'] = 2
    #qaoa_status['Maxiter_Step1'] = 200

    #11/11
    qaoa_status = {}
    qaoa_status['Parameters'] = 8 # QAOAのパラメータ数(量子回路の深さ*2)
    qaoa_status['Tol'] = 1e-3#収束精度
    qaoa_status['betagamma'] = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]#,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    qaoa_status['Parameter_PCA'] = 2
    qaoa_status['Maxiter_Step1'] = 200

    graph_file_name_list = ["random/random_7/8","random/random_7/9","random/random_7/10","random/random_7/11","random/random_7/12"] 
    #手法だけ変えて比較する    
    #out_file_name = "CG_Parameters_8_PTBO_2_aizu" #手法、パラメータ数,計算機
    #qaoa_status['Method_name'] = "CG" #使用する最適化アルゴリズム
    out_file_name = "Nelder-Mead_Parameters_8_PTBO_2_aizu" #手法、パラメータ数,計算機
    qaoa_status['Method_name'] = "Nelder-Mead" #使用する最適化アルゴリズム
    #out_file_name = "Powell_Parameters_8_PTBO_2aizu" #手法、パラメータ数,計算機
    #qaoa_status['Method_name'] = "Powell" #使用する最適化アルゴリズム

    start_time = time.time()
    time_limit = 8 * 3600
    for graph_file_name in graph_file_name_list:    
        for number in range(300):
            print(out_file_name,graph_file_name,number)
            json_open = open('in/' + graph_file_name + '/' + str(number) + 'in.json','r')
            json_load = json.load(json_open)
            G = nx.readwrite.json_graph.adjacency_graph(json_load)


            #answerのデータのロード
            answer_open = open('out/all_search/' + graph_file_name + '/' + str(number) + 'out.json','r')
            print('out/all_search/' + graph_file_name + '/' + str(number) + 'out.json')
            answer_dict = json.load(answer_open)
            answer = answer_dict['Max_cut_value']

            Record = qaoa_ptbo.solver(G,qaoa_status,answer) #グラフ、QAOAのステータスを渡す

            f = open('out/'+ out_file_name + "/" + graph_file_name + '/' + str(number) + 'out.json','w')
            json.dump(Record,f,ensure_ascii=False)
            
            end_time = time.time()
            if(time_limit < end_time - start_time):
                print("制限時間に達したため終了します" + 'out/'+ out_file_name + "/" + graph_file_name + '/' + str(number) + 'out.json','w')









