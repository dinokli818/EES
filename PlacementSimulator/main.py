from scheduler_tester import SchedulerTester
import math

def main():
    num_nodes = 3
    num_operators = 4
    num_edges = 3
    num_tests = int(math.pow(num_operators, num_nodes))
    tester = SchedulerTester(num_nodes, num_operators, num_edges, num_tests)
    tester.run_all_tests(False, "1")

if __name__ == "__main__":
    main()