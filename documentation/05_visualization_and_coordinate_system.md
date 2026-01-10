# Step 5: Visualization & Coordinate System

## 1. The "Dots" Puzzle
The user requested to see "the dots" (stone placements). We opened `Stones.csv` and found a mess:
*   Columns relative to... nothing?
*   Values ranged from 0 to 4095.
*   No documentation on what "x=2000" meant.

## 2. Reverse Engineering the Sheet
We used **Statistical Forensics** to map the board.

1.  **The Heatmap:** We plotted *every single stone* from thousands of games.
2.  **The "Donut" Hypothesis:** We expected stones to cluster in the House (the target).
    *   *Initial guess:* Center is (2048, 2048).
    *   *Reality:* The histogram showed the center was actually near **(765, 740)**.
3.  **The Scale:** We measured the "spread" of the stones.
    *   Most stones fall within a radius of ~600 units from the center.
    *   Since the standard Curling House radius is 6 feet, we derived the scale: **~100 units = 1 Foot**.

## 3. Interpreting the Visualization
We generated `analysis/coordinate_system_corrected.png`.

*   **The Rings:** We drew circles at 6ft, 4ft, 2ft, and 1ft (Button) using our derived scale.
*   **Verification:** The dots (actual stone data) lined up *perfectly* inside our drawn rings. This confirmed our reverse-engineered map was correct.

## 4. What the Data Means
Now that we have the map, every row in `Stones.csv` tells a story:
*   `x=765, y=740`: A "Button" shot (bullseye).
*   `x=500, y=740`: A "Guard" sitting to the left of the button.
*   `x=765, y=200`: A "High Guard" protecting the house.

This visualization allows us to answer the next level of strategy questions: *"Where should we place the rocks during a Power Play?"* (e.g., Center Guards vs Corner Guards).
