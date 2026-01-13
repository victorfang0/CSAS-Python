# Appendix A: Strategy Heatmap

## A.1 The Strategic Landscape (Win Probability Added)
The following heatmap visualizes the **Win Probability Added (WPA)** of invoking the Power Play in every possible game state. This is derived from our "Twin Earths" simulation, comparing the probability of winning with the Power Play vs. the standard game.

![Strategy Heatmap](/Users/victor/Desktop/CSAS/analysis/wpa_strategy_heatmap.png)

## A.2 How to Interpret This Map (Coach’s Guide)

This chart is designed to be a quick-reference "Cheat Sheet" for coaches and skips during a match.

### 1. The Color Code
*   **🔵 Blue / Teal (Positive WPA):** **USE THE POWER PLAY.**
    *   The Power Play increases your chance of winning in these situations.
    *   *Mnemonic:* "Blue Skies Ahead" (Good for you).
*   **🟣 Purple (Negative WPA):** **AVOID THE POWER PLAY.**
    *   Invoking the Power Play here actually *lowers* your chance of winning (usually because it gives the opponent a clean setup to steal or force).
    *   *Mnemonic:* "Purple Haze" (Danger).
*   **⚪️ White / Gray (Neutral):** **Indifferent.**
    *   The strategic choice has minimal impact (< 1% change). Reliance on team strength execution is preferred.

### 2. The Axes
*   **Y-Axis (Score Differential):** The difference in score **relative to your team**.
    *   Positive (+1, +2) means you are **Leading**.
    *   Negative (-1, -2) means you are **Trailing**.
*   **X-Axis (End Number):** The current End you are about to start (with the Hammer).

### 3. Key Strategic Rules
Based on the model's output, we have derived three "Golden Rules" for the Mixed Doubles Power Play:

1.  **The "Catch-Up" Rule (Trailing by 2+):**
    *   **Situation:** You are down by 2 or more points in Ends 4–7.
    *   **Action:** **AGGRESSIVE USE.** You will see deep Teal/Green blocks here. The Power Play opens up the center, allowing for high-scoring "Big Ends" (3+ points) necessary to close the gap.

2.  **The "Leading Penalty" (Up by 1 or 2):**
    *   **Situation:** You are leading by 1 or 2 points late in the game (End 6-7).
    *   **Action:** **DO NOT USE.** You will see Purple blocks here. Using the Power Play when leading exposes you to a "Steal" risk. A standard defensive house (center blocked) is statistically safer to protect a lead.

3.  **The "Use It or Lose It" (End 8):**
    *   **Situation:** It is the final end (End 8).
    *   **Action:** **ALWAYS USE (if you have it).** There is no future value to saving the Power Play. Unless the game is already mathematically tied/won, the model consistently shows a slight edge or neutral value, but never a penalty, for using it in the last end to control the playing area.
