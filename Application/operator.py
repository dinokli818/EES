class Operator:
    '''算子类

    '''
    def __init__(self, op_id):

        self.selectivity = 1.0

    def is_source(self):
        return not self.upstream_operators

    def is_sink(self):
        return not self.downstream_operators

    def response_time(self, input_rate):
        # TODO: Implement this method
        pass

    def compute_deployment_cost(self):
        # TODO: Implement this method
        pass

    def compute_max_deployment_cost(self):
        # TODO: Implement this method
        pass

    def compute_max_throughput(self, upstream_deployment):
        # TODO: Implement this method
        pass

    def get_max_path_length(self, operator):
        # TODO: Implement this method
        pass
