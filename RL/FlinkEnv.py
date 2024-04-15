import gymnasium as gym

class FlinkEnvironment(gym.Env):
    def __init__(self, num_operators):
        self.num_operators = num_operators
        self.action_space = gym.spaces.Discrete(3)  # -1：缩小 0: 不调整, 1: 增加
        self.observation_space = gym.spaces.Discrete(10)  # 状态离散化为 10 个整数
        self.state = None
        
    def reset(self):
        initial_busy_time = np.random.uniform(0.0, 1000.0, size=self.num_operators)  # 随机初始化状态
        self.state = self._discretize_state(initial_busy_time)
        return self.state
    
    def step(self, action):
        new_busy_time = float(input())#np.random.uniform(0.0, 1000.0, size=self.num_operators)  # 暂时假设新状态与当前状态相同
        new_state = self._discretize_state(new_busy_time)
        reward = self._calculate_reward(new_busy_time)  # 根据新状态计算奖励
        done = False  # 暂时假设不终止
        return new_state, reward, done, {}
    
    def _discretize_state(self, busy_time):
        # 将 busy time 映射为整数状态
        bins = np.linspace(0, 1000, num=11)
        return np.digitize(busy_time, bins) - 1
    
    def _calculate_reward(self, busy_time):
        # 根据新的 busy time 计算奖励
        # 需要根据问题的实际情况来定义奖励函数
        if busy_time < 700.0:
            return 1
        return 0  # 暂时假设奖励为零