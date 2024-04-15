import pandas as pd
import matplotlib.pyplot as plt

# 从CSV文件中读取数据
data = pd.read_parquet('data/yellow_tripdata_2015-01.parquet')
print(data.head())
# Convert the 'Start_Time' column to datetime
data['Start_Time'] = pd.to_datetime(data['tpep_pickup_datetime'])

# Set the 'Start_Time' column as the DataFrame index
data.set_index('Start_Time', inplace=True)

# Resample the data to calculate the count of data items in 10-minute intervals
resampled_data = data.resample('1T').count()
print(resampled_data.head())
# Plot the data as a waveform
plt.figure(figsize=(10, 6))
plt.fill_between(resampled_data.index, resampled_data['VendorID'], 0, alpha=0.7)
plt.xlabel('Time')
plt.ylabel('Data Items Count')
plt.title('Data Items Waveform in 1-Hour Intervals')
plt.grid(True)

# Show the plot
plt.show()