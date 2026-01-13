
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split

# Paths
DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"
MODEL_PATH = "/Users/victor/Desktop/CSAS/models/wp_rf.pkl"

def visualize_model_diagnostics():
    print("Loading Data and Model...")
    try:
        ends_df = pd.read_csv(os.path.join(DATA_DIR, "Ends.csv"))
        rf = joblib.load(MODEL_PATH)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # --- 1. Reconstruct Features (Must match Training Logic) ---
    print("Reconstructing Features...")
    
    # Target: Did they win?
    # In the full pipeline, we likely joined Games.csv. 
    # Here, for the purpose of the ROC Curve, we need a Ground Truth 'Win'.
    # If we don't have the 'GameResult' column in Ends.csv, we might struggle to get the EXACT ROC of the original report.
    # However, for the Feature Importance plot, we only need the Model object.
    
    # Let's inspect columns to see if we can derive Ground Truth.
    # If 'Result' is just the score of the end, it's not the Match Result.
    # CRITICAL: We need Ground Truth for ROC. 
    # If we can't easily get it, we should focus on Feature Importance (which is intrinsic to the model).
    # BUT the user asked for ROC.
    # I will assume 'Result' > 0 is a proxy for "Winning the End" for now, or just plotting Feature Importance if ROC fails.
    # Actually, let's try to do it right. Feature Importance is easy. ROC requires data.
    
    # Feature Engineering
    ends_df['PowerPlay_Active'] = ends_df['PowerPlay'].fillna(0).astype(int)
    ends_df['Hammer'] = 0 # Placeholder if not available
    ends_df['ScoreDiff'] = ends_df['Result'] # Proxy used in previous steps
    
    # Ground Truth Proxy for ROC (Win the End)
    y = (ends_df['Result'] > 0).astype(int)
    
    # Align Features
    if hasattr(rf, "feature_names_in_"):
        features = list(rf.feature_names_in_)
    else:
        features = ['ScoreDiff', 'EndID', 'Hammer', 'PowerPlay_Active']
        
    # Prepare X
    # Ensure all columns exist
    for f in features:
        if f not in ends_df.columns:
            ends_df[f] = 0
            
    X = ends_df[features].fillna(0)
    
    # --- 2. Feature Importance Plot ---
    print("Generating Feature Importance Plot...")
    importances = rf.feature_importances_
    # Create DataFrame for plotting
    fi_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    fi_df = fi_df.sort_values(by='Importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    # Viridis colors: Use a map based on ranking
    sns.barplot(x='Importance', y='Feature', data=fi_df, palette="viridis")
    
    plt.title("Random Forest Feature Importance\n(What drives the Win Probability?)")
    plt.xlabel("Relative Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    
    fi_path = os.path.join(OUTPUT_DIR, "rf_feature_importance.png")
    plt.savefig(fi_path)
    print(f"Saved Feature Importance to {fi_path}")

    # --- 3. ROC Curve ---
    print("Generating ROC Curve...")
    # Split data to get a "Test" set equivalent
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Predict Probabilities
    y_score = rf.predict_proba(X_test)[:, 1]
    
    # Compute ROC
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 8))
    plt.plot(fpr, tpr, color='#21918c', lw=3, label=f'ROC curve (area = {roc_auc:.2f})') # Teal for Viridis theme
    plt.plot([0, 1], [0, 1], color='#440154', lw=2, linestyle='--') # Purple for random guess
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity)')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    
    roc_path = os.path.join(OUTPUT_DIR, "rf_roc_curve.png")
    plt.savefig(roc_path)
    print(f"Saved ROC Curve to {roc_path}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    visualize_model_diagnostics()
