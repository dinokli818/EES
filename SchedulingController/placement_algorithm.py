import numpy as np

class PlacementAlgorithm:
    """
    包含多个抽象方法 存储实现的所有调度算法
    """
    @classmethod
    def random_placement(cls, topology, edge_cluster):
        """
        随机调度算法：随机把算子调度到任意节点
        """
        for i in range( topology.num_operators):
            random_node_index = np.random.randint(0, edge_cluster.num_nodes)
            topology.operators[i].node = edge_cluster.edge_nodes[random_node_index]
            topology.operators[i].node_id = random_node_index

    @classmethod
    def manual_placement(cls, topology, edge_cluster, placement):
        """
        手动调度算法：按照给定的算子放置（一个列表），算子调度到指定节点
        """
        for i in range(topology.num_operators):
            topology.operators[i].node = placement[i]
            topology.operators[i].node_id = topology.operators[i].node.node_id

    @classmethod
    def greedy_placement(cls, topology, edge_cluster):
        """
        贪心算法：
        """
        sorted_nodes = sorted(edge_cluster.edge_nodes, key=lambda node: node.cpu_capacity - node.occupied_resources['cpu'], reverse=True)

        for i in range(topology.num_operators):
            topology.operators[i].node = sorted_nodes[i]
            topology.operators[i].node_id = sorted_nodes[i].node_id

    @classmethod
    def min_load_placement(cls, topology, edge_cluster):
        """
        最小负载调度算法：
        """
        sorted_nodes = sorted(edge_cluster.edge_nodes, key=lambda node: node.occupied_resources['cpu'])

        for i in range(topology.num_operators):
            topology.operators[i].node = sorted_nodes[i]
            topology.operators[i].node_id = sorted_nodes[i].node_id

    @classmethod
    def heuristic_placement(cls, topology, edge_cluster):
        """
        启发式算法：
            考虑算子的上游和下游关系，尽量将有高通信量的算子放置在同一节点上，以减少通信延迟。
            在上下游节点中选择资源占用较小的节点，以平衡节点资源利用。
            算子的资源需求主要包括CPU和内存，考虑资源占用最大的上下游节点。
        """
        # 获取拓扑信息
        topology_structure = topology.edges
        operators = topology.operators

        # 获取边缘节点信息
        edge_nodes = edge_cluster.edge_nodes

        # 初始化节点资源利用情况
        node_resources = {node.node_id: {'cpu': 0, 'mem': 0} for node in edge_nodes}

        # 遍历算子，按照启发式规则分配节点
        for operator in operators:
            # 获取当前算子的上游和下游算子
            upstream_operators = np.where(topology_structure[:, operator.op_id] == 1)[0]
            downstream_operators = np.where(topology_structure[operator.op_id, :] == 1)[0]

            # 计算当前算子所需的资源
            required_cpu = operator.cpu_consumption
            required_mem = operator.mem_consumption

            # 找到当前算子上游和下游中资源占用最大的节点
            max_upstream_node = max(upstream_operators, key=lambda op: node_resources[op]['cpu'])
            max_downstream_node = max(downstream_operators, key=lambda op: node_resources[op]['cpu'])

            # 选择资源占用最小的节点作为放置节点
            selected_node = min([max_upstream_node, max_downstream_node], key=lambda node_id: sum(node_resources[node_id].values()))

            # 更新节点资源占用情况
            node_resources[selected_node]['cpu'] += required_cpu
            node_resources[selected_node]['mem'] += required_mem

            # 将算子放置到选定节点
            operator.node = edge_nodes[selected_node]
            operator.node_id = selected_node