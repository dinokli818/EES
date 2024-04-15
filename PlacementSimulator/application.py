class Application():
    """部署的流拓扑
    在有了拓扑和边缘集群后，提交拓扑到集群上，得到部署的流应用
    """
    def __init__(self, topology, edge_cluster):
        self.topology = topology
        self.edge_cluster = edge_cluster
        self.dp = [op.processing_time for op in topology.operators] # 辅助数组，动态规划记录
        self.dp_visited = [0] * topology.num_operators # 辅助数组，标记是否访问过
        self.next = [-1] * topology.num_operators # 辅助数组，用于存储结果

    def dp_recursive(self, i):
        """
        动态规划递归

        """
        if self.dp_visited[i]:
            return self.dp[i]
        else: 
            for j in range(self.topology.num_operators):
                if self.topology.edges[i][j] == 1:
                    temp = (
                        self.dp_recursive(j) +
                        self.topology.operators[i].processing_time +
                        + self.edge_cluster.edge_networks[self.topology.operators[i].node.node_id, 
                                                          self.topology.operators[j].node.node_id]['latency']
                        )
                    if self.dp[i] < temp:
                        self.dp[i] = temp
                        self.next[i] = j
            self.dp_visited[i] = 1
            return self.dp[i]
    
    def find_longest_path(self):
        """
        寻找部署的流应用上的最长流路径（传输延迟+处理延迟）

        Returns:
            list: 最长的liuluj
            float: 最长流路径的端到端延迟
        """
        longest_delay = 0
        longest_start = 0
        for i in range(self.topology.num_operators):
            delay = self.dp_recursive(i)
            if delay > longest_delay:
                longest_delay = delay
                longest_start = i
        return self.construct_path(longest_start), longest_delay
    
    def find_average_delay(self):
        """
        寻找所有流应用的平均端到端延迟（传输延迟+处理延迟）

        Returns:
            float: 平均流路径的端到端延迟
        """
        total_delay = 0
        total_paths = 0

        for i in range(self.topology.num_operators):
            for j in range(self.topology.num_operators):
                if i != j and self.topology.edges[i, j] == 1:
                    total_delay += self.dp_recursive(i) + self.dp_recursive(j)
                    total_paths += 1

        if total_paths == 0:
            return 0

        average_delay = total_delay / total_paths
        return average_delay
    
    def construct_path(self, start):
        path = [start]
        while self.next[start] != -1:
            start = self.next[start]
            path.append(start)
        return path
    