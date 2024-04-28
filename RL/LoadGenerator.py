
import numpy as np
from Operator import Operator
class LoadGenerator:
    def __init__(self):
        self.load_value = 0

    def run(self,operator):
        AMPLITUDE = 3000  
        CYCLE = 1000
        elapsed_time = operator.logical_clock  # 使用算子的逻辑时钟
        self.load_value = max(abs(int(2000 + AMPLITUDE * np.sin(2 * np.pi * elapsed_time / CYCLE))),1)
        operator.ingest(self.load_value)
        #time.sleep(0.001)  # 控制发送速率，使其与算子的处理速率同步

if __name__ == "__main__":
    operator = Operator("1", "1")
    load_generator = LoadGenerator()
    while True:
        load_generator.run(operator)
        operator.run()
        print(operator.get_busy_time())