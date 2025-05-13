from scripts.fbi_visuals import plot_all_comparisons
from scripts.cluster_analysis import prepare_cluster_features, perform_kmeans_clustering, plot_elbow_method
def main():
    print("Generating comparison charts for California vs Florida...")
    plot_all_comparisons()
    print("Charts saved to outputs/figures/")

if __name__ == "__main__":
    main()
    
def run_clustering():
    df = prepare_cluster_features()
    plot_elbow_method(df)  # visualize optimal k
    clustered_df, model = perform_kmeans_clustering(df, k=2)
    print("\nClustered State Profiles:")
    print(clustered_df[["cluster"]])
