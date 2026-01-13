
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.ensemble import RandomForestClassifier

# Paths
DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"

def visualize_win_prob_heatmap():
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
        # Fallback if unpickled model doesn't store names (unlikely with sklearn > 1.0)
        features = ['ScoreDiff', 'EndID', 'Hammer', 'PowerPlay_Active']
        
    print(f"Model expects features: {features}")
    
    # 2. PRODUCE HEATMAP DATA
    ends_range = list(range(1, 9))
    score_range = list(range(-4, 5)) 
    
    heatmap_data = []
    
    print("Simulating Game States...")
    for score in score_range:
        row = []
        for end in ends_range:
            # Create synthetic state dictionary
            state_dict = {
                'ScoreDiff': score,
                'EndID': end,
                'Hammer': 1,
                'PowerPlay_Active': 0,
                # Add default 0 for any other features the model might have used (e.g. Interactions)
            }
            # Fill missing keys with 0 just in case
            for f in features:
                if f not in state_dict:
                    state_dict[f] = 0
            
            # Create DF in correct order
            state = pd.DataFrame([state_dict])[features]
            
            # Predict Probability of "Winning"
            prob = rf.predict_proba(state)[0][1] # Probability of Class 1
            row.append(prob)
        heatmap_data.append(row)
        
    # Convert to DataFrame for Seaborn
    # Rows = Scores (Top is +4, Bottom is -4)
    # Cols = Ends (1 to 8)
    
    # Note: Heatmap origin is usually top-left. We want +4 at top.
    # score_range was -4..+4. So row 0 is -4. 
    # We should reverse it so +4 is at index 0 (top).
    heatmap_data.reverse()
    score_labels = list(reversed(score_range))
    
    df_viz = pd.DataFrame(heatmap_data, index=score_labels, columns=ends_range)
    
    # 3. PLOT
    plt.figure(figsize=(12, 10))
    # Using 'plasma' or 'viridis' to match the scientific style of the reference images
    sns.heatmap(df_viz, annot=True, fmt=".2f", cmap="viridis", cbar_kws={'label': 'Win Probability'})
    
    plt.title("The Landscape of Victory\n(Win Prob by Score & End, with Hammer)")
    plt.ylabel("Score Differential (My Team)")
    plt.xlabel("End Number")
    
    out_path = os.path.join(OUTPUT_DIR, "win_prob_heatmap.png")
    plt.savefig(out_path)
    print(f"Saved heatmap to {out_path}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    visualize_win_prob_heatmap()
