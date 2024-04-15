
from placement_algorithm import PlacementAlgorithm

class Scheduler:
    """
    调度器类
    执行调度，并且检查算子放置的合法性，
    """
    @classmethod
    def place_topology_on_cluster(self, stream_app, resource_limit):
        placement_algorithm = PlacementAlgorithm()
        placement_algorithm.random_placement(stream_app.topology, stream_app.edge_cluster) # 生成调度
        if not self.check_resource_constraints(stream_app, resource_limit): # 如果调度不合法
            return False
        else: #若调度合法，则返回True
            return True
            
    @classmethod
    def check_resource_constraints(self, stream_app, resource_limit):
        topology = stream_app.topology
        edge_cluster =  stream_app.edge_cluster
        if resource_limit:  # Only check constraints when resource_limit is True
            self.clear_occupied_resource(edge_cluster) # 清除边缘节点过去的资源占用信息
        for operator in topology.operators: 
            operator.node.occupied_resources['cpu'] += operator.cpu_consumption
            operator.node.occupied_resources['mem'] += operator.mem_consumption
            
        for node in edge_cluster.edge_nodes:
            if node.occupied_resources['cpu']  >= node.cpu_capacity:
                return False
            if node.occupied_resources['mem']  >= node.mem_capacity:
                return False
        return True
    
    @classmethod
    def clear_occupied_resource(self, edge_cluster):
        for node in edge_cluster.edge_nodes:
            node.occupied_resources['cpu'] = 0
            node.occupied_resources['mem'] = 0


