import numpy as np

class EdgeCluster:
    """边缘集群类
    
    初始化后生成一个边缘集群，包括所有的边缘节点和节点间网络链接
    
    Attributes:
        
       num_nodes: 
    """    
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.edge_nodes = self.generate_edge_nodes(num_nodes)
        self.edge_networks = self.generate_edge_networks(num_nodes)
        
    def generate_edge_nodes(self, num_nodes):
        """
        生成集群的所有边缘节点，并随机赋予内存、CPU供给

        Returns:
           由EdgeNode类实例组成的列表
        """
        edge_nodes = [EdgeNode(node_id=i, cpu_capacity=np.random.randint(1, 16), mem_capacity=None) 
                      for i in range(num_nodes)]
        for node in edge_nodes:
            node.mem_capacity = node.cpu_capacity * 2
        return edge_nodes

    def generate_edge_networks(self, num_nodes):
        """
        产生边缘集群的网络

        Args:
            num_nodes (int): 几乘几的二维矩阵

        Returns:
            一个单向的二维邻接矩阵A:  A[i,j]={边缘节点i到边缘节点j的传输延迟 边缘节点i到边缘节点j的带宽}
        """
        edge_networks = np.zeros((num_nodes, num_nodes), dtype=[('latency', float), ('bandwidth', float)])
        
        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                # Set latency and bandwidth for the forward direction
                edge_networks[i, j]['latency'] = np.random.uniform(1, 200)
                edge_networks[i, j]['bandwidth'] = np.random.uniform(1, 10)
                
                # Set latency and bandwidth for the reverse direction
                edge_networks[j, i]['latency'] = edge_networks[i, j]['latency']
                edge_networks[j, i]['bandwidth'] = edge_networks[i, j]['bandwidth']
        print(edge_networks)        
        return edge_networks
    
class EdgeNode:
    """
    边缘节点类
    节点具有CPU、内存资源
    """
    def __init__(self, node_id, cpu_capacity, mem_capacity):
        self.node_id = node_id
        self.cpu_capacity = cpu_capacity
        self.mem_capacity = mem_capacity
        self.occupied_resources = {'cpu': 0, 'mem': 0}
