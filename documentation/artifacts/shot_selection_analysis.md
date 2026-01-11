# Artifact: Shot Selection Analysis

**File:** `shot_selection_analysis.png`
**Type:** Strategic Analysis (PNG)

## What this is
A visualization testing the "Magic Spot" hypothesis. It compares the winning guard placements against losing guard placements.

## The "Magic Spot" Hypothesis
We hypothesized that **Win Probability is a function of Stone Coordinates**. 
*   *Theory:* If you place the guard at exactly $(x, y)$, your chance of winning increases significantly.
*   *Expectation:* We expected to see a "Winning Cluster" of stones at specific coordinates that differed from the "Losing Cluster".

## How we built it
1.  **Filtering:** We isolated Power Play ends.
2.  **Grouping:** We split them into "Big Wins" (Scored 3+ points) and "Losses" (Stolen/0 points).
3.  **Plotting:** We plotted the location of the *first thrown stone* (the Guard) for both groups.

## How to interpret it
*   **Left Panel (Big Win):** Where winners placed their guards.
    *   *Centroid:* X=796, Y=1221.
*   **Right Panel (Loss):** Where losers placed their guards.
    *   *Centroid:* X=803, Y=1214.
*   **The Findings:** The heatmaps look identical.
    *   Big Wins Centroid: $X = 796.9$
    *   Losses Centroid: $X = 803.2$
    *   **Difference:** $6.3$ pixels ($< 1$ inch).
*   **Evidence of Falsification:**
    *   If the "Magic Spot" existed, the difference $\Delta x$ would be significant (e.g., $> 1$ foot).
    *   Since $\Delta x \approx 0$, we reject the hypothesis. There is no winning coordinate.
*   **Conclusion:** There is no "Magic Spot." Winning comes from executing the shot at the standard location, not from finding a secret coordinate.
