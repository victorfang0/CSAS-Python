
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches
import numpy as np

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_DIR = "/Users/victor/Desktop/CSAS/analysis/"

def visualize_system():
    # Calculated Parameters based on histogram drop-off at 600 units
    # 600 units ~= 6 feet (House Radius)
    # Scale ~= 100 units/foot
    CENTER_X = 765
    CENTER_Y = 740
    SCALE = 100 # pixels per foot
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    print("Loading Stones...")
    stones = pd.read_csv(os.path.join(DATA_DIR, "Stones.csv"))
    
    all_x = []
    all_y = []
    sample = stones.sample(n=min(len(stones), 50000), random_state=42)
    
    # Vectorized masking to correct shape mismatch
    # Iterate columns pairs
    for i in range(1, 13):
        xk = f'stone_{i}_x'
        yk = f'stone_{i}_y'
        if xk in sample.columns and yk in sample.columns:
            # Drop rows where EITHER is NaN in this pair
            pair_data = sample[[xk, yk]].dropna()
            
            xs = pair_data[xk].values
            ys = pair_data[yk].values
            
            # Mask error codes
            mask = (xs > 200) & (xs < 4000) & (ys > 200) & (ys < 4000)
            
            all_x.extend(xs[mask])
            all_y.extend(ys[mask])
            
    print(f"Plotting {len(all_x)} points...")
    
    # 1. Plot Heatmap (Zoomed in around Center)
    # Range: Center +/- 10 feet (1000 units)
    view_range_x = [CENTER_X - 1000, CENTER_X + 1000]
    view_range_y = [CENTER_Y - 1000, CENTER_Y + 1000]
    
    ax.hist2d(all_x, all_y, bins=100, cmap='Greys', range=[view_range_x, view_range_y], alpha=0.3)
    
    # 2. Draw House Rings
    # Radii in feet: 12ft diam = 6ft radius
    radii_ft = [6, 4, 2, 0.5] 
    colors = ['blue', 'white', 'red', 'white'] # Outer to Inner
    
    for r, color in zip(radii_ft, colors):
        circle = patches.Circle((CENTER_X, CENTER_Y), r * SCALE, 
                                facecolor=color, edgecolor='black', alpha=0.3, linewidth=2, label=f'{r*2}ft Ring')
        ax.add_patch(circle)
        
    # 3. Annotations
    ax.plot(CENTER_X, CENTER_Y, 'x', color='black', markersize=15, markeredgewidth=3, label='Center (Tee)')
    
    # Center Line
    ax.axvline(x=CENTER_X, color='black', linestyle='--', alpha=0.5, label='Center Line')
    # Tee Line
    ax.axhline(y=CENTER_Y, color='black', linestyle='--', alpha=0.5, label='Tee Line')
    
    # Text Annotations
    ax.text(CENTER_X + 650, CENTER_Y, "12 Foot Ring Edge", fontsize=10, verticalalignment='center')
    
    ax.set_xlim(view_range_x)
    ax.set_ylim(view_range_y)
    ax.set_title(f"Corrected Coordinate System\nOrigin: ({CENTER_X}, {CENTER_Y}) | Scale: 100 units = 1 foot", fontsize=14)
    ax.invert_yaxis() # Match standard image coords
    
    ax.legend(loc='upper right')
    
    out_path = os.path.join(OUTPUT_DIR, "coordinate_system_corrected.png")
    plt.savefig(out_path)
    print(f"Saved annotated plot to {out_path}")

if __name__ == "__main__":
    visualize_system()
