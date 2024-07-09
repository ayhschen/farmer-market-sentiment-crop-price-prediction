from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR
import json
import csv
import matplotlib.pyplot as plt

json_file_path = "jsons/wheat/wheat_data_analysis.json"

# Load your data
with open(json_file_path, 'r') as f:
    data = json.load(f)

csv_file_path = "jsons/wheat/wheat_data_analysis.csv"

with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Month_Number', 'Supply_Aggregate',
                     'Demand_Aggregate', 'Volatility'])

    for month, values in data.items():
        writer.writerow(values)

data = pd.read_csv(csv_file_path)

# [month, sentiment_supply, sentiment_demand, monthly_volatility], this is the data format of the csv file
# separate data into exogenous and endogenous variables

# Separate exogenous and endogenous variables
exog_vars = ['Supply_Aggregate', 'Demand_Aggregate']
endog_vars = ['Volatility']


# Create lagged variables
lags = 1
data_lagged = pd.concat([data[exog_vars + endog_vars].shift(i)
                        for i in range(lags + 1)], axis=1).dropna()


# Split data into train and test sets
train_size = int(0.8 * len(data_lagged))
train_data = data_lagged[:train_size]
test_data = data_lagged[train_size:]

# Fit VARX model
model = VAR(endog=train_data[endog_vars], exog=train_data[exog_vars])
results = model.fit(maxlags=lags)

exog_future = test_data[exog_vars]

print(len(test_data))
# Forecast using the fitted model
forecast = results.forecast(y=test_data[endog_vars].values, steps=len(
    test_data), exog_future=exog_future)


# Print the forecasted values
print(forecast)

# Plot the forecasted values
plt.plot(forecast[:, 0], label='forecast')
plt.plot(test_data['Volatility'].values[:, 0], label='actual')
plt.legend()

# Assume `forecast` is your predicted values and `actual_values` are the actual values from your test dataset
actual_values = test_data['Volatility'].values
# Calculate MAE
# forecast[:, 0] selects the first forecast in each pair
mae = mean_absolute_error(actual_values[:, 0], forecast[:, 0])

# Calculate MSE
mse = mean_squared_error(actual_values[:, 0], forecast[:, 0])

# Calculate RMSE
rmse = np.sqrt(mse)

# Print the results
print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")

plt.show()
