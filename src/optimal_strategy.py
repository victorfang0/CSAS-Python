
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

MODEL_PATH = "/Users/victor/Desktop/CSAS/models/wp_rf.pkl"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"

def generate_strategy():
    print("Loading Model...")
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
        
    # Create Simulation Grid
    # ScoreDiff: -4 to +4
    # EndID: 1 to 7 (Can't use PP in 8th/Extra usually? Or just regular ends)
    # Hammer: Always 1 (You have hammer to use PP)
    
    score_diffs = range(-4, 5) # -4 to +4
    ends = range(1, 8)
    
    heatmap_data = [] # List of dicts
    
    print("Simulating Game States...")
    for end in ends:
        row_wpa = []
        for diff in score_diffs:
            # Case 1: Use PP
            # Feature Order: ['EndID', 'ScoreDiff', 'Hammer', 'PowerPlay_Active']
            # Make sure to match training order!
            feat_pp = [[end, diff, 1, 1]]
            prob_pp = model.predict_proba(feat_pp)[0][1]
            
            # Case 2: Normal
            feat_norm = [[end, diff, 1, 0]]
            prob_norm = model.predict_proba(feat_norm)[0][1]
            
            # WPA
            wpa = prob_pp - prob_norm
            
            # Additional: Opportunity Cost Logic
            # Gain must be SIGNIFICANT to use it early.
            # Using raw WPA for now.
            
            heatmap_data.append({
                'End': end,
                'ScoreDiff': diff,
                'WPA': wpa
            })
            
    df_sim = pd.DataFrame(heatmap_data)
    
    # Pivot for Heatmap
    # Index: ScoreDiff (descending), Columns: End
    pivot_wpa = df_sim.pivot(index='ScoreDiff', columns='End', values='WPA')
    pivot_wpa = pivot_wpa.sort_index(ascending=False)
    
    print("Plotting Strategy Heatmap...")
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_wpa, annot=True, fmt=".1%", cmap="RdBu_r", center=0)
    plt.title("Comparative Gain (Win Probability Added) by Using Power Play")
    plt.ylabel("Score Differential (Pos=Leading, Neg=Trailing)")
    plt.xlabel("End Number")
    
    out_path = os.path.join(OUTPUT_DIR, "optimal_strategy_heatmap.png")
    plt.savefig(out_path)
    print(f"Saved heatmap to {out_path}")
    
    # Recommendation
    best_case = df_sim.loc[df_sim['WPA'].idxmax()]
    print("\n--- Optimal Strategy Found ---")
    print(f"Best Time to Use PP: End {int(best_case['End'])}, Score Diff {int(best_case['ScoreDiff'])}")
    print(f"Gain: +{best_case['WPA']:.2%}")

if __name__ == "__main__":
    generate_strategy()
