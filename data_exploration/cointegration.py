import numpy as np
import json
from datetime import datetime
from statsmodels.tsa.stattools import grangercausalitytests

# Function to calculate percent change, handling zero and NaN cases
def calculate_percent_change(data):
    changes = np.diff(data)
    percent_changes = np.zeros_like(changes, dtype=float)
    for i in range(len(changes)):
        if data[i] != 0:
            percent_changes[i] = (changes[i] / data[i]) * 100
        else:
            percent_changes[i] = np.nan
    return np.concatenate(([np.nan], percent_changes))

# Load the JSON data
file_path = 'jsons/wheat/wheat_data_analysis.json'
with open(file_path, 'r') as file:
    wheat_data = json.load(file)

# Extracting and processing the data
volatility_scores = []
supply_scores = []
demand_scores = []

for month, values in wheat_data.items():
    if len(values) >= 4:
        volatility_scores.append(values[3])  # Fourth value is volatility
        supply_scores.append(values[1])      # Second value is supply score
        demand_scores.append(values[2])      # Third value is demand score

# Calculate percent change for supply, demand, and volatility
supply_percent_change = calculate_percent_change(supply_scores)
demand_percent_change = calculate_percent_change(demand_scores)
volatility_percent_change = calculate_percent_change(volatility_scores)

# Combine the data and remove any rows with NaN values
data = np.column_stack([volatility_percent_change, supply_percent_change, demand_percent_change])
data = data[~np.isnan(data).any(axis=1)]  # Remove rows with NaN

# Perform Granger Causality Tests
print('Granger Causality Test: Supply -> Volatility')
grangercausalitytests(data[:, [1, 0]], maxlag=4)

print('\nGranger Causality Test: Demand -> Volatility')
grangercausalitytests(data[:, [2, 0]], maxlag=4)
