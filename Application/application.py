import numpy as np
from typing import List, Tuple, Dict, Set


class Application:
    def __init__(self):
        self.operators = []
        self.source_sink_paths = []

    def add_operator(self, operator):
        self.operators.append(operator)
        self.compute_source_sink_paths()

    def add_edge(self, op1, op2):
        op1.add_downstream(op2)
        op2.add_upstream(op1)
        self.compute_source_sink_paths()

    def compute_source_sink_paths(self):
        self.source_sink_paths = []

        for op1 in self.operators:
            if not op1.is_source():
                continue
            for op2 in self.operators:
                if not op2.is_sink():
                    continue
                self.source_sink_paths.extend(self.compute_source_sink_paths(op1, op2))

    def compute_source_sink_paths(self, src, sink):
        paths = []
        paths_queue = []
        path = [src]
        paths_queue.append(path)

        while paths_queue:
            path = paths_queue.pop(0)
            last = path[-1]

            if last == sink:
                paths.append(path)

            for op in last.downstream_operators:
                visited = any(n == op for n in path)
                if not visited:
                    new_path = path.copy()
                    new_path.append(op)
                    paths_queue.append(new_path)

        return paths

    def get_all_paths(self):
        return self.source_sink_paths

    def end_to_end_latency(self, input_rate):
        latency = 0.0

        for path in self.source_sink_paths:
            latency = max(latency, self.end_to_end_latency(input_rate, path))

        return latency

    def end_to_end_latency(self, input_rate, path):
        latency = 0.0

        for op in path:
            operator_resp_time = op.response_time(input_rate)
            latency += operator_resp_time

        return latency

    def end_to_end_latency_op_resp_time(self, op_resp_time):
        latency = 0.0

        for path in self.source_sink_paths:
            latency = max(latency, self.end_to_end_latency_op_resp_time(op_resp_time, path))

        return latency

    def end_to_end_latency_op_resp_time(self, op_resp_time, path):
        latency = 0.0

        for op in path:
            operator_resp_time = op_resp_time[op]
            latency += operator_resp_time

        return latency

    def get_operators(self):
        return self.operators

    def compute_deployment_cost(self):
        total_cost = 0.0
        for op in self.get_operators():
            total_cost += op.compute_deployment_cost()

        return total_cost

    def compute_max_deployment_cost(self):
        total_cost = 0.0
        for op in self.get_operators():
            total_cost += op.compute_max_deployment_cost()

        return total_cost

    def get_max_path_length(self, operator):
        length = 1
        for path in self.source_sink_paths:
            for op in path:
                if operator == op:
                    length = max(length, len(path))
                    break

        return length

    def compute_operator_deployment(self, operator):
        deployment = [0] * len(ComputingInfrastructure.get_infrastructure().get_node_types())
        op_instances = operator.current_deployment
        for i in range(len(op_instances)):
            deployment[op_instances[i].get_index()] += 1

        return deployment

    def compute_global_deployment(self):
        global_deployment = [0] * len(ComputingInfrastructure.get_infrastructure().get_node_types())

        for op in self.operators:
            op_deployment = self.compute_operator_deployment(op)
            for j in range(len(op_deployment)):
                global_deployment[j] += op_deployment[j]

        return global_deployment

    def compute_per_operator_input_rate(self, input_rate):
        op_deployment = {}
        for op in self.operators:
            op_deployment[op] = op.current_deployment

        return self.compute_per_operator_input_rate(input_rate, op_deployment)

    def compute_per_operator_input_rate(self, input_rate, op_deployment):
        op_input_rate = {op: 0.0 for op in self.operators}
        done = False

        while not done:
            done = True

            for src in self.get_operators():
                if not src.is_source():
                    continue

                checked = set()
                queue = [src]

                while queue:
                    op = queue.pop(0)
                    if op not in checked:
                        rate = 0.0

                        if op.is_source():
                            rate = input_rate

                        else:
                            for up in op.upstream_operators:
                                rate += min(op_input_rate[up], up.compute_max_throughput(op_deployment[up])) * up.selectivity

                        old_value = op_input_rate[op]
                        done &= (old_value == rate)

                        op_input_rate[op] = rate

                        for down in op.downstream_operators:
                            queue.append(down)

                        checked.add(op)

        return op_input_rate

# Dummy class to replace ComputingInfrastructure
class ComputingInfrastructure:
    @staticmethod
    def get_infrastructure():
        return ComputingInfrastructure()

    def get_node_types(self):
        # TODO: Implement this method
        pass

# Example usage:
if __name__ == "__main__":
    app = Application()
    op1 = Operator(1)
    op2 = Operator(2)
    op3 = Operator(3)

    app.add_operator(op1)
    app.add_operator(op2)
    app.add_operator(op3)

    app.add_edge(op1, op2)
    app.add_edge(op2, op3)

    input_rate = 100.0
    op_resp_time = app.compute_per_operator_input_rate(input_rate)
    print("Operator Input Rates:", op_resp_time)
