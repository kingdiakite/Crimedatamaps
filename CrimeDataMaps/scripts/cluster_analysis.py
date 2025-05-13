import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scripts.clean_fbi_data import clean_fbi_csv

def prepare_cluster_features():
    # Load and clean all 6 datasets
    datasets = {
        "california": {
            "age": "data/california_offender_age.csv",
            "weapon": "data/california_weapon_type.csv",
            "location": "data/california_location_type.csv"
        },
        "florida": {
            "age": "data/florida_offender_age.csv",
            "weapon": "data/florida_weapon_type.csv",
            "location": "data/florida_location_type.csv"
        }
    }

    feature_rows = []
    for state, paths in datasets.items():
        combined = {}
        for category, path in paths.items():
            df = clean_fbi_csv(path)
            total = df["value"].sum()
            for _, row in df.iterrows():
                key = f"{category}_{row['key'].strip().lower().replace(' ', '_')}"
                combined[key] = row["value"] / total  # normalize
        combined["state"] = state
        feature_rows.append(combined)

    df_features = pd.DataFrame(feature_rows).set_index("state").fillna(0)
    return df_features

def perform_kmeans_clustering(df, k=2):
    model = KMeans(n_clusters=k, random_state=42)
    labels = model.fit_predict(df)
    df["cluster"] = labels
    return df, model

def plot_elbow_method(df):
    inertias = []
    K_range = range(1, 6)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df)
        inertias.append(kmeans.inertia_)

    plt.figure(figsize=(6, 4))
    plt.plot(K_range, inertias, marker='o')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    plt.tight_layout()
    plt.savefig("outputs/figures/elbow_method.png")
    plt.close()
