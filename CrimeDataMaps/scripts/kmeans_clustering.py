import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from adjustText import adjust_text

# Read and rename input data
df = pd.read_csv("data/usa/county_crime_summary.csv")
df = df.rename(columns={
    "homicide": "H",
    "robbery": "Rob",
    "rape": "R",
    "aggravated_assault": "AA"
})

# Set index to county name and select crime columns
df = df.set_index("county")[["H", "Rob", "R", "AA"]]

# Create a bar graph showing total crime per county
os.makedirs("images", exist_ok=True)
county_totals = df.sum(axis=1).sort_values(ascending=False)
plt.figure(figsize=(12, 6))
county_totals.plot(kind="bar")
plt.title("Total Crime Counts per County")
plt.ylabel("Total Incidents")
plt.xlabel("County")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("images/summary_bar_graph.png")
plt.close()

# Normalize data and run K-Means
X_scaled = StandardScaler().fit_transform(df)
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X_scaled)
df["Cluster"] = clusters

# Scatter plot (normalized space) with labels
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='tab10')
texts = [plt.text(X_scaled[i, 0], X_scaled[i, 1], df.index[i], fontsize=8) for i in range(len(df))]
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
plt.title("County Crime Patterns - K-Means Clustering")
plt.xlabel("Normalized Feature 1")
plt.ylabel("Normalized Feature 2")
plt.legend(*scatter.legend_elements(), title="Cluster")
os.makedirs("output", exist_ok=True)
plt.tight_layout()
plt.savefig("output/kmeans_clusters.png")
plt.close()

# Heatmap: average crime rates by cluster
cluster_means = df.groupby("Cluster")[["H", "Rob", "R", "AA"]].mean()
plt.figure(figsize=(8, 5))
sns.heatmap(cluster_means, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Average Crime Rate per Cluster")
plt.xlabel("Crime Type")
plt.ylabel("Cluster")
plt.tight_layout()
os.makedirs("plots/kmeans", exist_ok=True)
plt.savefig("plots/kmeans/cluster_heatmap.pdf")
plt.close()

# PCA plot of clusters
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap="tab10")
texts = [plt.text(X_pca[i, 0], X_pca[i, 1], df.index[i], fontsize=8) for i in range(len(df))]
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("K-Means Clustering of Counties (PCA)")
plt.legend(*scatter.legend_elements(), title="Cluster")
plt.tight_layout()
plt.savefig("plots/kmeans/pca_clusters.pdf")
plt.close()

print("K-Means clustering and visualizations saved.")
