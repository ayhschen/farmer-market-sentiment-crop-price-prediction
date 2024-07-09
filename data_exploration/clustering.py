import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Sample data for demonstration
np.random.seed(42)
data = pd.read_csv("jsons/wheat/wheat_data_analysis.csv")

# Standardizing the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# K-means++ clustering
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42)
kmeans.fit(data_scaled)

# Cluster labels
labels = kmeans.labels_

# Add cluster labels to the DataFrame
data['Cluster'] = labels

# Generate all combinations of three features
feature_combinations = list(itertools.combinations(data.columns[:-1], 3))

# Plotting each combination
fig = plt.figure(figsize=(20, 15))

for i, combo in enumerate(feature_combinations, 1):
    ax = fig.add_subplot(2, 2, i, projection='3d')
    ax.scatter(data[combo[0]], data[combo[1]], data[combo[2]], c=data['Cluster'], cmap='viridis')
    ax.set_xlabel(combo[0])
    ax.set_ylabel(combo[1])
    ax.set_zlabel(combo[2])
    ax.set_title(f'3D plot of {combo[0]}, {combo[1]}, {combo[2]}')

plt.tight_layout()
plt.show()
