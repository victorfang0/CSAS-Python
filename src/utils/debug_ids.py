
import pandas as pd
import os

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"

def debug_ids():
    ends = pd.read_csv(os.path.join(DATA_DIR, "Ends.csv"))
    games = pd.read_csv(os.path.join(DATA_DIR, "Games.csv"))
    
    ends_ids = set(ends['GameID'].unique())
    games_ids = set(games['GameID'].unique())
    
    print(f"Ends Game IDs: {len(ends_ids)}")
    print(f"Games Game IDs: {len(games_ids)}")
    print(f"Intersection: {len(ends_ids.intersection(games_ids))}")
    
    # Check Team IDs
    print("\n--- Team IDs ---")
    ends_teams = set(ends['TeamID'].unique())
    games_teams = set(games['TeamID1'].unique()).union(set(games['TeamID2'].unique()))
    print(f"Ends Teams: {len(ends_teams)}")
    print(f"Games Teams: {len(games_teams)}")
    print(f"Intersection: {len(ends_teams.intersection(games_teams))}")

if __name__ == "__main__":
    debug_ids()
