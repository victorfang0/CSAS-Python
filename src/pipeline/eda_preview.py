
import pandas as pd
import os

# Define paths - using absolute path since we know it
data_dir = "/Users/victor/Desktop/CSAS/DATA/"
files = ["Ends.csv", "Games.csv", "Stones.csv", "Teams.csv"]

def load_and_inspect():
    dfs = {}
    print(f"{'File':<15} | {'Shape':<15} | {'Columns'}")
    print("-" * 100)
    
    for f in files:
        path = os.path.join(data_dir, f)
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                dfs[f.split('.')[0]] = df
                print(f"{f:<15} | {str(df.shape):<15} | {', '.join(df.columns[:5])}...")
            except Exception as e:
                print(f"{f:<15} | ERROR: {e}")
        else:
            print(f"{f:<15} | NOT FOUND at {path}")

    # Deep dive into Ends.csv (Game states)
    if 'Ends' in dfs:
        ends = dfs['Ends']
        print("\n--- Ends.csv Columns ---")
        print(ends.columns.tolist())
        
        print("\n--- Sample Rows (Ends.csv) ---")
        print(ends.head(3).T)

    # Deep dive into Stones.csv (Rock locations)
    if 'Stones' in dfs:
        stones = dfs['Stones']
        print("\n--- Stones.csv Columns ---")
        print(stones.columns.tolist())

if __name__ == "__main__":
    load_and_inspect()
