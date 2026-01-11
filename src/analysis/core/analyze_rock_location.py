
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import seaborn as sns

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"

def analyze_shot_selection():
    print("Loading Data...")
    ends_df = pd.read_csv(os.path.join(DATA_DIR, "Ends.csv"))
    stones_df = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    
    # 1. Prepare Ends Data (Target)
    # Filter for Power Play Ends only
    pp_ends = ends_df[ends_df['PowerPlay'].notna() & (ends_df['PowerPlay'] != 0)].copy()
    
    # Create a composite key string for easier matching if needed, or just iterate
    # We will merge on ['CompetitionID', 'GameID', 'EndID']
    # Note: Stones.csv has SessionID too
    
    # 2. Prepare Stones Data (Features)
    # ShotID values are [7, 8, 9...], likely starting at 7 for this dataset?
    # We want the FIRST RECORDED STATE of the end.
    
    # Sort by keys + ShotID
    stones_sorted = stones_df.sort_values(by=['CompetitionID', 'GameID', 'EndID', 'ShotID'])
    
    # Take the first shot of every end
    first_shots = stones_sorted.groupby(['CompetitionID', 'GameID', 'EndID']).first().reset_index()
    
    print(f"Total PP Ends found: {len(pp_ends)}")
    print(f"Total First Shots found: {len(first_shots)}")
    
    # Merge
    # Ensure types match
    join_cols = ['CompetitionID', 'GameID', 'EndID']
    merged = pd.merge(first_shots, pp_ends, on=join_cols, how='inner')
    
    print(f"Merged Data Points: {len(merged)}")
    
    if len(merged) < 10:
        print("Not enough data to analyze. Check join keys.")
        return

    # 3. Analyze relationship: Stone Location vs Points
    # We care about the location of the JUST THROWN stone.
    # Which "Stone_i" corresponds to Shot 1?
    # The Description says: "Stone_1 and Stone_7 are the pre-placed stones"
    # "Teams throw the rest... Team 1 throws stones 2-6".
    # So ShotID 1 is likely throwing "Stone 2" (if Team 1) or "Stone 8" (if Team 2)?
    # Or does `Stone_i_x` update? 
    # Let's assume we want to see ALL stones on the sheet.
    
    # Hypothesis: Winning ends (3+ pts) have guards in different spots than Losing ends (0-1 pts).
    # Categorize Result
    merged['Outcome'] = merged['Result'].apply(lambda x: 'Big_Win' if x >= 3 else ('Loss_Steal' if x <= 0 else 'Normal'))
    
    # Let's collect coordinates of ALL stones on the board at Shot 1
    # For each outcome type.
    
    outcomes = ['Big_Win', 'Loss_Steal']
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Coordinates
    CENTER_X, CENTER_Y = 765, 740
    SCALE = 100
    
    for ax, outcome in zip(axes, outcomes):
        subset = merged[merged['Outcome'] == outcome]
        
        all_x = []
        all_y = []
        
        # Collect all valid stone positions in this subset
        for i in range(1, 13):
            xk = f'stone_{i}_x'
            yk = f'stone_{i}_y'
            if xk in subset.columns:
                vals_x = subset[xk].values
                vals_y = subset[yk].values
                
                # Filter valid
                mask = (vals_x > 200) & (vals_x < 4000) & (vals_y > 200) & (vals_y < 4000)
                all_x.extend(vals_x[mask])
                all_y.extend(vals_y[mask])
        
        # Plot Heatmap
        # Zoom in on House/Guard Zone
        view_x = [CENTER_X - 1000, CENTER_X + 1000]
        view_y = [CENTER_Y - 1000, CENTER_Y + 1500] # More Y to see guards?
        
        h = ax.hist2d(all_x, all_y, bins=50, cmap='Reds', range=[view_x, view_y])
        ax.set_title(f"Stone Positions after Shot 1: {outcome} ({len(subset)} ends)")
        ax.invert_yaxis()
        
        # Draw House
        radii = [6, 4, 2]
        for r in radii:
            c = plt.Circle((CENTER_X, CENTER_Y), r*SCALE, fill=False, color='blue')
            ax.add_patch(c)
            
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "shot_selection_analysis.png")
    plt.savefig(out_path)
    print(f"Saved analysis to {out_path}")

if __name__ == "__main__":
    analyze_shot_selection()
