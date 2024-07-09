import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import json

# Function to calculate percent change
def calculate_percent_change(data):
    return np.diff(data) / data[:-1] * 100

# Function to aggregate data in four-month intervals
def aggregate_in_four_months(data):
    aggregated_data = []
    for i in range(0, len(data), 4):
        if i + 3 < len(data):  # Ensure there are enough data points to form a four-month period
            aggregated_data.append(np.mean(data[i:i+4]))  # Replace np.mean with np.sum if that's more appropriate
    return aggregated_data

# Load the JSON data
# Replace 'path_to_your_json_file.json' with the actual path to your JSON file
file_path = './jsons/wheat/wheat_data_analysis.json'

with open(file_path, 'r') as file:
    wheat_data = json.load(file)

# Extracting and processing the data
dates = []
volatility_scores = []
supply_scores = []
demand_scores = []

for month, values in wheat_data.items():
    if len(values) >= 4:
        date = datetime.strptime(month, '%B_%Y')
        dates.append(date)
        volatility_scores.append(values[3])  # Fourth value is volatility
        supply_scores.append(values[1])      # Second value is supply score
        demand_scores.append(values[2])      # Third value is demand score


num_complete_periods = len(dates) // 4
dates_aggregated = dates[:num_complete_periods * 4:4]  # Adjusted to ensure matching length with data arrays

volatility_scores_aggregated = aggregate_in_four_months(volatility_scores[:num_complete_periods * 4])
supply_scores_aggregated = aggregate_in_four_months(supply_scores[:num_complete_periods * 4])
demand_scores_aggregated = aggregate_in_four_months(demand_scores[:num_complete_periods * 4])
# Aggregate data in four-month intervals
# dates_aggregated = dates[::4]  # Taking every fourth month for the date labels
# volatility_scores_aggregated = aggregate_in_four_months(volatility_scores)
# supply_scores_aggregated = aggregate_in_four_months(supply_scores)
# demand_scores_aggregated = aggregate_in_four_months(demand_scores)

# Calculate percent change for the aggregated data
supply_percent_change_aggregated = calculate_percent_change(supply_scores_aggregated)
demand_percent_change_aggregated = calculate_percent_change(demand_scores_aggregated)
vol_percent_change_aggregated = calculate_percent_change(volatility_scores_aggregated)

# Plotting
plt.figure(figsize=(15, 8))
plt.plot(dates_aggregated[1:], supply_percent_change_aggregated, label='Supply % Change', marker='o', color='blue')
plt.plot(dates_aggregated[1:], vol_percent_change_aggregated, label='Volatility % Change', marker='x', color='red')
plt.plot(dates_aggregated[1:], demand_percent_change_aggregated, label='Demand % Change', marker='o', color='green')

# Graph formatting
plt.title('Demand, Supply, Volatility % Change Over Four-Month Periods')
plt.xlabel('Date')
plt.ylabel('% Change')
plt.legend()
plt.grid(True)

# Date formatting on X-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())

plt.show()
