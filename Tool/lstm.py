import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# 从CSV文件中读取数据
data = pd.read_csv("data/output.csv")
data.columns = ['Fibonacci', 'GenerateTime', 'IngestTime','OutputTime']

#计算每个数据项的时间区间[0,1)...(n,n+1)（以秒为单位）
data['GeneratedInterval'] = ((data['GenerateTime'] - data['GenerateTime'].min()) / 1000).astype(np.int64)

# 创建一个空的DataFrame用于存储负载
load_data = pd.DataFrame(columns=['GeneratedInterval', 'load'])

# 计算每5秒内的负载
window_size = 5  # 每5秒计算一次统计值，t=5时，纵坐标是[0,5)所有数据的相关值
for window_start in range(0, data['GeneratedInterval'].max() + 1, window_size):
    window_end = window_start + window_size
    window_data = data[(data['GeneratedInterval'] >= window_start) & (data['GeneratedInterval'] < window_end)]
    if not window_data.empty:
        # 处理窗口边界点
        if window_end > data['GeneratedInterval'].max():
            break #window_end = data['GeneratedInterval'].max() + 1  # 将窗口结束时间设置为最大时间戳+1
        load = window_data['Fibonacci'].count() / window_size
        load_data = pd.concat([load_data, pd.DataFrame({'GeneratedInterval': [window_start], 'load': [load]})], ignore_index=True)

#接下来是LSTM部分

# 数据预处理
load_data['load'] = load_data['load'].astype(float)
scaler = MinMaxScaler()
load_data['load'] = scaler.fit_transform(load_data['load'].values.reshape(-1, 1))

# 创建序列数据
sequence_length = 5  # 指定每个序列的长度
X, y = [], []
for i in range(len(load_data) - sequence_length):
    X.append(load_data['load'].values[i:i+sequence_length])
    y.append(load_data['load'].values[i+sequence_length])

X = np.array(X)
y = np.array(y)

# 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 构建LSTM模型
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(50, input_shape=(sequence_length, 1)),
    tf.keras.layers.Dense(1)
])

# 编译模型
model.compile(loss='mean_squared_error', optimizer='adam')

# 训练模型
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# 预测下一个时间窗口的负载
last_sequence = load_data['load'].values[-sequence_length:].reshape(1, -1, 1)
next_load = model.predict(last_sequence)
next_load = scaler.inverse_transform(next_load)  # 反归一化

print("预测下一个时间窗口的负载：", next_load)
# 绘制折线图
fig, ax1 = plt.subplots()

# 绘制延迟
ax1.set_xlabel('Time (ProcessedIntervals)')
ax1.set_ylabel('P99 Latency (ms)', color='tab:blue')
ax1.plot(result_latency['ProcessedInterval'], result_latency['p99_latency'], color='tab:blue', label='P99 Latency')
ax1.plot(result_latency['ProcessedInterval'], result_latency['mean_latency'], color='tab:green', label='Mean Latency')
ax1.tick_params(axis='y', labelcolor='tab:blue')
#ax1.set_yscale('log')
# 创建第二个Y轴
ax2 = ax1.twinx()
ax2.set_ylabel('Load (tuple/s)', color='tab:red')
ax2.plot(load_data['GeneratedInterval'], load_data['load'], color='tab:red', label='Load', alpha=0.3)  # 使用alpha设置浅色

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.title('P99 Latency, Mean Latency, and Load Over Time')
plt.grid(True)

plt.savefig("your_chart.png", dpi=300, bbox_inches='tight')
plt.show()