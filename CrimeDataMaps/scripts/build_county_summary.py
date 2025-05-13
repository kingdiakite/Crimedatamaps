import os
import pandas as pd

INPUT_DIR = "data/usa"
CRIME_TYPES = ["homicide", "robbery", "rape", "aggravated_assault"]  
OUTPUT_FILE = "data/usa/county_crime_summary.csv"

rows = []

for county in os.listdir(INPUT_DIR):
    county_dir = os.path.join(INPUT_DIR, county)
    if not os.path.isdir(county_dir):
        continue

    crime_counts = {"county": county}
    
    for crime in CRIME_TYPES:
        crime_dir = os.path.join(county_dir, crime)
        if not os.path.isdir(crime_dir):
            crime_counts[crime] = 0
            continue

        # Total count = sum of all values in victim_age.csv (or offender_race.csv, etc.)
        total = 0
        for file in os.listdir(crime_dir):
            if not file.endswith(".csv"):
                continue
            try:
                df = pd.read_csv(os.path.join(crime_dir, file))
                value_col = "value" if "value" in df.columns else df.columns[-1]
                total += df[value_col].sum()
            except Exception as e:
                print(f"Skipping {county}/{crime}/{file}: {e}")
        
        crime_counts[crime] = total
    
    rows.append(crime_counts)

# Save final summary
summary_df = pd.DataFrame(rows)
summary_df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved summary to {OUTPUT_FILE}")