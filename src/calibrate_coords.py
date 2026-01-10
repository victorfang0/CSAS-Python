
import pandas as pd
import numpy as np
import os

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"

def calibrate_scale():
    stones = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    
    # Hypothesis from Find Center: (765, 740)
    center_x = 765
    center_y = 740
    
    # Filter valid coords
    x_cols = [c for c in stones.columns if c.endswith('_x')]
    y_cols = [c for c in stones.columns if c.endswith('_y')]
    
    all_x = []
    all_y = []
    
    # Sample to save memory
    sample = stones.sample(n=min(len(stones), 20000), random_state=42)
    
    for c in x_cols:
        all_x.extend(sample[c].dropna().values)
    for c in y_cols:
        all_y.extend(sample[c].dropna().values)
        
    x = np.array(all_x)
    y = np.array(all_y)
    
    # Calculate distance from center
    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    
    print(f"--- Calibration Stats ---")
    print(f"Center Assumed: ({center_x}, {center_y})")
    print(f"Mean Distance: {np.mean(dist):.2f}")
    print(f"Median Distance: {np.median(dist):.2f}")
    print(f"90th Percentile Distance: {np.percentile(dist, 90):.2f}")
    
    # Standard House Radius is 6 feet (12ft diameter)
    # Most stones land in the house.
    # Let's assume the 90th percentile roughly correlates to the edge of the house (radius 6ft) or slightly outside.
    # Or better: The bunching should be inside the 4ft ring (radius 2ft) or 8ft ring?
    # Actually, in mixed doubles, many stones are in the 4ft.
    
    # Let's verify if the distribution has a drop-off.
    # We'll print histogram buckets of distance
    counts, bins = np.histogram(dist, bins=20, range=(0, 2000))
    print("\nDistance Histogram (bins of 100 units):")
    for b, c in zip(bins, counts):
        print(f"{int(b)}-{int(b+100)}: {c}")

if __name__ == "__main__":
    calibrate_scale()
