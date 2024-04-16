import math
import threading
import time
import numpy as np


class Operator:
    def __init__(self,job_id,operator_id):
        self.mutex = threading.Lock()
        self.job_id = job_id
        self.operator_id = operator_id
        self.busy_time = 0
        self.parallelism = 1

    def get_busy_time(self):
        #这里应该是利用Restful API或者InfluxDB都可以
        return self.busy_time

    def rescale(self,act):
        self.mutex.acquire() 
        #这里应该是利用Restful API触发停机重配置
        match act:
            case 0:
                self.parallelism = max(int(self.parallelism / 2),1)
                self.restart()
            case 1:
                self.parallelism = self.parallelism
            case 2:
                self.parallelism = int(self.parallelism * 2)
                self.restart()
        self.mutex.release()

    def restart(self):
        #这里应该是利用Restful API触发停机重配置
        #time.sleep(100)
        pass

    def run(self):
        AMPLITUDE = 499  # 振幅
        FREQUENCY = 1   # 频率
        start_time = time.time()  # 记录开始时间

        while True:
            elapsed_time = time.time() - start_time # 经过的时间模5
            
            # 计算当前时间对应的正弦值
            load_value = 500 + AMPLITUDE * np.sin(2 * np.pi * elapsed_time / FREQUENCY)
            load_value = int(load_value)

            self.mutex.acquire()
            self.busy_time = min(999,load_value/self.parallelism)
            self.mutex.release()
            time.sleep(0.001)  # 等待5秒，控制更新速率