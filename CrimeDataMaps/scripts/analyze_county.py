# Generate bar plots for offender age, location, and weapon use per county
import pandas as pd
import matplotlib.pyplot as plt
import os

CRIME_TYPES = ["homicide", "rape", "robbery", "aggravated_assault"]
DATA_DIR = "data/usa"
OUTPUT_DIR = "output/plots"

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty or df.shape[1] < 2:
            return None
        return df
    except Exception:
        return None

def plot_and_save(df, x_col, y_col, title, output_path):
    if df is None:
        return
    plt.figure()
    df.plot(kind="bar", x=x_col, y=y_col, legend=False)
    plt.title(title)
    plt.xlabel(x_col.replace("_", " ").title())
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, format='pdf')
    plt.close()

def analyze_county(county):
    for crime in CRIME_TYPES:
        base_path = os.path.join(DATA_DIR, county, crime)

        location_df = load_csv(os.path.join(base_path, "location_type.csv"))
        age_df = load_csv(os.path.join(base_path, "offender_age.csv"))
        weapon_df = load_csv(os.path.join(base_path, "weapon_type.csv"))

        plot_and_save(location_df, "key", "value",
              f"{crime.title()} Locations in {county.title()}",
              f"{OUTPUT_DIR}/{county}/{crime}/location.pdf")

        plot_and_save(age_df, "key", "value",
              f"{crime.title()} Offender Ages in {county.title()}",
              f"{OUTPUT_DIR}/{county}/{crime}/age.pdf")


        plot_and_save(weapon_df, "key", "value",
                      f"{crime.title()} Weapon Types in {county.title()}",
                      f"{OUTPUT_DIR}/{county}/{crime}/weapon.pdf")

def main():
    counties = [d for d in os.listdir(DATA_DIR)
                if os.path.isdir(os.path.join(DATA_DIR, d))]

    for county in counties:
        print(f"Processing {county}...")
        analyze_county(county)

    print("Done generating all plots.")

if __name__ == "__main__":
    main()
