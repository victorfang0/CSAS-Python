
import pandas as pd
import os

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"

def check_coords():
    df = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    
    # Check x and y columns
    x_cols = [c for c in df.columns if c.endswith('_x')]
    y_cols = [c for c in df.columns if c.endswith('_y')]
    
    print("--- Coordinate Ranges ---")
    
    # Stack all X values to get global min/max
    all_x = df[x_cols].stack()
    print(f"X Range: {all_x.min()} to {all_x.max()}")
    
    all_y = df[y_cols].stack()
    print(f"Y Range: {all_y.min()} to {all_y.max()}")
    
    # Check nulls
    print(f"Nulls in X: {all_x.isnull().sum()}")

if __name__ == "__main__":
    check_coords()
