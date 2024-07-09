import pandas as pd
from datetime import datetime

# Sample outputs from your provided code
outputs = [
    "Quantitative: Wheat: Feed and residual use in Russia is 21.0 million tons, increased 1.0 million tons, 2023-01-01, 1",
    "Quantitative: Wheat: Global consumption is 791.0 million tons, increased 2.4 million tons, 2023-02-01, 0.5",
    "Qualitative: Wheat: Supply outlook is stable, due to unchanged U.S. wheat outlook, 2023-03-01, 0",
    "Quantitative: Wheat: Ending stocks are 862 million bushels, decreased 15 million bushels, 2023-04-01, -0.5",
    "Quantitative: Wheat: Global exports are 41 million tons, decreased 2.5 million tons, 2023-05-01, -1"
]

# Initialize lists for data
data = []

# Process each output
for output in outputs:
    parts = output.split(", ")
    date = datetime.strptime(parts[-2], '%Y-%m-%d')
    score = float(parts[-1])
    commodity = parts[0].split(": ")[1]
    metric = " ".join(parts[0].split(": ")[2:]).split(" is ")[0]
    value = parts[1]
    change = parts[2]

    # Create a dictionary for each data point
    data_point = {
        "Date": date,
        "Commodity": commodity,
        "Metric": metric,
        "Value": value,
        "Change": change,
        "Score": score
    }
    data.append(data_point)

# Convert to DataFrame
df = pd.DataFrame(data)

# Pivot the DataFrame to get time series format
time_series_df = df.pivot_table(index="Date", columns=["Commodity", "Metric"], values=["Value", "Score"], aggfunc='first')

# Handling missing values (optional)
time_series_df.fillna(method='ffill', inplace=True)  # Forward fill to propagate last valid observation

print(time_series_df)
