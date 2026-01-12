# Comparative Gain: A Win Probability Approach to Power Play Optimization in Mixed Doubles Curling

**Abstract**
In Mixed Doubles Curling, the Power Play is a high-variance strategic option available once per game. This paper leverages a Random Forest classifier (AUC 0.89) to model Win Probability ($P_{win}$) as a function of game state. We introduce a metric, **Win Probability Added (WPA)**, to quantify the strategic value of the Power Play. Our analysis reveals that the Power Play is a catch-up mechanic best deployed in Ends 5-7 when trailing by 2-4 points (WPA +26%). Conversely, we demonstrate that using the Power Play while leading yields negative WPA due to increased variance. Finally, we investigate "Shot Selection" strategy and find a null result ($\Delta x < 1$ inch) between winning and losing guard placements, suggesting that execution, rather than novel positioning, is the primary driver of end outcomes.

---

## 1. Introduction
Mixed Doubles Curling introduces a "Power Play" mechanic that fundamentally alters the board state by moving pre-placed stones to the wing. Coaches and skips face a critical decision: *When is the optimal moment to invoke this advantage?*

### 1.1 Preliminary Analysis (The Naive Approach)
Initial linear regression modeling (`lm(Result ~ PowerPlay)`) of the dataset suggested a significant advantage, with a coefficient of **+0.71 points** per end ($p < 2e^{-16}$). While statistically valid, this "Expected Points" ($E[P]$) approach is strategically flawed.

In late-game scenarios, minimizing variance is often more valuable than maximizing score. We propose a transition to **Win Probability Added (WPA)** as the gold standard for decision making.

## 2. Methodology

### 2.1 Global Assumptions with Justifications
To model the complex environment of Mixed Doubles Curling, we made the following strategic assumptions:
*   **Assumption 1: Rational Actors.** We assume teams attempt to maximize their win probability at all times.
    *   *Justification:* While human error exists, modeling "mistakes" is impossible without psychological data. We assume optimal intent.
*   **Assumption 2: Continuity of Skill.** We assume a team's ability to execute a shot is constant throughout the game (no fatigue/momentum).
    *   *Justification:* Statistical analysis of "Hot Hand" phenomena in sports often suggests momentum is illusory. Treating skill as constant reduces noise.
*   **Assumption 3: Independence of Ends.** We assume the outcome of End $N$ depends only on the state variables (Score, Hammer) and not on the history of End $N-1$.
    *   *Justification:* This Markov Assumption allows us to simulate millions of game states efficiently without needing full game histories.

### 2.2 Table of Definitions
To ensure clarity, we define the following variables used in our model:

| Symbol | Variable | Definition | Unit |
| :--- | :--- | :--- | :--- |
| $P_{win}$ | Win Probability | The likelihood (0-1) that a team wins the match. | Probability |
| $WPA$ | Win Probability Added | The change in $P_{win}$ caused by a specific decision. | Percentage |
| $\vec{x}$ | State Vector | The tensor representing the game state: $\{Score, End, Hammer\}$. | Vector |
| $\lambda$ | Scale Factor | The ratio of pixels in the dataset to real-world feet. | px/ft |
| $\mu$ | Centroid | The geometric center of a cluster of stones. | $(x,y)$ coord |

### 2.2 Data Engineering
The raw dataset consisted of two disparate CSV files: `Games.csv` (metadata) and `Ends.csv` (play-by-play). We implemented a rigorous cleaning pipeline to prepare this data for modeling:
1.  **Composite Keys:** We discovered ID collisions where `GameID: 1` referred to multiple matches across different events. We resolved this by generating a unique primary key: `CompetitionID_GameID_EndID`.
2.  **Feature Engineering:**
    *   **Hammer Logic:** We algorithmically tracked possession of the "Last Rock" advantage, flipping the binary indicator `Hammer` only when a team scored $>0$ points.
    *   **Score Differential:** We computed `ScoreDiff = OwnScore - OpponentScore` to quantify game pressure.
    *   **Handling Sentinel Values:** Coordinate error codes (e.g., `x=4095`) were filtered out before centroid analysis.

### 2.3 Model Selection & Justification
We selected a **Random Forest Classifier** ($N_{trees}=100$, Max Depth=5) to approximate the Win Probability function:

$$
f(\vec{x}) = P(Win_{Match} | \vec{x}_{End})
$$

where $\vec{x}$ is the state vector $\{ScoreDiff, EndID, Hammer, PowerPlay\}$.

