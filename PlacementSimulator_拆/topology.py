from stream_operator import Operator
from tool import random_dag
import numpy as np


class Topology:
    """拓扑类"""     
    def __init__(self, num_operators, num_edges):
        self.num_operators = num_operators
        self.num_edges = num_edges
        self.operators = [Operator(node=None,processing_time=np.random.uniform(1, 16),
                                   cpu_consumption=np.random.uniform(1, 4),
                                   mem_consumption=np.random.uniform(1, 8),
                                    op_id=i) for i in range(self.num_operators)]
        self.edges = random_dag(self.num_operators,self.num_edges) # 利用Tool中的DAG生成算法生成边
