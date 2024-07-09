import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming 'data_dict' is your dictionary with Month_Year as keys and the list of values
data = pd.read_csv("jsons/wheat/wheat_data_analysis.csv")
# data["Agg"] = (data["Supply_Aggregate"] + 4 * data["Demand_Aggregate"])
print(data)
# data = data.iloc[: , 1:]

# Calculate correlation matrix
corr_matrix = data.corr()

# Create a heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
