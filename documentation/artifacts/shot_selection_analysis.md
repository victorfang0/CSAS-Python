# Artifact: Shot Selection Analysis

**File:** `shot_selection_analysis.png`
**Type:** Strategic Analysis (PNG)

## What this is
A visualization testing the "Magic Spot" hypothesis. It compares the winning guard placements against losing guard placements.

## How we built it
1.  **Filtering:** We isolated Power Play ends.
2.  **Grouping:** We split them into "Big Wins" (Scored 3+ points) and "Losses" (Stolen/0 points).
3.  **Plotting:** We plotted the location of the *first thrown stone* (the Guard) for both groups.

## How to interpret it
*   **Left Panel (Big Win):** Where winners placed their guards.
    *   *Centroid:* X=796, Y=1221.
*   **Right Panel (Loss):** Where losers placed their guards.
    *   *Centroid:* X=803, Y=1214.
*   **The Findings:** The heatmaps look identical. The numeric difference is < 1 inch.
*   **Conclusion:** There is no "Magic Spot." Winning comes from executing the shot at the standard location, not from finding a secret coordinate.
