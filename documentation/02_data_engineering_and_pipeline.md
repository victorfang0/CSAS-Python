# Step 2: Data Engineering & Pipeline

## 1. The Raw Data
We started with two files:
*   `Ends.csv`: Contains the results of every end (scores).
*   `Games.csv`: Contains metadata about the teams and match IDs.

## 2. The Critical Bug: ID Collisions
During the first pass, we found a major issue.
*   **Observation:** There were thousands of rows in `Ends.csv`, but when we grouped by `GameID`, we only saw ~5 unique games.
*   **Root Cause:** The `GameID` (e.g., "1") was reused across different Competitions. "Game 1" existed in the Olympics, and "Game 1" existed in the World Championship.
*   **The Fix:** We implemented a **Composite Key**. We grouped data by `['CompetitionID', 'GameID']`. This unique combination correctly separated the matches, recovering thousands of data points.

## 3. Feature Engineering logic
We wrote a script (`src/feature_engineering.py`) to transform the raw logs into a "Teaching Dataset" for our AI model.

### Key Features Created:
*   `ScoreDiff`: We calculated the running score *before* the end started.
    *   *Logic:* `CumlativeScore_TeamA - CumulativeScore_TeamB`.
*   `Hammer`: The rule is "Loser of the previous end gets the Hammer".
    *   *Logic:* We implemented a state tracker that flips the hammer token after every end.
*   `Won_Game`: The target variable.
    *   *Logic:* We summed the total points for the game and checked if `FinalPoints_Team > FinalPoints_Opp`.

## 4. The Output
The pipeline produced `analysis/modeling_data.csv`, a clean table where every row represents *one decision point* in a game:
*   Input: "End 6, Down by 2, Have Hammer".
*   Action: "Used Power Play".
*   Result: "Won Game (True/False)".
