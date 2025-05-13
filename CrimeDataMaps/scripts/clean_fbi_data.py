import os
import pandas as pd

ROOT_DIR = "data/usa"

def clean_csv(path):
    try:
        df = pd.read_csv(path)
        df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
        df = df.dropna(how='all')
        df = df.loc[:, ~df.columns.str.contains('unnamed')]
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df.to_csv(path, index=False)
        print(f"Cleaned: {path}")
    except Exception as e:
        print(f"Failed to clean {path}: {e}")

def walk_and_clean(root):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".csv"):
                clean_csv(os.path.join(dirpath, filename))

if __name__ == "__main__":
    walk_and_clean(ROOT_DIR)
