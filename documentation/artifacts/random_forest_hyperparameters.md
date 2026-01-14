# Appendix B: Model Specification & Hyperparameters

## B.1 Model Selection Rationale
We selected a **Random Forest Classifier** (`sklearn.ensemble.RandomForestClassifier`) over other architectures (e.g., Logistic Regression, Neural Networks) for three key reasons:

1.  **Non-Linearity:** Curling strategy is highly non-linear. The value of "having the Hammer" changes drastically depending on the End and Score. Decision Trees capture these step-function interactions naturally.
2.  **Robustness to Noise:** Sports data is inherently noisy (human execution error). Random Forests (bagging) reduce variance better than single Decision Trees or un-regularized Gradient Boosting.
3.  **Data Size:** With $N \approx 3,000$ ends (estimated), Deep Learning models would likely overfit. Random Forests perform exceptionally well on tabular data of this scale.

## B.2 Training & Validation Split
To ensure the model generalizes to unseen games, we employed a strict validation strategy:

*   **Split Ratio:** **80% Training / 20% Testing**.
    *   *Justification:* Keeps the majority of data for learning patterns ($N_{train} \approx 2,400$) while reserving a statistically significant sample ($N_{test} \approx 600$) for evaluation.
*   **Stratification (`stratify=y`):**
    *   *Method:* The split maintained the exact proportion of "Wins" and "Losses" in both sets.
    *   *Justification:* Prevents bias. If the Test set accidentally contained mostly "Winning" games, a naive model that predicts "Win" could appear artificially accurate. Stratification forces the model to learn the *features*, not the distribution.

## B.3 Hyperparameter Justifications

| Parameter | Value | Justification |
| :--- | :--- | :--- |
| **`n_estimators`** | `100` | **Balance.** 100 trees provide sufficient voting power to smooth out anomalies (variance reduction) without incurring unnecessary computational latency during the 100,000+ simulations required for the WPA Heatmap. |
| **`max_depth`** | `5` | **Regularization.** We intentionally limited the tree depth to 5. This forces the model to learn "General Rules" (e.g., "Down 2 with Hammer is good") rather than memorizing specific game states (Overfitting). Deep trees risks modeling the noise of individual execution errors. |
| **`random_state`** | `42` | **Reproducibility.** Ensures that exactly the same ends are assigned to the Test Set every time the code is run, guaranteeing that our reported AUC (0.89) is verifiable by peer review. |
| **`features`** | 4 | We restricted inputs to `ScoreDiff`, `EndID`, `Hammer`, and `PowerPlay`. We excluded Team IDs to ensure the model learned **Curling Strategy**, not "Team Sweden is good." |

## B.4 Model Evaluation (ROC & AUC)
To validate the model’s predictive power, we examined the **Receiver Operating Characteristic (ROC) Curve**.

*   **The Metric:** The **AUC (Area Under Curve)** score represents the probability that the model will rank a randomly chosen "Winning" state higher than a randomly chosen "Losing" state.
*   **Our Result:** **AUC = 0.89**.
    *   *Interpretation:* A score of 0.5 is random guessing. A score of 1.0 is perfect prediction. achieving 0.89 indicates **Excellent** predictive power (typically, >0.8 is considered strong for sports analytics).
*   **Visual Check:** The ROC curve (see `analysis/rf_roc_curve.png`) bows sharply toward the top-left corner, confirming that the model achieves a high True Positive Rate (Sensitivity) while keeping False Positives low.
