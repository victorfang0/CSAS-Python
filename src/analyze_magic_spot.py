
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths and Constants
DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"
PIXELS_PER_FOOT = 100
PIXELS_PER_INCH = PIXELS_PER_FOOT / 12.0

def analyze_magic_spot():
    print("Loading Data...")
    try:
        ends_df = pd.read_csv(os.path.join(DATA_DIR, "Ends.csv"))
        stones_df = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    except FileNotFoundError:
        print("Data not found.")
        return

    # 1. Prepare Data
    # Filter for Power Play Ends
    pp_ends = ends_df[ends_df['PowerPlay'].notna() & (ends_df['PowerPlay'] != 0)].copy()
    
    # Get First Shot (Guard)
    # Using lowercase stone_1_x/y as discovered earlier
    # Note: Stones.csv is Long format or Wide?
    # Checked earlier: It has stone_1_x ... stone_12_y.
    # But wait, earlier `visualize_execution_contours.py` failed on `Stone_1_x` then merged with `stones_sorted`?
    # Let's re-verify the "Merge" logic. 
    # In `visualize_execution_contours.py` I used `stones_df` which I thought was Long, but the `head` output showed `stone_1_x`.
    # Ah, the `head` output showed `stone_1_x` columns. 
    # BUT `Stones.csv` rows are shots?
    # Yes: `ShotID` 1..16.
    # So `stone_1_x` in row `ShotID=1` is the position of Stone 1 AFTER Shot 1?
    # Or is it the throw?
    # Usually "Stone Placement" implies where it ended up.
    # For "First Shot of the Power Play", it's the Corner Guard.
    # We want the position of the stone thrown in Shot 1.
    # In `Stones.csv` snapshot format, valid columns for Shot 1 are `stone_1_x`.
    # So for ShotID=1, we want `stone_1_x`.
    
    # Filter for the FIRST shot of each end (Guard)
    # ShotIDs are inconsistent (e.g. start at 7), so we take the minimum ShotID per end.
    idx = stones_df.groupby(['CompetitionID', 'GameID', 'EndID'])['ShotID'].idxmin()
    first_shots = stones_df.loc[idx].copy()
    
    # Coordinates of Stone 1
    first_shots['GuardX'] = first_shots['stone_1_x']
    first_shots['GuardY'] = first_shots['stone_1_y']
    
    # Join with Ends to get Result
    join_cols = ['CompetitionID', 'GameID', 'EndID']
    merged = pd.merge(first_shots, pp_ends, on=join_cols, how='inner')
    
    # 2. Analyze Thresholds
    thresholds = [2, 3, 4, 5]
    results_table = []
    
    print("\n--- Magic Spot Analysis (Distance between Winners and Losers) ---")
    
    for T in thresholds:
        # Define Groups
        # Win: Score >= T
        # Loss: Score <= 0 (Steal)
        winners = merged[merged['Result'] >= T]
        losers = merged[merged['Result'] <= 0]
        
        # Calculate Centroids
        if len(winners) > 0:
            w_x, w_y = winners['GuardX'].mean(), winners['GuardY'].mean()
        else:
            w_x, w_y = 0, 0
            
        if len(losers) > 0:
            l_x, l_y = losers['GuardX'].mean(), losers['GuardY'].mean()
        else:
            l_x, l_y = 0, 0
        
        # Euclidean Distance
        dist_px = np.sqrt((w_x - l_x)**2 + (w_y - l_y)**2)
        dist_in = dist_px / PIXELS_PER_INCH
        
        row = {
            "Threshold": f"Result >= {T}",
            "N_Wins": len(winners),
            "N_Losses": len(losers),
            "Win_Centroid": f"({w_x:.1f}, {w_y:.1f})",
            "Loss_Centroid": f"({l_x:.1f}, {l_y:.1f})",
            "Delta_Pixels": dist_px,
            "Delta_Inches": dist_in
        }
        results_table.append(row)
        print(f"Threshold {T}+: Delta = {dist_in:.2f} inches (N={len(winners)} vs {len(losers)})")
        
    # Save Table (Manual Markdown to avoid 'tabulate' dependency)
    lines = []
    lines.append("| Threshold | N_Wins | N_Losses | Win_Centroid | Loss_Centroid | Delta_Pixels | Delta_Inches |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in results_table:
        lines.append(f"| {row['Threshold']} | {row['N_Wins']} | {row['N_Losses']} | {row['Win_Centroid']} | {row['Loss_Centroid']} | {row['Delta_Pixels']:.2f} | {row['Delta_Inches']:.2f} |")
    
    md_table = "\n".join(lines)
    
    with open(os.path.join(OUTPUT_DIR, "magic_spot_stats.md"), "w") as f:
        f.write("# Magic Spot Analysis: Centroid Deltas\n\n")
        f.write(md_table)
        
    # 3. Visualization 1: Delta Bar Chart
    df_results = pd.DataFrame(results_table) # Fix NameError
    plt.figure(figsize=(8, 6))
    bars = sns.barplot(data=df_results, x='Threshold', y='Delta_Inches', palette="viridis")
    
    # Add 1-inch reference line
    plt.axhline(y=1.0, color='red', linestyle='--', label='1 Inch (Minimal Effect)')
    
    plt.title("Difference in Guard Placement (Winners vs Losers)\n(Evidence of Null Result)")
    plt.ylabel("Distance Between Centers (Inches)")
    plt.xlabel("Definition of 'Win'")
    plt.legend()
    
    for container in bars.containers:
        bars.bar_label(container, fmt='%.2f"')
        
    out_path_bar = os.path.join(OUTPUT_DIR, "magic_spot_deltas.png")
    plt.savefig(out_path_bar)
    print(f"Saved Bar Chart to {out_path_bar}")


    # 4. Visualization 2: Scatter Plot (Outcome >= 2 vs Steal)
    # Using T=2 as the representative case
    T = 2
    subset = merged[ (merged['Result'] >= T) | (merged['Result'] <= 0) ].copy()
    subset['Outcome'] = subset['Result'].apply(lambda x: f'Win ({T}+)' if x >= T else 'Loss (Steal)')
    
    plt.figure(figsize=(10, 10))
    
    # KDE "Glow" Effect (Underlay)
    sns.kdeplot(
        data=subset,
        x='GuardX', y='GuardY',
        hue='Outcome',
        palette={f'Win ({T}+)': '#21918c', 'Loss (Steal)': '#440154'},
        fill=True,
        alpha=0.3,
        levels=5,
        thresh=0.05,
        legend=False
    )

    # Scatter (Teal vs Purple)
    sns.scatterplot(
        data=subset, 
        x='GuardX', y='GuardY', 
        hue='Outcome', 
        style='Outcome',
        palette={f'Win ({T}+)': '#21918c', 'Loss (Steal)': '#440154'},
        alpha=0.6, # Slightly more opaque
        s=40,
        linewidth=0.5,
        edgecolor='white'
    )
    
    # Plot Centroids
    # Recalculate for T=2 specifically for plotting
    w_data = subset[subset['Result'] >= T]
    l_data = subset[subset['Result'] <= 0]
    
    plt.scatter(w_data['GuardX'].mean(), w_data['GuardY'].mean(), color='white', s=200, marker='X', edgecolors='black', label='Win Centroid', zorder=10)
    plt.scatter(l_data['GuardX'].mean(), l_data['GuardY'].mean(), color='yellow', s=200, marker='X', edgecolors='black', label='Loss Centroid', zorder=10)
    
    # Draw House (765, 740)
    house = plt.Circle((765, 740), 600, fill=False, color='gray', linestyle=':', label='House Area')
    plt.gca().add_patch(house)
    
    plt.title(f"Guard Placement Scatter (Wins vs Steals)\nCentroids marked with 'X'")
    plt.gca().invert_yaxis()
    plt.axis('equal')
    
    # Zoom in on Guard Zone (Left side usually? Or Center?)
    # Corner guard is usually side. Center guard is center. 
    # Let's let it auto-scale but maybe focus if dense.
    
    out_path_scatter = os.path.join(OUTPUT_DIR, "magic_spot_scatter_detailed.png")
    plt.savefig(out_path_scatter)
    print(f"Saved Scatter Plot to {out_path_scatter}")

if __name__ == "__main__":
    analyze_magic_spot()
