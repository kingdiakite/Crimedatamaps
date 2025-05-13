import matplotlib.pyplot as plt
import seaborn as sns
from scripts.clean_fbi_data import clean_fbi_csv

def plot_side_by_side(national_df, state_df, title, ylabel, save_path):
    combined_df = national_df.set_index("key").join(
        state_df.set_index("key"),
        lsuffix="_nat",
        rsuffix="_state",
        how="inner"
    ).reset_index()

    combined_df = combined_df.rename(columns={
        "value_nat": "California",
        "value_state": "Florida"
    })

    combined_df = combined_df.sort_values("California", ascending=False)

    plt.figure(figsize=(12, 8))
    bar_width = 0.4
    x = range(len(combined_df))

    plt.barh(
        [i + bar_width for i in x], combined_df["California"], 
        height=bar_width, label="California", color="skyblue"
    )
    plt.barh(
        x, combined_df["Florida"], 
        height=bar_width, label="Florida", color="coral"
    )

    plt.yticks([i + bar_width / 2 for i in x], combined_df["key"])
    plt.xlabel("Number of Homicides")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_all_comparisons():
    # Clean both versions of each dataset
    cal_age = clean_fbi_csv("data/california_offender_age.csv")
    fl_age = clean_fbi_csv("data/florida_offender_age.csv")
    plot_side_by_side(
        cal_age, fl_age,
        title="Homicides by Offender Age Group",
        ylabel="Age Group",
        save_path="outputs/figures/compare_offender_age.png"
    )

    cal_weapon = clean_fbi_csv("data/california_weapon_type.csv")
    fl_weapon = clean_fbi_csv("data/florida_weapon_type.csv")
    plot_side_by_side(
        cal_weapon, fl_weapon,
        title="Homicides by Weapon Type",
        ylabel="Weapon Type",
        save_path="outputs/figures/compare_weapon_type.png"
    )

    cal_loc = clean_fbi_csv("data/california_location_type.csv")
    fl_loc = clean_fbi_csv("data/florida_location_type.csv")
    plot_side_by_side(
        cal_loc, fl_loc,
        title="Homicides by Location Type",
        ylabel="Location Type",
        save_path="outputs/figures/compare_location_type.png"
    )
