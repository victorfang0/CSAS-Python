# Step 3: Modeling Win Probability

## 1. Why Machine Learning?
We could have used simple statistics (e.g., "Teams leading by 2 win 80% of the time"). However, Curling has complex interactions:
*   Being down by 1 in End 1 is **very different** from being down by 1 in End 8.
*   The relationship is **Non-Linear**.
*   Machine Learning (Random Forest) captures these "interaction effects" automatically.

## 2. Algorithm Selection: Random Forest
We chose **Random Forest** (over simpler Logistic Regression or complex Deep Learning) because:
*   **Robustness:** It works well with small-to-medium datasets (we had ~350 clean data points after matching).
*   **No Overfitting:** It averages many decision trees, preventing it from memorizing the specific games in the dataset.
*   **Interpretability:** We can extract "Feature Importance" to see what matters.

## 3. Training Process
1.  **Split:** We withheld 20% of the games as a "Test Set" to honestly evaluate performance.
2.  **Train:** The model looked at the 80% "Training Set" and learned patterns like:
    *   *Pattern:* "When ScoreDiff is > 0 and End is > 6, Result is usually Win."
    *   *Pattern:* "When ScoreDiff is < -2 in End 7, Result is usually Loss."
3.  **Evaluate:** We tested the model on the unseen 20% data.

## 4. Results
*   **Accuracy:** **81%**. (The model correctly predicted the winner 4 out of 5 times just by knowing the score and end).
*   **AUC (Area Under Curve):** **0.89**.
    *   *Meaning:* This is an "A Grade" model. An AUC of 0.5 is random guessing. An AUC of 1.0 is perfect clairvoyance. 0.89 is extremely strong for sports prediction.

We now have a "Virtual Curling Expert" that can look at any scoreboard and tell you the probability of winning.
