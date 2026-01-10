
import pandas as pd
import numpy as np
import os

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"

def analyze_stats():
    ends_df = pd.read_csv(os.path.join(DATA_DIR, "Ends.csv"))
    stones_df = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    
    # Filter PP Ends
    pp_ends = ends_df[ends_df['PowerPlay'].notna() & (ends_df['PowerPlay'] != 0)].copy()
    
    # First Shots (Min ShotID)
    stones_sorted = stones_df.sort_values(by=['CompetitionID', 'GameID', 'EndID', 'ShotID'])
    first_shots = stones_sorted.groupby(['CompetitionID', 'GameID', 'EndID']).first().reset_index()
    
    # Merge
    merged = pd.merge(first_shots, pp_ends, on=['CompetitionID', 'GameID', 'EndID'], how='inner')
    
    # Categorize
    merged['Outcome'] = merged['Result'].apply(lambda x: 'Big_Win' if x >= 3 else ('Loss_Steal' if x <= 0 else 'Normal'))
    
    # Calculate Centroids for Big Win vs Loss
    print("--- Guard Location Strategy (Coordinates) ---")
    
    for outcome in ['Big_Win', 'Loss_Steal']:
        subset = merged[merged['Outcome'] == outcome]
        
        # Collect all validity X,Y
        all_x = []
        all_y = []
        
        for i in range(1, 13):
            xk = f'stone_{i}_x'
            yk = f'stone_{i}_y'
            # We assume the "Guard" is the stone roughly in the Guard Zone (Y > 2000? or Y near Hogline)
            # Actually, let's just take ALL stones present at start.
            if xk in subset.columns:
                vals_x = subset[xk].values
                vals_y = subset[yk].values
                mask = (vals_x > 200) & (vals_x < 4000) & (vals_y > 200) & (vals_y < 4000)
                all_x.extend(vals_x[mask])
                all_y.extend(vals_y[mask])
                
        if len(all_x) > 0:
            mean_x = np.mean(all_x)
            mean_y = np.mean(all_y)
            print(f"Outcome: {outcome} (N={len(subset)})")
            print(f"  Mean Stone Location: ({mean_x:.1f}, {mean_y:.1f})")
            
            # Distance from "Perfect Guard" (e.g. Center Line X=765)
            # Center Guard vs Corner Guard check
            # Center X = 765.
            diff_x = abs(mean_x - 765)
            print(f"  Avg Deviation from CenterLine: {diff_x:.1f} pixels")

if __name__ == "__main__":
    analyze_stats()
