
import pandas as pd
import os

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"

def debug_stones():
    df = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    print("Columns:", df.columns.tolist())
    if 'ShotID' in df.columns:
        print("Unique ShotID values:", sorted(df['ShotID'].unique()))
    else:
        print("ShotID column not found!")

if __name__ == "__main__":
    debug_stones()
