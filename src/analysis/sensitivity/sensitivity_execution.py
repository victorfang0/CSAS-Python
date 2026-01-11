
import pandas as pd
import numpy as np
import os

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"

def analyze_sensitivity():
    print("Loading Data...")
    ends_df = pd.read_csv(os.path.join(DATA_DIR, "Ends.csv"))
    stones_df = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    
    # 1. Prepare Data
    pp_ends = ends_df[ends_df['PowerPlay'].notna() & (ends_df['PowerPlay'] != 0)].copy()
    stones_sorted = stones_df.sort_values(by=['CompetitionID', 'GameID', 'EndID', 'ShotID'])
    first_shots = stones_sorted.groupby(['CompetitionID', 'GameID', 'EndID']).first().reset_index()
    
    # Merge
    merged = pd.merge(first_shots, pp_ends, on=['CompetitionID', 'GameID', 'EndID'], how='inner')
    
    print(f"Analyzing {len(merged)} Power Play ends for sensitivity...")
    
    thresholds = [2, 3, 4, 5]
    
    print("\n--- Execution Sensitivity Analysis (Threshold Testing) ---")
    print(f"{'Threshold':<10} | {'Win Count':<10} | {'Loss Count':<10} | {'Win X_mean':<10} | {'Loss X_mean':<10} | {'Delta X (px)':<15} | {'Delta (in)':<10}")
    print("-" * 105)
    
    for t in thresholds:
        # Define Groups
        wins = merged[merged['Result'] >= t]
        losses = merged[merged['Result'] <= 0]
        
        # Calculate Centroid for Wins
        win_x = []
        for i in range(1, 13):
            xk = f'stone_{i}_x'
            yk = f'stone_{i}_y'
            if xk in wins.columns:
                vals_x = wins[xk].values
                vals_y = wins[yk].values
                mask = (vals_x > 200) & (vals_x < 4000) & (vals_y > 200) & (vals_y < 4000)
                win_x.extend(vals_x[mask])
        
        mean_win = np.mean(win_x) if len(win_x) > 0 else 0
        
        # Calculate Centroid for Losses
        loss_x = []
        for i in range(1, 13):
            xk = f'stone_{i}_x'
            yk = f'stone_{i}_y'
            if xk in losses.columns:
                vals_x = losses[xk].values
                vals_y = losses[yk].values
                mask = (vals_x > 200) & (vals_x < 4000) & (vals_y > 200) & (vals_y < 4000)
                loss_x.extend(vals_x[mask])
                
        mean_loss = np.mean(loss_x) if len(loss_x) > 0 else 0
        
        delta_px = abs(mean_win - mean_loss)
        delta_in = (delta_px / 100) * 12
        
        print(f">= {t:<7} | {len(wins):<10} | {len(losses):<10} | {mean_win:<10.1f} | {mean_loss:<10.1f} | {delta_px:<15.1f} | {delta_in:<10.2f}")

    print("\n[Interpretation] Low Delta X (< 0.5 inches) indicates the Null Result is robust to the definition of 'Winning'.")

if __name__ == "__main__":
    analyze_sensitivity()
