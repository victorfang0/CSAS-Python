# Artifact: Optimal Strategy Heatmap

**File:** `optimal_strategy_heatmap.png`
**Type:** Analysis Result (PNG)

## What this is
The "Answer Key" for the Power Play decision. It visualizes the **Win Probability Added (WPA)** for using a Power Play in every possible game state.

## How we built it
1.  **Model:** Trained a Random Forest Classifier (AUC 0.89) to predict Win % from Score, End, and Hammer.
2.  **Simulation:** For every cell in the grid (e.g., End 6, Score -2), we simulated two futures:
    *   Future A: With Power Play.
    *   Future B: Without Power Play.
3.  **Calculation:** Cell Value = $P(Win | PP) - P(Win | Normal)$.

## How to interpret it
*   **Y-Axis (Score Diff):** Positive means you are Winning. Negative means you are Losing.
*   **X-Axis (End):** The stage of the game (1-7).
*   **Blue Cells (Positive):** **USE THE POWER PLAY.** It increases your chance of winning.
    *   *Key Insight:* The best time is Ends 5-7 when trailing by 2-4 points (+26% gain).
*   **Red Cells (Negative):** **DO NOT USE IT.** It hurts your chance of winning.
    *   *Key Insight:* Never use it when leading. It introduces unnecessary risk.
