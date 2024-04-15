import networkx as nx
import graphviz
import itertools
from edge_cluster import EdgeCluster, EdgeNode
from topology import Topology
from application import Application
from scheduler import Scheduler
from placement_algorithm import PlacementAlgorithm

class SchedulerTester:
    def __init__(self, num_nodes, num_operators,num_edges, num_tests=1):
        """调度器测试类
        在一个测试实例中固定测试的拓扑和集群
        Args:
            num_tests (int, optional): 测试次数，默认100次
        """        
        self.topology = Topology(num_operators,num_edges)
        self.edge_cluster = EdgeCluster(num_nodes)
        
        self.num_nodes = num_nodes
        self.num_operators = num_operators
        self.num_tests = num_tests
        self.best_delay = float('inf')
        self.best_placement = [0] * self.num_operators
        self.best_longest_path = None
        self.stream_app = None
        self.resource_limit = None
        self.test_id = None

    def generate_all_placements(self):
        edge_nodes_indices = range(self.num_nodes)
        all_placements = list(itertools.product(edge_nodes_indices, repeat=self.num_operators))
        return all_placements
    
    def run_all_tests(self, resource_limit, test_id):
        self.resource_limit = resource_limit
        self.test_id = test_id
        scheduler = Scheduler()
        self.stream_app = Application(self.topology, self.edge_cluster)
        all_placements = self.generate_all_placements()

        for placement in all_placements:
            PlacementAlgorithm.manual_placement(self.topology, self.edge_cluster, placement)
            corr_placement = scheduler.check_resource_constraints(self.stream_app, self.resource_limit)
            
            if self.resource_limit and not corr_placement: 
                continue

            longest_path, longest_delay = self.stream_app.find_longest_path()
            placement_delay = self.stream_app.find_average_delay()

            if placement_delay < self.best_delay:
                self.best_delay = placement_delay
                self.best_longest_path = longest_path
                self.best_placement = [op.node for op in self.topology.operators]

        print("Best Delay:", self.best_delay)
        print("Longest_path:", self.best_longest_path)
        PlacementAlgorithm.manual_placement(self.topology, self.edge_cluster, self.best_placement)
        self.draw()

    def run_tests(self, resource_limit, test_id):
        """运行调度测试
        初始化需要的调度器，并选择调度算法，在固定的拓扑和集群上运行调度算法多次，
        找到拥有最小的最大流路径延迟的初始放置
        """
        self.resource_limit = resource_limit
        self.test_id = test_id
        scheduler = Scheduler()
        self.stream_app = Application(self.topology, self.edge_cluster)
        for _ in range(self.num_tests):
            corr_placement = scheduler.place_topology_on_cluster(self.stream_app, resource_limit)
            if self.resource_limit and not corr_placement: #资源限制+拓扑正确 00-0 01-0 10-1 11-0
                continue
            longest_path, longest_delay = self.stream_app.find_longest_path()
            placement_delay = self.stream_app.find_average_delay()
            if placement_delay < self.best_delay:
                self.best_delay = placement_delay
                self.best_longest_path = longest_path
                self.best_placement = [op.node for op in self.topology.operators] # 放置是边缘节点的列表
                #print("Best Placement:", self.best_placement)
        #print(self.topology.operators[0].node)
        #print("Best Placement:", self.best_placement)
        print("Best Delay:", self.best_delay)
        print("Longest_path:", self.best_longest_path)
        PlacementAlgorithm.manual_placement(self.topology, self.edge_cluster, self.best_placement)
        self.draw()

    def draw(self):
        G = nx.DiGraph()
        for operator in self.topology.operators:
            G.add_node(operator.op_id, label=f"{operator.op_id}\nNode: {operator.node.node_id}\n{operator.processing_time:.2f}")
        for i in range(self.topology.num_operators):
            for j in range(self.topology.num_operators):
                if self.topology.edges[i, j] != 0:
                    i_node_id = self.topology.operators[i].node.node_id
                    j_node_id = self.topology.operators[j].node.node_id
                    edge_latency = float(self.edge_cluster.edge_networks[i_node_id, j_node_id]['latency'])
                    G.add_edge(self.topology.operators[i].op_id, self.topology.operators[j].op_id, label=f"{edge_latency:.2f}")

        # Create a Graphviz object
        dot = graphviz.Digraph(comment='Topology Graph', graph_attr={'dpi': '300'})

        # Add nodes and edges to Graphviz object
        for node in G.nodes():
            dot.node(str(node), G.nodes[node]['label'])
        for edge in G.edges():
            dot.edge(str(edge[0]), str(edge[1]), label=G.edges[edge]['label'])

        # Save the dot file
        dot_file_path = "graph"+ self.test_id + ".dot"
        dot.render(dot_file_path, format='png', cleanup=True)

        print(f"Dot file saved at: {dot_file_path}.png with DPI set to 300")
