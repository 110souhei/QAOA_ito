import matplotlib.pyplot as plt
import numpy as np
import json
import nfev as nf


def x_node(num_degree : int,opt : str):
    
    data = nf.nfev(num_degree,opt)
    plt.boxplot(data, vert=True, patch_artist=True,labels=[8,9,10,11,12])

    # グラフの装飾
    plt.title(opt+ ' ' + str(num_degree) +  ' degree')
    plt.ylabel('nfev')
    plt.xlabel('nodes')
    plt.ylim(0,100)
    #plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 表示
    plt.show()


if __name__ == "__main__":
    x_node(7,'Nelder-Mead')
    x_node(7,'CG')
    x_node(7,'Powell')