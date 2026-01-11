
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

DATA_PATH = "/Users/victor/Desktop/CSAS/documentation/artifacts/modeling_data.csv"

def analyze_strategy_sensitivity():
    print("Loading Data...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print("Modeling data not found.")
        return

    # Features
    features = ['EndID', 'ScoreDiff', 'Hammer', 'PowerPlay_Active']
    target = 'Won_Game'
    
    # Preprocessing
    df['Hammer'] = df['Hammer'].astype(int)
    df['PowerPlay_Active'] = df['PowerPlay_Active'].astype(int)
    
    X = df[features]
    y = df[target].astype(int)
    
    # Test Scenario: End 6, Trailing by 2, With Hammer. To PP or Not to PP?
    # This is the "Catch-Up Rule" hotspot.
    scenario_pp = pd.DataFrame({'EndID': [6], 'ScoreDiff': [-2], 'Hammer': [1], 'PowerPlay_Active': [1]})
    scenario_no_pp = pd.DataFrame({'EndID': [6], 'ScoreDiff': [-2], 'Hammer': [1], 'PowerPlay_Active': [0]})
    
    n_iterations = 20
    wpa_results = []
    decisions = []
    
    print("\n--- Strategy Sensitivity Analysis (Bootstrapping) ---")
    print(f"Scenario: End 6, Score -2, Hammer=True")
    print(f"Goal: Test if the 'Use Power Play' recommendation is stable across {n_iterations} random training sets.\n")
    print(f"{'Run':<5} | {'WPA':<10} | {'Decision':<10}")
    print("-" * 35)
    
    for i in range(n_iterations):
        # Bootstrap Resample (80% of data, with replacement)
        X_sample, _, y_sample, _ = train_test_split(X, y, train_size=0.8, random_state=i) # Vary random state effectively samples differently
        
        # Train Model
        clf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42) # Keep max_depth=5 as per methodology
        clf.fit(X_sample, y_sample)
        
        # Predict
        p_pp = clf.predict_proba(scenario_pp)[0][1]
        p_no = clf.predict_proba(scenario_no_pp)[0][1]
        
        wpa = p_pp - p_no
        decision = "USE PP" if wpa > 0 else "NO PP"
        
        wpa_results.append(wpa)
        decisions.append(1 if wpa > 0 else 0)
        
        print(f"{i+1:<5} | {wpa:+.4f}     | {decision}")
        
    # Summary Stats
    mean_wpa = np.mean(wpa_results)
    std_wpa = np.std(wpa_results)
    stability = (sum(decisions) / n_iterations) * 100
    
    print("-" * 35)
    print(f"Mean WPA: {mean_wpa:+.4f}")
    print(f"Std Dev:  {std_wpa:.4f}")
    print(f"Stability: {stability:.0f}% of models recommend Power Play.")
    
    if std_wpa < 0.05 and stability > 90:
        print("\nConclusion: The Strategy is ROBUST. Noise in the data does not flip the decision.")
    else:
        print("\nConclusion: The Strategy is SENSITIVE. Small data changes might flip the decision.")

if __name__ == "__main__":
    analyze_strategy_sensitivity()
