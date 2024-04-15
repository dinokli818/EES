import numpy as np
from random import shuffle as sl  
from random import randint as rd    
 #node节点数量，edge边数量 
def random_dag(node,edge):

    n = node
    node = range(0,n)   
    node = list(node)  
    
    sl(node)  #生成拓扑排序
    m = edge
    result = [] #存储生成的边，边用tuple的形式存储
    
    appeared_node = []
    not_appeared_node = node
    #生成前n - 1条边  
    while len(result) != n - 1:
        #生成第一条边
        if len(result) == 0:
            p1 = rd(0,n - 2)
            p2 = rd(p1+1,n - 1)
            x = node[p1]
            y = node[p2]
            appeared_node.append(x)
            appeared_node.append(y)
            not_appeared_node = list(set(node).difference(set(appeared_node)))
            result.append((x,y))
        #生成后面的边
        else:
            p1 = rd(0,len(appeared_node) - 1)
            x = appeared_node[p1]#第一个点从已经出现的点中选择
            p2 = rd(0,len(not_appeared_node) - 1)
            y = not_appeared_node[p2]
            appeared_node.append(y)#第二个点从没有出现的点中选择
            not_appeared_node = list(set(node).difference(set(appeared_node)))
     #必须保证第一个点的排序在第二个点之前
            if node.index(y) < node.index(x):
                result.append((y,x))
            else:
                result.append((x,y))
   #生成后m - n + 1条边     
    while len(result) != m:
        p1 = rd(0,n - 2)
        p2 = rd(p1+1,n - 1)
        x = node[p1]
        y = node[p2]
    #如果该条边已经生成过，则重新生成
        if (x,y) in result:
            continue
        else:
            result.append((x,y))
    
    matrix = np.zeros((n,n))
    for i in range(len(result)):
        matrix[result[i][0],result[i][1]] = 1

    return matrix
