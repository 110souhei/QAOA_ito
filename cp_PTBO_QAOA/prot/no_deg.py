import numpy as np
import json
import networkx as nx


def no_deg_ans(num_node: int,opt : str) -> list:
    
    ans = [[] for i in range(5)]
    print(ans)
    for num_degree in range(5,10):
        for number in range(100):
            file_name = str(num_node) + "_node_" + str(num_degree) + "_degree/" + str(number)
            
            json_open_ans = open('../../ans/' + file_name + 'out.json','r')
            json_load_ans = json.load(json_open_ans)
            
            json_open_opt = open('../out/'+opt + '/' + file_name + 'out.json','r')
            try :
                json_load_opt = json.load(json_open_opt)
                pass
            except:
                continue
            else:
                ans[num_degree - 5].append(json_load_opt['ans']/json_load_ans['ans'])
    return ans


def deg_no_ans(num_degree: int,opt : str) -> list:
    
    ans = [[] for i in range(5)]
    for num_node in range(8,13):
        for number in range(100):
            file_name = str(num_node) + "_node_" + str(num_degree) + "_degree/" + str(number)
            json_open_ans = open('../../ans/' + file_name + 'out.json','r')
            json_load_ans = json.load(json_open_ans)
            
            json_open_opt = open('../out/'+opt + '/' + file_name + 'out.json','r')
            
            try :
                json_load_opt = json.load(json_open_opt)
                pass
            except:
                continue
            else:
                ans[num_node - 8].append(json_load_opt['ans']/json_load_ans['ans'])
    return ans


if __name__ == "__main__":
    res = no_deg_ans(8,'Powell')
    print(res)
    
    #res = deg_no_ans(7,'Nelder-Mead')
    #print(res)