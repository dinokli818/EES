import threading
import time
import numpy as np
import OperatorEnv
import Operator
# 初始化 Q 表
num_operators = 1  # 逻辑算子数量，同一个逻辑算子的多个实例他们应该被汇总来看，不考虑倾斜
num_actions = 3  # 动作数量
num_states = 10  # 状态数量 0.1,0.2,...,1.0
q_table = np.zeros((num_states, num_actions))
q_table[:, 1] = 0.01
# 定义强化学习参数
learning_rate = 0.1
discount_factor = 0.9
exploration_prob = 1.0
max_exploration_prob = 1.0
min_exploration_prob = 0.01
exploration_decay_rate = 0.001



# 创建环境
env = OperatorEnv.OperatorEnv()

# 强化学习训练
num_episodes = 1000
for episode in range(num_episodes):
    operator = Operator.Operator("1","1")
    thread = threading.Thread(target=operator.run)
    thread.start()
    state = env.reset(operator)
    done = False
    for _ in range(num_episodes):#while not done:
        if np.random.uniform(0, 1) < exploration_prob:
            action = env.action_space.sample()  # 随机选择动作
        else:
            action = np.argmax(q_table[state, :])  # 选择最优动作
        
        new_state, reward, done, _ = env.step(action)
        
        # 更新 Q 表
        q_table[state, action] = (1 - learning_rate) * q_table[state, action] + \
                                 learning_rate * (reward + discount_factor * np.max(q_table[new_state, :]))
        
        state = new_state
        print(q_table,action,new_state,operator.busy_time,operator.parallelism)
        #time.sleep(5)
    
    # 衰减探索概率
    exploration_prob = min_exploration_prob + \
                       (max_exploration_prob - min_exploration_prob) * np.exp(-exploration_decay_rate * episode)

# 在决策时选择最优动作
def make_decision(state):
    return np.argmax(q_table[state, :])