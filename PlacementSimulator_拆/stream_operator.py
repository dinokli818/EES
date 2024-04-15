class Operator:
    """算子类"""     
    def __init__(self, processing_time=None, cpu_consumption=None, mem_consumption = None, node=None, op_id=None, node_id=None):
        self.op_id = op_id
        self.node = node  # 算子调度到的边缘节点
        self.node_id = node_id
        self.processing_time = processing_time
        self.cpu_consumption = cpu_consumption
        self.mem_consumption = mem_consumption
