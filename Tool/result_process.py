# 将sink后的数据包含的延迟信息进行处理绘图

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 从CSV文件中读取数据
data = pd.read_csv("data/1.csv")
data.columns = ['Fibonacci', 'GenerateTime', 'IngestTime','OutputTime']

# 计算每个数据项的延迟（以毫秒为单位）
data['Delay'] = data['OutputTime'] - data['IngestTime']

#计算每个数据项的时间区间[0,1)...(n,n+1)（以秒为单位）
data['GeneratedInterval'] = ((data['GenerateTime'] - data['GenerateTime'].min()) / 1000).astype(np.int64)
data['ProcessedInterval'] = ((data['OutputTime'] - data['OutputTime'].min()) / 1000).astype(np.int64)
data['IngestedInterval'] = ((data['IngestTime'] - data['IngestTime'].min()) / 1000).astype(np.int64)
data['OutputInterval'] = ((data['OutputTime'] - data['OutputTime'].min()) / 1000).astype(np.int64)

# 创建一个空的DataFrame用于存储绘图需要的p99延迟、延迟均值以及负载
result_latency = pd.DataFrame(columns=['ProcessedInterval', 'p99_latency', 'mean_latency'])
result_load = pd.DataFrame(columns=['GeneratedInterval',"OutputInterval", 'load',"throughput","throughput2"])

# 计算每5秒内的p99延迟、延迟均值
window_size = 5  # 每5秒计算一次统计值，t=5时，纵坐标是[0,5)所有数据的延迟相关值
for window_start in range(0, data['ProcessedInterval'].max() + 1, window_size):
    window_end = window_start + window_size
    window_data = data[(data['ProcessedInterval'] >= window_start) & (data['ProcessedInterval'] < window_end)]
    if not window_data.empty:
        # 处理窗口边界点
        if window_end > data['ProcessedInterval'].max():
            break #window_end = data['ProcessedInterval'].max() + 1  # 将窗口结束时间设置为最大时间戳+1
        p99_latency = np.percentile(window_data['Delay'], 99)
        mean_latency = window_data['Delay'].mean()
        result_latency = pd.concat([result_latency, pd.DataFrame({'ProcessedInterval': [window_end], 'p99_latency': [p99_latency], 'mean_latency': [mean_latency]})], ignore_index=True)
# 计算每5秒内的p99延迟、延迟均值
# t=0时，纵坐标是[0,5)所有数据的生产速率
for window_start in range(0, data['GeneratedInterval'].max() + 1, window_size):
    window_end = window_start + window_size
    window_data = data[(data['GeneratedInterval'] >= window_start) & (data['GeneratedInterval'] < window_end)]
    if not window_data.empty:
        # 处理窗口边界点
        if window_end > data['GeneratedInterval'].max():
            break #window_end = data['GeneratedInterval'].max() + 1  # 将窗口结束时间设置为最大时间戳+1
        load = window_data['Fibonacci'].count() / window_size
        result_load = pd.concat([result_load, pd.DataFrame({'GeneratedInterval': [window_start], 'load': [load]})], ignore_index=True)
for window_start in range(0, data['OutputInterval'].max() + 1, window_size):
    window_end = window_start + window_size
    window_data = data[(data['OutputInterval'] >= window_start) & (data['OutputInterval'] < window_end)]
    if not window_data.empty:
        # 处理窗口边界点
        if window_end > data['OutputInterval'].max():
            break #window_end = data['GeneratedInterval'].max() + 1  # 将窗口结束时间设置为最大时间戳+1
        throughput = window_data['Fibonacci'].count() / window_size
        result_load = pd.concat([result_load, pd.DataFrame({'OutputInterval': [window_start], 'throughput': [throughput]})], ignore_index=True)

for window_start in range(0, data['IngestedInterval'].max() + 1, window_size):
    window_end = window_start + window_size
    window_data = data[(data['IngestedInterval'] >= window_start) & (data['IngestedInterval'] < window_end)]
    if not window_data.empty:
        # 处理窗口边界点
        if window_end > data['IngestedInterval'].max():
            break #window_end = data['GeneratedInterval'].max() + 1  # 将窗口结束时间设置为最大时间戳+1
        throughput2 = window_data['Fibonacci'].count() / window_size
        result_load = pd.concat([result_load, pd.DataFrame({'IngestedInterval': [window_start], 'throughput2': [throughput2]})], ignore_index=True)

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
ax2.set_ylabel('Load,Throuhgput (tuple/s)', color='tab:red')
ax2.plot(result_load['GeneratedInterval'], result_load['load'], color='tab:red', label='Load', alpha=0.3)  # 使用alpha设置浅色
ax2.plot(result_load['OutputInterval'], result_load['throughput'], color='tab:orange', label='throughput', alpha=0.3)  # 使用alpha设置浅色
ax2.plot(result_load['IngestedInterval'], result_load['throughput2'], color='tab:pink', label='throughput2', alpha=0.3)  # 使用alpha设置浅色

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.title('P99 Latency, Mean Latency,Load and Throughput Over Time')
plt.grid(True)

plt.savefig("your_chart.png", dpi=300, bbox_inches='tight')
plt.show()