**Why Random Forest?**
1.  **Non-Linear Interactions:** The strategic value of game state variables is highly conditional. For example, possession of the Hammer (last rock) is critical in End 8 (worth ~100% win probability if tied) but less decisive in End 1. Similarly, a +1 lead is valuable in low-scoring defensive games but precarious in high-scoring shootouts. Methods like **Logistic Regression** assume linear relationships and fail to capture these "cliff-edge" interaction effects without manual feature engineering.
2.  **Robustness to Overfitting:** By averaging the predictions of 100 independent decision trees, the Random Forest minimizes the variance inherent in small datasets ($N \approx 5000$ ends).
3.  **Rejection of Alternatives:**
    *   **Logistic Regression:** Rejected due to its inability to model complex decision boundaries (e.g., the specific non-linear value of the Power Play at End 6 vs End 7) without extensive transformation.
    *   **Deep Neural Networks:** Rejected as "overkill". Given the tabular nature and limited size of the dataset, deep learning models are prone to overfitting and lack the interpretability required for a strategy paper.
    *   **XGBoost:** Considered, but Random Forest was preferred for its simpler hyperparameter tuning and lower risk of overfitting on this specific sample size.

## 3. Strategic Analysis (The "When")

### 3.1 The Twin Earths Simulation
To measure the value of the Power Play, we simulated two scenarios for every possible game state:
$$
WPA = f(\vec{x}_{PP}) - f(\vec{x}_{Normal})
$$

### 3.2 Results
*   **The Catch-Up Rule:** When trailing by 2-4 points in Ends 5-7, the Power Play maximizes WPA (+26%). The "open board" increases scoring variance, which is favorable for the trailing team.
*   **The Leading Penalty:** When leading, the Power Play often results in negative WPA. Leading teams benefit from low-variance "cluttered" centers; the Power Play removes this clutter.

### 3.3 Sensitivity Analysis
To test the robustness of our "Catch-Up Rule" (End 6, Score -2), we performed a bootstrap analysis with $N=20$ iterations on 80% subsamples of the data.
*   **Stability:** The model recommended "Use Power Play" in **90%** of iterations (18/20).
*   **Variance:** The mean WPA was $+0.148$ with a standard deviation of $\sigma=0.07$.
*   **Conclusion:** While the strategic advantage is statistically significant, the non-zero variance confirms that the Power Play remains a high-risk/high-reward calculated gamble, not a guaranteed win.

## 4. Execution Analysis (The "How")

### 4.1 The Magic Spot Hypothesis
We investigated whether specific placements of the Corner Guard correlated with higher points. We compared the coordinates of the first thrown stone in "Big Win" ends ($Points \ge 3$) versus "Stolen" ends ($Points \le 0$).

### 4.2 Findings
*   **Big Wins:** Mean Guard X = 796.9.
*   **Losses:** Mean Guard X = 803.2.
*   **Difference:** $\Delta \approx 0.7$ inches.

### 4.3 Sensitivity Analysis
We tested the "Null Result" by varying the definition of a "Win" from $\ge 2$ points to $\ge 5$ points.
*   **Threshold $\ge 2$:** $\Delta x = 0.85$ inches.
*   **Threshold $\ge 3$:** $\Delta x = 0.75$ inches.
*   **Threshold $\ge 4$:** $\Delta x = 0.86$ inches.
*   **Conclusion:** The finding is robust. Regardless of the scoring threshold, winning and losing guard placements are indistinguishable to within 1 inch.

### 4.4 Conclusion
We observed no statistically significant difference in stone placement. This suggests a state of **Strategic Equilibrium**.

### 4.4 Strengths & Weaknesses
**Strengths:**
*   **Robust Metric:** $WPA$ is superior to "Average Points" for strategic decision making.
*   **Large Sample Size:** Our "Null Result" on shot selection is based on 598 ends, giving it high statistical power.

**Weaknesses:**
*   **No "Rock Interaction" Model:** Our Win Probability model predicts based on Score/End, but does not "see" the board state (e.g., number of guards).
*   **Skill Homogeneity:** We treat all teams as "Average." A model that accounted for individual Team Skill (e.g., Bruce Mowat vs Italy) would be more precise.

## 5. Conclusion
Our system provides a solved framework for the Power Play:
1.  **Strategy:** Use the WPA Heatmap to decide *when* to call it (Late game, Catch-up).
2.  **Tactics:** Do not deviate from standard guard placement; focus on execution consistency.

This approach moves Mixed Doubles analysis from "Average Points" to "Championship Probability".
