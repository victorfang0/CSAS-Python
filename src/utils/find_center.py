
import pandas as pd
import numpy as np
import os

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"

def find_center():
    stones = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    
    x_cols = [c for c in stones.columns if c.endswith('_x')]
    y_cols = [c for c in stones.columns if c.endswith('_y')]
    
    all_x = []
    all_y = []
    
    sample = stones.sample(n=min(len(stones), 20000), random_state=42)
    
    for c in x_cols:
        vals = sample[c].dropna().values
        all_x.extend(vals[vals < 4000]) # Filter error codes
    for c in y_cols:
        vals = sample[c].dropna().values
        all_y.extend(vals[vals < 4000])
        
    x = np.array(all_x)
    y = np.array(all_y)
    
    print("--- Centroid Statistics ---")
    print(f"Mean X: {np.mean(x):.2f}")
    print(f"Mean Y: {np.mean(y):.2f}")
    print(f"Median X: {np.median(x):.2f}")
    print(f"Median Y: {np.median(y):.2f}")
    
    # Check if Y is bimodal (two ends?)
    # Print histogram of Y
    counts, bins = np.histogram(y, bins=20)
    print("\nY Coordinate Histogram:")
    for b, c in zip(bins, counts):
        print(f"{int(b)}-{int(b+(bins[1]-bins[0]))}: {c}")

    # Check X histogram (Side to side?)
    counts_x, bins_x = np.histogram(x, bins=20)
    print("\nX Coordinate Histogram:")
    for b, c in zip(bins_x, counts_x):
        print(f"{int(b)}-{int(b+(bins_x[1]-bins_x[0]))}: {c}")

if __name__ == "__main__":
    find_center()
