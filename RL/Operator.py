import math
import threading
import time
import numpy as np

class Operator:
    def __init__(self, job_id, operator_id):
        self.job_id = job_id
        self.operator_id = operator_id
        self.busy_time = 0
        self.parallelism = 1
        self.records = 0
        self.execute_rate = 1000
        self.logical_clock = 0

    def get_busy_time(self):
        return self.busy_time

    def rescale(self, act):
        match act:
            case 0:
                self.parallelism = max(int(self.parallelism / 2), 1)
                self.restart()
            case 1:
                self.parallelism = self.parallelism
            case 2:
                self.parallelism = min(int(self.parallelism * 2), 32)
                self.restart()
        
    def ingest(self, records):
        self.records += records

    def restart(self):
        pass

    def run(self):
        self.busy_time = min(999, self.records / (self.parallelism * self.execute_rate) * 1000)
        self.records = max(self.records - self.execute_rate * self.parallelism, 0)
        self.logical_clock += 1
        #time.sleep(0.001)  # Control update rate
