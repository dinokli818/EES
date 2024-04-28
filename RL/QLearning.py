import threading
import numpy as np
from OperatorEnv import OperatorEnv
from LoadGenerator import LoadGenerator
import matplotlib.pyplot as plt
load_values = []
records_values = []
busy_times = []
parallelisms = []

# 初始化 Q 表
num_operators = 1  # 逻辑算子数量，同一个逻辑算子的多个实例他们应该被汇总来看，不考虑倾斜
num_actions = 3  # 动作空间大小
load_scale = 10  # 负载状态空间大小
par_scale = 6 #并行度状态空间大小
q_table = np.zeros((load_scale, par_scale, num_actions))
#q_table[:, 1] = 0.01
# 定义强化学习参数
learning_rate = 0.1
discount_factor = 0.9
exploration_prob = 1.0
max_exploration_prob = 1.0
min_exploration_prob = 0.01
exploration_decay_rate = 0.001

env = OperatorEnv()
load_generator = LoadGenerator()
# 强化学习训练
num_episodes = 10
for episode in range(num_episodes):
    state = env.reset()
    done = False
    for _ in range(1000):
        action = np.argmax(q_table[state[0],state[1], :])
        load_generator.run(env.operator)
        env.operator.run()
        new_state, reward, done, _ = env.step(action)
        
        # 更新 Q 表
        q_table[state[0],state[1], action] = (1 - learning_rate) * q_table[state[0],state[1], action] + \
                                 learning_rate * (reward + discount_factor * np.max(q_table[new_state[0],new_state[1], :]))
        load_values.append(load_generator.load_value)
        busy_times.append(env.operator.busy_time)
        parallelisms.append(env.operator.parallelism)
        records_values.append(env.operator.records)
        state = new_state
        #print(q_table, action, new_state, env.operator.busy_time, env.operator.parallelism)

    # 衰减探索概率
    exploration_prob = min_exploration_prob + \
                       (max_exploration_prob - min_exploration_prob) * np.exp(-exploration_decay_rate * episode)

print(q_table)

# 绘制图表
plt.figure(figsize=(12, 8))

# 绘制负载图
plt.subplot(4, 1, 1)
plt.plot(load_values, color='blue')
plt.xlabel('Time Steps')
plt.ylabel('Load')
plt.title('Load Over Time')

# 绘制繁忙时间图
plt.subplot(4, 1, 2)
plt.plot(busy_times, color='green')
plt.xlabel('Time Steps')
plt.ylabel('Busy Time')
plt.title('Busy Time Over Time')

# 绘制并行度图
plt.subplot(4, 1, 3)
plt.plot(parallelisms, color='red')
plt.xlabel('Time Steps')
plt.ylabel('Parallelism')
plt.title('Parallelism Over Time')

# 绘制记录数
plt.subplot(4, 1, 4)
plt.plot(records_values, color='yellow')
plt.xlabel('Time Steps')
plt.ylabel('Records')
plt.title('Parallelism Over Time')

plt.tight_layout()
plt.show()