
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths
DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"

def visualize_shot_selection_contours():
    print("Loading Data...")
    ends_df = pd.read_csv(os.path.join(DATA_DIR, "Ends.csv"))
    stones_df = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    
    # 1. Prepare Data
    # Filter for Power Play Ends
    pp_ends = ends_df[ends_df['PowerPlay'].notna() & (ends_df['PowerPlay'] != 0)].copy()
    
    # Merge Result into Stones based on ID
    # Stones has columns: CompetitionID, SessionID, GameID, EndID, ShotID, Stone_1_x, Stone_1_y, etc.
    # We want the FIRST shot of the end (Shot 1).
    stones_sorted = stones_df.sort_values(by=['CompetitionID', 'GameID', 'EndID', 'ShotID'])
    first_shots = stones_sorted.groupby(['CompetitionID', 'GameID', 'EndID']).first().reset_index()
    
    join_cols = ['CompetitionID', 'GameID', 'EndID']
    merged = pd.merge(first_shots, pp_ends, on=join_cols, how='inner')
    
    # Label "Success" vs "Failure"
    # Success = Scored 2+ points (Big End)
    # Failure = Stolen (Score <= 0)
    merged['Outcome'] = merged['Result'].apply(lambda x: 'Big Win (2+)' if x >= 2 else ('Loss (Steal)' if x <= 0 else 'Neutral'))
    
    # Filter out Neutral
    subset = merged[merged['Outcome'].isin(['Big Win (2+)', 'Loss (Steal)'])]
    
    # Extract Coordinates of the GUARD
    # Assuming Stone_1 is the guard position.
    # Note: Coordinates range 0-4096.
    
    data = []
    
    print("Extracting Coordinates...")
    for idx, row in subset.iterrows():
        # Clean coords (remove sentinel values)
        # Case sensitive!
        x = row['stone_1_x']
        y = row['stone_1_y']
        
        # Valid range?
        if 200 < x < 4000 and 200 < y < 4000:
            data.append({'x': x, 'y': y, 'Outcome': row['Outcome']})
            
    df_plot = pd.DataFrame(data)
    
    # 3. PLOT (Style Match: Scatter + KDE Contours)
    plt.figure(figsize=(10, 10))
    
    # We want to zoom in on the Guard Zone.
    # Center X ~ 765. Guard Y ~ 1200?
    
    # Scatter Points (alpha low to show density)
    # Viridis Palette Colors
    # Purple (#440154) for Steals (Low Value)
    # Teal/Green (#21918c) for Big Wins (High Value)
    
    # Scatter Points
    sns.scatterplot(
        data=df_plot, 
        x='x', y='y', 
        hue='Outcome', 
        style='Outcome',
        palette={'Big Win (2+)': '#21918c', 'Loss (Steal)': '#440154'},
        alpha=0.3,
        s=30
    )
    
    # KDE Contours
    # Win = Teal
    sns.kdeplot(
        data=df_plot[df_plot['Outcome']=='Big Win (2+)'], 
        x='x', y='y', 
        color='#21918c', 
        levels=5, 
        thresh=0.2,
        alpha=0.7
    )
    
    # Loss = Purple
    sns.kdeplot(
        data=df_plot[df_plot['Outcome']=='Loss (Steal)'], 
        x='x', y='y', 
        color='#440154', 
        levels=5, 
        thresh=0.2,
        alpha=0.7,
        linestyles='--'
    )

    # Draw House for Refernce
    CENTER_X, CENTER_Y = 765, 740 # Approx Button
    SCALE = 100
    house_circle = plt.Circle((CENTER_X, CENTER_Y), 6*SCALE, fill=False, color='blue', linewidth=2, label='House')
    plt.gca().add_patch(house_circle)
    
    plt.title("Execution Analysis: Guard Placement (Big Wins vs Steals)\n(Overlapping Contours Prove the Null Result)")
    plt.xlabel("Sheet Width (Pixels)")
    plt.ylabel("Sheet Length (Pixels)")
    plt.legend()
    plt.gca().invert_yaxis() # Curling sheet top-down
    plt.axis('equal')
    
    # Zoom to relevant area
    plt.xlim(0, 1600)
    plt.ylim(0, 2000)
    
    out_path = os.path.join(OUTPUT_DIR, "execution_contours.png")
    plt.savefig(out_path)
    print(f"Saved Execution Contour Plot to {out_path}")

if __name__ == "__main__":
    visualize_shot_selection_contours()
