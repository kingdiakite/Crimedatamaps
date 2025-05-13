# Build normalized categorical features (weapon, age, location) for each county

import os
import pandas as pd

DATA_DIR = "data/usa"
OUTPUT_CSV = "data/usa/county_crime_features.csv"

CRIME_TYPES = ["homicide", "rape", "robbery", "aggravated_assault"]
CSV_TYPES = ["location_type.csv", "weapon_type.csv", "offender_age.csv"]

rows = []

# Go through each county folder
for county in os.listdir(DATA_DIR):
    county_dir = os.path.join(DATA_DIR, county)
    if not os.path.isdir(county_dir):
        continue

    feature_row = {"county": county}

    for crime in CRIME_TYPES:
        crime_dir = os.path.join(county_dir, crime)
        if not os.path.isdir(crime_dir):
            continue

        for csv_type in CSV_TYPES:
            file_path = os.path.join(crime_dir, csv_type)
            if not os.path.exists(file_path):
                continue

            try:
                df = pd.read_csv(file_path)
                if "key" not in df.columns or "value" not in df.columns:
                    continue
                total = df["value"].sum()
                if total == 0:
                    continue

                # Normalize values and make readable column names
                for _, row in df.iterrows():
                    key = row["key"]
                    if not isinstance(key, str):
                        continue
                    norm_key = key.strip().lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
                    colname = f"{crime}_{csv_type.replace('.csv','')}_{norm_key}"
                    feature_row[colname] = row["value"] / total

            except Exception as e:
                print(f"Skipping {file_path}: {e}")
                continue

    rows.append(feature_row)

# Save final feature matrix
df = pd.DataFrame(rows).fillna(0)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Feature set saved to {OUTPUT_CSV}")
