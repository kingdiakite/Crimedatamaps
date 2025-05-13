import os
import pandas as pd

root_dir = "data/clean"
header_map = {
    "location_type": "key",
    "count": "value"
}

for root, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            df = pd.read_csv(file_path)
            if list(df.columns) == ["key", "value"]:
                df.columns = ["location_type", "count"]
                df.to_csv(file_path, index=False)
                print(f"Fixed headers in {file_path}")