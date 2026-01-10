# Step 4: Strategic Analysis (WPA & Heatmap)

## 1. The Strategy Engine
We have a model that predicts winning. Now we use it to calculate strategy.

**The Method: "The Twin Earth Simulation"**
For every possible situation (e.g., End 6, Score -2), we asked the model two questions:
1.  **Earth A:** "What is the win probability if we use the **Power Play** right now?" ($P_{PP}$)
2.  **Earth B:** "What is the win probability if we use a **Normal End** right now?" ($P_{Normal}$)

## 2. Calculating Comparative Gain
We subtracted the two probabilities:
$$ Gain = P_{PP} - P_{Normal} $$

*   **Positive Gain:** The Power Play improved our chances.
*   **Negative Gain:** The Power Play hurt our chances.

## 3. The Results (The Heatmap)
We visualized thousands of these simulations in the `analysis/optimal_strategy_heatmap.png`.

### Key Findings Explained:
*   **The Golden Zone (End 6, Score -2 to -4):**
    *   *Why?* You are running out of time (End 6/8). You need a mult-point end to catch up. The Power Play forces rocks to the wings, creating a "messy" board that allows for big scores (3 or 4 points).
    *   *Result:* Gain of +26.89%. This is massive. It turns a "Likely Loss" into a "Toss Up".

*   **The Danger Zone (Leading by > 0):**
    *   *Why?* When you are winning, your goal is **Variance Reduction**. You want boring ends. You want to peel rocks and keep the middle open.
    *   *Result:* Using the Power Play (which creates messiness) actually **reduces** your win probability. You are taking unnecessary risks.

## 4. Opportunity Cost
This is the final piece of the puzzle.
*   "Why not use it in End 1 if the Gain is +1%?"
*   **Answer:** Because you represent a *Limited Resource*. You only get ONE Power Play per game.
*   We concluded that you should **save** the Power Play until the Gain exceeds a "Threshold" (e.g., > 10%). End 1 gains are too small to justify burning the card. The "Option Value" of holding it for a future End 6 emergency is far higher.
