
import numpy as np
import json
import networkx as nx


def nfev(num_node: int,opt : str) -> list:
    
    ans = [[] for i in range(5)]
    print(ans)
    for num_degree in range(5,10):
        for number in range(100):
            
            file_name = str(num_node) + "_node_" + str(num_degree) + "_degree/" + str(number)
            try:
                json_open_opt = open('../out/'+opt + '/' + file_name + 'out.json','r')
                pass
            except:
                continue
            try :
                json_load_opt = json.load(json_open_opt)
                pass
            except:
                continue
            else:
                ans[num_degree - 5].append(json_load_opt['nfev'])
    return ans




if __name__ == "__main__":
    res = nfev(8,'Powell')
    print(res)