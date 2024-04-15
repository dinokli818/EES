import pandas as pd
import matplotlib.pyplot as plt

# Read the data from a local Parquet file
data = pd.read_parquet('data/yellow_tripdata_2015-01.parquet')

# Convert the datetime columns to datetime data type
data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
data['tpep_dropoff_datetime'] = pd.to_datetime(data['tpep_dropoff_datetime'])

# Extract the day of the week from the pickup datetime
data['Day_of_Week'] = data['tpep_pickup_datetime'].dt.dayofweek

# Set the 'tpep_pickup_datetime' column as the DataFrame index
data.set_index('tpep_pickup_datetime', inplace=True)

# Resample the data to calculate the count of data items in 1-hour intervals
resampled_data = data.resample('1H').count()

# Group the data by day of the week and calculate the mean for each day
weekly_mean_data = resampled_data.groupby(resampled_data.index.dayofweek).mean()

# Plot the data as a waveform
plt.figure(figsize=(10, 6))
plt.plot(weekly_mean_data.index, weekly_mean_data['VendorID'], marker='o', linestyle='-')
plt.xlabel('Day of the Week (0=Monday, 6=Sunday)')
plt.ylabel('Average Data Items Count per Hour')
plt.title('Average Data Items Count by Day of the Week')
plt.grid(True)

# Show the plot
plt.show()