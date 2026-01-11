# Random Forest Model Configuration

## 1. Model Architecture
We utilized the `scikit-learn` implementation of the **Random Forest Classifier**.

### Hyperparameters
| Parameter | Value | Justification |
| :--- | :--- | :--- |
| **`n_estimators`** | `100` | A committee of 100 trees provides a stable probability estimate ($\sigma < 0.05$) without excessive computational cost. |
| **`max_depth`** | `5` | Constraining depth is critical to prevent overfitting on our small dataset ($N \approx 5000$). It forces the model to learn general strategic rules (e.g., "ScoreDiff is good") rather than memorizing specific game instances. |
| **`random_state`** | `42` | Ensures reproducibility of the results and the 80/20 train-test split. |
| **`bootstrap`** | `True` | (Default) Each tree is trained on a random subset of the data with replacement, increasing model diversity. |

---

## 2. Training Process

### Data Split
*   **Training Set:** 80%
*   **Test Set:** 20%
*   **Stratification:** Yes (Preserves the win/loss ratio in both sets).

### Input Features ($\vec{x}$)
The model consumes a 4-dimensional state vector:
1.  **`ScoreDiff`** (Integer): The scoring margin (Our Score - Opponent Score).
2.  **`EndID`** (Integer): The current end number (1-8).
3.  **`Hammer`** (Binary): 1 if we have the Last Rock advantage, 0 otherwise.
4.  **`PowerPlay_Active`** (Binary): 1 if the Power Play is currently active.

### Target Variable ($y$)
*   **`Won_Game`** (Binary): 1 if the team eventually won the match, 0 otherwise.

---

## 3. Performance Metrics
*   **AUC (Area Under Curve):** **0.89** (Indicates excellent discriminatory power).
*   **Interpretability:** High. Feature importance analysis confirms `ScoreDiff` is the dominant predictor, followed by `EndID` and `Hammer` interaction.
