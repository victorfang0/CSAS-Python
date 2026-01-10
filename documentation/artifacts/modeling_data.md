# Artifact: Modeling Data (Processed)

**File:** `modeling_data.csv` & `modeling_data_with_probs.csv`
**Type:** Dataset (CSV)

## What this is
The clean, feature-engineered dataset used to train the Random Forest model.

## How we built it
1.  **Source:** Merged `Ends.csv` and `Games.csv` using Composite Keys (`CompetitionID` + `GameID`).
2.  **Features Added:**
    *   `ScoreDiff`: Calculated running total score before the end.
    *   `Hammer`: Tracked possession based on previous end scoring.
    *   `Won_Game`: The target variable (1/0).
3.  **Refinement:** `modeling_data_with_probs.csv` includes the model's *predictions* (`WinProb`) derived in Step 3.

## How to interpret it
*   **Rows:** Each row is one "End" of a Curling match.
*   **Columns:**
    *   `PowerPlay_Active`: 1 if used, 0 if not.
    *   `WinProb`: The estimated chance (0.00-1.00) that the team eventually won the game from that position.
*   **Usage:** This is the "Ground Truth" table that powers all our strategy simulations.
