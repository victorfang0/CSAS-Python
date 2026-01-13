
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.ensemble import RandomForestClassifier

# Paths
DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"

def visualize_wpa_strategy():
    model_path = os.path.join("/Users/victor/Desktop/CSAS", "models", "wp_rf.pkl")
    print(f"Loading Pre-Trained Model from {model_path}...")
    try:
        import joblib
        rf = joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Features expected by the model (Strict Order)
    if hasattr(rf, "feature_names_in_"):
        features = list(rf.feature_names_in_)
    else:
        features = ['ScoreDiff', 'EndID', 'Hammer', 'PowerPlay_Active']
        
    print(f"Model features: {features}")
    
    # 2. PRODUCE WPA DATA
    ends_range = list(range(1, 9))
    score_range = list(range(-4, 5)) 
    
    heatmap_data = []
    
    print("Simulating Twin Earths (WPA Calculation)...")
    for score in score_range:
        row = []
        for end in ends_range:
            # Base dict
            base_dict = {
                'ScoreDiff': score,
                'EndID': end,
                'Hammer': 1,
            }
            
            # Earth A: WITH Power Play
            state_pp_dict = base_dict.copy()
            state_pp_dict['PowerPlay_Active'] = 1
            # Fill missing
            for f in features:
                if f not in state_pp_dict: state_pp_dict[f] = 0
            state_pp = pd.DataFrame([state_pp_dict])[features]
            
            prob_pp = rf.predict_proba(state_pp)[0][1]
            
            # Earth B: WITHOUT Power Play (Standard)
            state_norm_dict = base_dict.copy()
            state_norm_dict['PowerPlay_Active'] = 0
            # Fill missing
            for f in features:
                if f not in state_norm_dict: state_norm_dict[f] = 0
            state_normal = pd.DataFrame([state_norm_dict])[features]
            
            prob_normal = rf.predict_proba(state_normal)[0][1]
            
            # WPA
            wpa = (prob_pp - prob_normal) * 100 # In Percentage Points
            row.append(wpa)
            
        heatmap_data.append(row)
        
    # Format for Plotting
    heatmap_data.reverse()
    score_labels = list(reversed(score_range))
    
    df_viz = pd.DataFrame(heatmap_data, index=score_labels, columns=ends_range)
    
    # 3. PLOT
    plt.figure(figsize=(12, 10))
    
    # Use a DIVERGING colormap (RdBu_r: Blue=Positive, Red=Negative)
    # Center at 0.
    sns.heatmap(df_viz, annot=True, fmt=".1f", cmap="viridis", cbar_kws={'label': 'WPA (Percentage Points)'})
    
    plt.title("Strategic Value of the Power Play (Results from Section 3)\n(Positive = Use PP, Negative = Avoid PP)")
    plt.ylabel("Score Differential (My Team)")
    plt.xlabel("End Number")
    
    out_path = os.path.join(OUTPUT_DIR, "wpa_strategy_heatmap.png")
    plt.savefig(out_path)
    print(f"Saved WPA heatmap to {out_path}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    visualize_wpa_strategy()
