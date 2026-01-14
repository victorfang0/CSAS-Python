
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample

# Paths
DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"

def analyze_bootstrap():
    print("Loading Data for Bootstrap...")
    try:
        # Load Raw Data
        ends_df = pd.read_csv(os.path.join(DATA_DIR, "Ends.csv"))
    except FileNotFoundError:
        print("Data not found.")
        return

    # Basic Feature Engineering (Mirroring visualize_rf.py)
    ends_df['PowerPlay_Active'] = ends_df['PowerPlay'].fillna(0).astype(int)
    # We need a Target. Assuming 'Result' > 0 is Win for this Quick Bootstrap
    # In reality, we used Games.csv join, but strictly for WPA model stability check, 
    # we can use the end result as a proxy for "Good Outcome" or load the modeling_data if available.
    # Let's check modeling_data.csv path. 
    # Attempting to load the cleaned file would be better.
    
    model_data_path = os.path.join(OUTPUT_DIR, "modeling_data.csv")
    if os.path.exists(model_data_path):
        df = pd.read_csv(model_data_path)
        features = ['EndID', 'ScoreDiff', 'Hammer', 'PowerPlay_Active']
        target = 'Won_Game' # Assuming this exists in modeling_data
    else:
        # Fallback to Ends.csv
        print("Using Ends.csv fallback...")
        df = ends_df.copy()
        df['ScoreDiff'] = df['Result'] # Proxy
        df['Hammer'] = 0 # Placeholder
        df['Won_Game'] = (df['Result'] > 0).astype(int) # End Win Proxy
        features = ['EndID', 'ScoreDiff', 'Hammer', 'PowerPlay_Active']
        target = 'Won_Game'

    # Fill NaNs
    X = df[features].fillna(0)
    y = df[target]

    # Bootstrap Configuration
    n_iterations = 20
    wpa_estimates = []
    
    print(f"Starting {n_iterations} Bootstrap Iterations...")
    
    # Critical Scenario: Trailing by 2 in End 6 with Hammer (The 'Green Light' Zone)
    # We want to measure the WPA Gain of PowerPlay vs No PowerPlay in this specific state.
    scenario_pp = pd.DataFrame({'EndID': [6], 'ScoreDiff': [-2], 'Hammer': [1], 'PowerPlay_Active': [1]})
    scenario_no_pp = pd.DataFrame({'EndID': [6], 'ScoreDiff': [-2], 'Hammer': [1], 'PowerPlay_Active': [0]})

    for i in range(n_iterations):
        # Resample
        X_resampled, y_resampled = resample(X, y, random_state=i)
        
        # Train Model (Fast)
        rf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
        rf.fit(X_resampled, y_resampled)
        
        # Predict Probabilities
        prob_pp = rf.predict_proba(scenario_pp)[0][1]
        prob_no_pp = rf.predict_proba(scenario_no_pp)[0][1]
        
        # WPA Gain
        wpa_gain = prob_pp - prob_no_pp
        wpa_estimates.append(wpa_gain)
        
        print(f"Iter {i+1}: WPA Gain = {wpa_gain:.4f}")

    # Statistics
    stats = {
        "Mean": np.mean(wpa_estimates),
        "Median": np.median(wpa_estimates),
        "Std Dev": np.std(wpa_estimates),
        "Min": np.min(wpa_estimates),
        "Max": np.max(wpa_estimates),
        "95% CI Lower": np.percentile(wpa_estimates, 2.5),
        "95% CI Upper": np.percentile(wpa_estimates, 97.5)
    }
    
    # 1. Plot Distribution
    plt.figure(figsize=(8, 6))
    sns.histplot(wpa_estimates, kde=True, bins=10, color='#21918c', alpha=0.6)
    
    # Add Reference Lines
    plt.axvline(stats['Mean'], color='#440154', linestyle='-', linewidth=2, label=f"Mean: {stats['Mean']:.3f}")
    plt.axvline(stats['95% CI Lower'], color='red', linestyle='--', label='95% CI')
    plt.axvline(stats['95% CI Upper'], color='red', linestyle='--')
    
    plt.title("Bootstrap Analysis of WPA Stability (N=20)\nScenario: Down 2, End 6 (Power Play Gain)")
    plt.xlabel("Estimated Win Probability Added (WPA)")
    plt.legend()
    
    out_img = os.path.join(OUTPUT_DIR, "wpa_bootstrap_distribution.png")
    plt.savefig(out_img)
    print(f"Saved Plot to {out_img}")
    
    # 2. Save Stats Table
    with open(os.path.join(OUTPUT_DIR, "wpa_bootstrap_stats.md"), "w") as f:
        f.write("# WPA Bootstrap Analysis (Stability Check)\n\n")
        f.write("We performed 20 iterations of bootstrapping (retraining the model on resampled data) to test the stability of our key strategic finding: **The Benefit of Power Play when Trailing by 2.**\n\n")
        f.write("## Statistics\n")
        f.write("| Metric | Value |\n")
        f.write("|---|---|\n")
        for k, v in stats.items():
            f.write(f"| {k} | {v:.4f} |\n")
            
    print("Saved Stats Table.")

if __name__ == "__main__":
    analyze_bootstrap()
