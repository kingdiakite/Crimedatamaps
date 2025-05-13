# Train and evaluate a Random Forest model for crime risk prediction

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load normalized categorical features and summary totals
features_df = pd.read_csv("data/usa/county_crime_features.csv")
summary_df = pd.read_csv("data/usa/county_crime_summary.csv")

# Merge both datasets on county
df = pd.merge(features_df, summary_df, on="county", how="inner")

# Total crime count per county (used to label risk levels)
df["violent_crime_total"] = df[["homicide", "rape", "robbery", "aggravated_assault"]].sum(axis=1)

# Create 3-class label based on quantiles (Low, Medium, High)
quantiles = df["violent_crime_total"].quantile([0.33, 0.66])
low_thresh, high_thresh = quantiles[0.33], quantiles[0.66]

def assign_level(val):
    if val <= low_thresh:
        return "Low"
    elif val <= high_thresh:
        return "Medium"
    return "High"

df["CrimeLevel"] = df["violent_crime_total"].apply(assign_level)

# Prepare training data (drop totals and labels)
drop_cols = ["county", "CrimeLevel", "violent_crime_total", "homicide", "rape", "robbery", "aggravated_assault"]
X = df.drop(columns=drop_cols)
y = df["CrimeLevel"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into 50% train/test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.5, random_state=42, stratify=y)

# Train a Random Forest classifier
rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)

# Create output folder for prediction visuals
os.makedirs("output/predictions", exist_ok=True)

# Plot top 15 feature importances
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]
top_features = np.array(X.columns)[indices[:15]]
top_importances = importances[indices[:15]]

plt.figure(figsize=(10, 6))
sns.barplot(x=top_importances, y=top_features)
plt.title("Top 15 Feature Importances (Random Forest)")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig("output/predictions/feature_importance.png")
plt.close()

# Plot confusion matrix for 3-class prediction
cm = confusion_matrix(y_test, rf_preds, labels=["Low", "Medium", "High"])
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=["Low", "Medium", "High"],
            yticklabels=["Low", "Medium", "High"])
plt.title("Confusion Matrix (Random Forest - 3-Class)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("output/predictions/confusion_matrix.png")
plt.close()

# Print basic model metrics
print("\nRandom Forest Accuracy:", accuracy_score(y_test, rf_preds))
print("\nClassification Report:\n", classification_report(y_test, rf_preds))
