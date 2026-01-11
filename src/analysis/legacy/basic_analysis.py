
import pandas as pd
import numpy as np

DATA_PATH = "/Users/victor/Desktop/CSAS/analysis/modeling_data.csv"

def run_analysis():
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print("Data file not found. Ensure feature_engineering.py ran successfully.")
        return

    print("--- Basic Analysis Report ---")
    print(f"Total Data Points (End-Teams): {len(df)}")
    
    # 1. PP Frequency
    pp_count = df['PowerPlay_Active'].sum()
    print(f"\nPower Play Usage:")
    print(f"Total PP Ends: {pp_count}")
    print(f"Frequency: {pp_count / len(df):.2%}")
    
    # 2. Points Scored Analysis
    print(f"\nScoring Efficiency:")
    avg_score_all = df['PointsScored'].mean()
    avg_score_pp = df[df['PowerPlay_Active']]['PointsScored'].mean()
    avg_score_no_pp = df[~df['PowerPlay_Active']]['PointsScored'].mean()
    
    print(f"Avg Points (Overall): {avg_score_all:.2f}")
    print(f"Avg Points (With PP): {avg_score_pp:.2f}")
    print(f"Avg Points (No PP):   {avg_score_no_pp:.2f}")
    print(f"Comparative Gain (Raw Points): {avg_score_pp - avg_score_no_pp:.2f}")
    
    # 3. Score Differential Context
    # When do they use it?
    print(f"\nContextual Usage (Score Diff before PP):")
    pp_contexts = df[df['PowerPlay_Active']]['ScoreDiff']
    print(pp_contexts.describe())

if __name__ == "__main__":
    run_analysis()
