import os
import re
import shutil

# Full county prefix-to-name mapping
county_prefixes = {
    # San Diego
    "SDAA": "san_diego", "SDH": "san_diego", "SDR": "san_diego", "SDRob": "san_diego",
    # South San Francisco
    "SFAA": "south_san_francisco", "SFH": "south_san_francisco",
    "SFR": "south_san_francisco", "SFRob": "south_san_francisco",
    # Albany
    "ALBAA": "albany", "ALBH": "albany", "ALBR": "albany", "ALBRob": "albany",
    # Allegheny
    "AlleghenyAA": "allegheny", "AlleghenyH": "allegheny", "AlleghenyR": "allegheny", "AlleghenyRob": "allegheny",
    # Burleigh
    "BurleighAA": "burleigh", "BurleighH": "burleigh", "BurleighR": "burleigh", "BurleighRob": "burleigh",
    # Cass
    "CassAA": "cass", "CassH": "cass", "CassR": "cass", "CassRob": "cass",
    # Dallas
    "DTXAA": "dallas", "DTXH": "dallas", "DTXR": "dallas", "DTXRob": "dallas",
    # Harris 
    "HTXAA": "harris", "HTXH": "harris", "HTXR": "harris", "HTXRob": "harris",
    # Philadelphia
    "PHILLYAA": "philadelphia", "PHILLYH": "philadelphia", "PHILLYR": "philadelphia", "PHILLYRob": "philadelphia",
    # Laramie 
    "LaramieAA": "laramie", "LaramieH": "laramie", "LaramieR": "laramie", "LaramieRob": "laramie",
    # Natrona
    "NatronaAA": "natrona", "NatronaH": "natrona", "NatronaR": "natrona", "NatronaRob": "natrona",
    # New York County
    "NYCAA": "new_york_county", "NYCH": "new_york_county", "NYCR": "new_york_county", "NYCRob": "new_york_county",
    # Duval
    "DuvalAA": "duval", "DuvalH": "duval", "DuvalR": "duval", "DuvalRob": "duval",
    # Minnehaha
    "MinnehaAA": "minnehaha", "MinnehaH": "minnehaha", "MinnehaR": "minnehaha", "MinnehaRob": "minnehaha",
    # Pennington
    "PenningAA": "pennington", "PenningH": "pennington", "PenningR": "pennington", "PenningRob": "pennington",
    # Kent
    "KentAA": "kent", "KentH": "kent", "KentR": "kent", "KentRob": "kent",
    # New Castle
    "NewCastleAA": "new_castle", "NewCastleH": "new_castle", "NewCastleR": "new_castle", "NewCastleRob": "new_castle",
    # Miami
    "MiamiAA": "miami", "MiamiH": "miami", "MiamiR": "miami", "MiamiRob": "miami"
}
 
# Map prefix suffix to crime type
def resolve_crime_code(prefix):
    if "Rob" in prefix:
        return "robbery"
    elif "H" in prefix:
        return "homicide"
    elif "R" in prefix:
        return "rape"
    elif "AA" in prefix:
        return "aggravated_assault"
    return "unknown"

# Determine type of data from filename
def detect_file_type(filename):
    if "Offender age" in filename:
        return "offender_age.csv"
    elif "Weapon" in filename:
        return "weapon_type.csv"
    elif "Location" in filename:
        return "location_type.csv"
    return None

# Extract prefix like "PHILLYR", "DTXRob", etc.
def extract_prefix(filename):
    match = re.match(r"([A-Za-z]+(?:AA|H|R|Rob))", filename)
    return match.group(1) if match else None

# Ensure full folder structure exists
def create_all_folders(dest_root="data/usa"):
    counties = set(county_prefixes.values())
    crimes = ["aggravated_assault", "homicide", "rape", "robbery"]
    for county in counties:
        for crime in crimes:
            os.makedirs(os.path.join(dest_root, county, crime), exist_ok=True)

# Main organization logic
def organize_files(base_dir="~/Downloads", dest_root="data/usa"):
    base_dir = os.path.expanduser(base_dir)
    os.makedirs(dest_root, exist_ok=True)  # Create data/usa if missing
    create_all_folders(dest_root)

    for file in os.listdir(base_dir):
        if not file.endswith(".csv"):
            continue

        prefix = extract_prefix(file)
        if not prefix:
            print(f"Skipping unmatchable filename: {file}")
            continue

        county = county_prefixes.get(prefix)
        crime = resolve_crime_code(prefix)
        file_type = detect_file_type(file)

        if not county:
            print(f"Skipping unknown prefix: {prefix}")
            continue
        if crime == "unknown" or not file_type:
            print(f"Skipping unrecognized crime/type: {file}")
            continue

        src_path = os.path.join(base_dir, file)
        dest_path = os.path.join(dest_root, county, crime, file_type)

        shutil.copy(src_path, dest_path)
        print(f"Moved {file} → {dest_path}")

if __name__ == "__main__":
    organize_files()

 