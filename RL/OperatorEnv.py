import gymnasium as gym
import numpy as np
import gymnasium as gym
import numpy as np
from Operator import Operator

class OperatorEnv(gym.Env):
    """
    逻辑算子的gym环境
    """
    def __init__(self):
        self.action_space = gym.spaces.Discrete(3)  # -1：缩小 0: 不调整, 1: 增加
        self.observation_space = gym.spaces.Discrete(10)  # 状态离散化为 10 个整数
        self.operator = Operator("1", "1")
        self.state = 0,int(np.log2(self.operator.parallelism))
        
    def reset(self):
        self.operator = Operator("1", "1")
        self.state = 0,int(np.log2(self.operator.parallelism))
        return self.state
    
    def step(self, action):
        self.operator.rescale(action)
        new_busy_time = self.operator.get_busy_time()

        new_state = self._discretize_state(new_busy_time),int(np.log2(self.operator.parallelism))
        reward = self._calculate_reward(new_busy_time,action)  # 根据新状态计算奖励
        done = False  # 暂时假设不终止
        return new_state, reward, done, {}
    
    def _discretize_state(self, busy_time):
        # 将 busy time 映射为整数状态
        bins = np.linspace(0, 1000, num=11)
        return np.digitize(busy_time, bins) - 1
    
    def _calculate_reward(self, busy_time,action):
        # 根据新的 busy time 计算奖励
        # 需要根据问题的实际情况来定义奖励函数
        reward = 0
        if busy_time < 700.0:
            reward +=0.5
        if busy_time >= 700.0:
            reward-=1
        if action==0 or action ==1:
            reward -= 1.5
        return reward
