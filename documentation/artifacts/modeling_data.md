# Artifact: Modeling Data (Processed)

**File:** `modeling_data.csv` & `modeling_data_with_probs.csv`
**Type:** Dataset (CSV)

## What this is
The cleaned, feature-engineered dataset used to train the Random Forest model.

### What is a Random Forest?
Think of it as a **"Committee of Experts"**.
*   A single **Decision Tree** is like one expert: It learns simple rules (e.g., "If Score < -2, then Loss"). However, single trees often "overfit" (they memorize the specific game instead of learning the general rule).
*   A **Random Forest** trains 100 different trees. Each tree sees a slightly different version of the data (random subset).
*   To make a prediction, the forest asks all 100 trees to vote. The majority vote wins.
*   **Why is this better?** It reduces variance. If one tree makes a mistake because of a weird data point, the other 99 trees correct it. This makes the model **Robust**.

### Model Parameters (Our Configuration)
We used the following specific settings in `src/train_model.py`:

*   **`n_estimators=100`** (Number of Trees):
    *   We trained 100 separate decision trees.
    *   *Why?* 100 is a standard "Goldilocks" number—enough to get a stable average, but not so many that it becomes slow.

*   **`max_depth=5`** (Tree Height):
    *   Each tree is only allowed to ask 5 questions (e.g., Q1: Score? Q2: Hammer? Q3: End?...).
    *   *Why?* Deep trees (Depth 20+) memorize noise. Shallow trees (Depth 5) learn **General Strategy**. This prevents overfitting.

*   **`random_state=42`** (Reproducibility):
    *   This ensures that if you run the code again, you get the exact same result. Science must be reproducible.

*   **Features Used (The Inputs):**
    1.  `ScoreDiff`: The current lead/deficit.
    2.  `EndID`: How much time is left.
    3.  `Hammer`: Who has the last shot advantage.
    4.  `PowerPlay_Active`: Is the board open (PP) or closed (Normal)?:

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
