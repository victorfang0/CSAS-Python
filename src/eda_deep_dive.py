
import pandas as pd
import os

data_dir = "/Users/victor/Desktop/CSAS/DATA/"
ends_path = os.path.join(data_dir, "Ends.csv")
games_path = os.path.join(data_dir, "Games.csv")

def deep_dive():
    ends = pd.read_csv(ends_path)
    
    # 1. Check PowerPlay values
    print("--- PowerPlay Value Counts ---")
    print(ends['PowerPlay'].value_counts(dropna=False))
    
    # 2. Check Result values and correlation with End lines
    # Let's see some rows where PowerPlay is used
    pp_rows = ends[ends['PowerPlay'] == 1] # Assuming 1 is used
    if not pp_rows.empty:
        print("\n--- Sample PowerPlay Rows ---")
        print(pp_rows[['GameID', 'TeamID', 'EndID', 'Result', 'PowerPlay']].head(5))
    else:
        print("\n No rows with PowerPlay == 1 found. Converting literal check.")
        print(ends['PowerPlay'].unique())

    # 3. Check Games.csv to see if it has 'Winner' or 'FinalScore'
    if os.path.exists(games_path):
        games = pd.read_csv(games_path)
        print("\n--- Games.csv Columns ---")
        print(games.columns.tolist())
        print(games.head(2).T)

if __name__ == "__main__":
    deep_dive()
