
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Force non-interactive backend
import matplotlib.pyplot as plt
import os
import numpy as np

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"

def visualize():
    print("Loading Stones.csv...")
    stones = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    
    # Filter out potential nulls
    stones = stones.dropna(subset=['stone_1_x']) # Check first stone at least
    
    # 1. Global Heatmap to find the House
    # We'll stick all x and y coordinates into one big bucket
    x_cols = [c for c in stones.columns if c.endswith('_x')]
    y_cols = [c for c in stones.columns if c.endswith('_y')]
    
    all_x = []
    all_y = []
    
    # Sample first 5000 rows to save time if needed, or do all
    sample = stones.sample(n=min(len(stones), 10000), random_state=42)
    
    for i in range(1, 17): # Stones 1-16 (columns are stone_1_x to stone_16_x? Wait, let's check cols)
        # Deep Dive showed stone_1_x up to stone_12_x (Mixed doubles has fewer stones?)
        # 5 stones per team? 6?
        # Column list from preview: stone_1_x ... stone_12_x
        xk = f'stone_{i}_x'
        yk = f'stone_{i}_y'
        if xk in stones.columns:
            all_x.extend(sample[xk].dropna().values)
            all_y.extend(sample[yk].dropna().values)
            
    print(f"Plotting {len(all_x)} stone positions...")
    
    plt.figure(figsize=(10, 10))
    plt.hist2d(all_x, all_y, bins=100, cmap='Blues', range=[[0, 4095], [0, 4095]])
    plt.colorbar(label='Stone Density')
    plt.title("Aggregate Stone Locations (0-4095 Coordinate Space)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    
    # Invert Y if needed (monitor standard coords usually top-left 0,0)
    plt.gca().invert_yaxis()
    
    heatmap_path = os.path.join(OUTPUT_DIR, "stone_density_heatmap.png")
    plt.savefig(heatmap_path)
    print(f"Saved Heatmap to {heatmap_path}")
    plt.close()
    
    # 2. Plot a Specific Power Play End
    # Let's find an end with PowerPlay = 1 (or True)
    # We need to link back to match Ends? Or just find one in Stones (does it have PP flag?)
    # Stones.csv does NOT have PP flag based on my preview (Columns: GameID, EndID, ShotID...)
    # We need to merge or just get a GameID/EndID from the previous analysis step.
    
    # Let's manually pick a Game/End that we know used PP from modeling_data.csv
    try:
        model_df = pd.read_csv(os.path.join(OUTPUT_DIR, "modeling_data.csv"))
        pp_ends = model_df[model_df['PowerPlay_Active'] == True]
        
        if not pp_ends.empty:
            sample_end = pp_ends.iloc[0]
            gid = int(sample_end['GameID'])
            eid = int(sample_end['EndID'])
            comp_id = int(sample_end['CompetitionID'])
            
            print(f"Visualizing Power Play End: Comp {comp_id}, Game {gid}, End {eid}")
            
            # Get stones for this end
            # Stones.csv has one row per SHOT. We want the FINAL state of the end?
            # Or does it have coordinates for every shot?
            # "stone_1_x" ... "stone_12_x". This looks like a snapshot of ALL stones?
            # If so, per shot?
            
            end_shots = stones[
                (stones['CompetitionID'] == comp_id) & 
                (stones['GameID'] == gid) & 
                (stones['EndID'] == eid)
            ]
            
            # The last shot of the end should show the final state
            final_state = end_shots.sort_values('ShotID').iloc[-1]
            
            plt.figure(figsize=(8, 8))
            
            # Draw Rings (Approximation based on 0-4095 range, CENTER assumed 2048, 2048 for now)
            # We will refine this after seeing the heatmap
            center_x, center_y = 2048, 2048
            
            # Plot stones
            xs = []
            ys = []
            colors = []
            
            for i in range(1, 13): # 12 stones max usually
                xk = f'stone_{i}_x'
                yk = f'stone_{i}_y'
                if xk in final_state and pd.notna(final_state[xk]):
                    x_val = final_state[xk]
                    y_val = final_state[yk]
                    xs.append(x_val)
                    ys.append(y_val)
                    # Color? We don't verify owner yet, just 'red' for dots
                    colors.append('red')

            plt.scatter(xs, ys, c=colors, s=200, edgecolors='black')
            plt.xlim(0, 4095)
            plt.ylim(0, 4095)
            plt.gca().set_aspect('equal')
            plt.gca().invert_yaxis()
            plt.title(f"State after Last Shot (Comp {comp_id}, Game {gid}, End {eid})")
            
            sample_path = os.path.join(OUTPUT_DIR, "sample_pp_end.png")
            plt.savefig(sample_path)
            print(f"Saved Sample Plot to {sample_path}")
            
    except Exception as e:
        print(f"Could not plot specific end: {e}")

if __name__ == "__main__":
    visualize()
