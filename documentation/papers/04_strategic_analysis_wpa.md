# Step 4: The Strategic Analysis
*Or: "Simulating Parallel Universes."*

We have our Virtual Expert (the Random Forest model, which approximates $f(\vec{x})$). Now we play a game called **"Twin Earths"**.

## 1. The Simulation
We want to know: *Is the Power Play good?*
To answer this, we take a specific situation—let's say **End 6, Score -2**. We assume we have the Hammer ($H=1$).

We ask our model to predict the future in two different universes:

1.  **Universe A (Power Play):** We set the feature vector $\vec{x}_{pp} = \{E=6, S=-2, H=1, PP=1\}$.
$$
P_{win}^{pp} = f(\vec{x}_{pp}) \approx 0.45
$$
    *(We have a 45% chance to win)*.

2.  **Universe B (Normal):** We set the feature vector $\vec{x}_{norm} = \{E=6, S=-2, H=1, PP=0\}$.
$$
P_{win}^{norm} = f(\vec{x}_{norm}) \approx 0.35
$$
    *(We have a 35% chance to win)*.

## 2. Calculating the Gain
We simply subtract the two probabilities to find the marginal utility:
$$
\Delta P = P_{win}^{pp} - P_{win}^{norm}
$$

$$
\Delta P = 0.45 - 0.35 = +0.10
$$

In this scenario, using the Power Play increases our chance of winning by **10%**. That is huge. That is worth doing.

## 3. The Heatmap (The Answer Key)
We ran this "Twin Earths" simulation for all $S \in [-4, +4]$ and $E \in [1, 8]$.
The result is the Heatmap you saw. Here is how to read it:

### The "Catch-Up" Rule ($S < 0$)
*   Look at **Ends 5, 6, and 7**.
*   Look at the rows where the team is **Trailing**.
*   **Theorem:** Power Play increases Variance ($\sigma^2_{score}$).
    *   When $S < 0$, you need high variance to overcome the deficit.
    *   Therefore, $\Delta P > 0$ (Positive WPA).

### The "Don't Throw It Away" Rule ($S > 0$)
*   Look at the rows where the team is **Leading**.
*   **Theorem:** When $S > 0$, your goal is to minimize variance ($\text{min } \sigma^2_{score}$).
    *   Power Play increases variance.
    *   Therefore, $\Delta P < 0$ (Negative WPA).
    *   **Lesson:** Never use a Risk-Creation tool when you are winning.

## 4. Opportunity Cost ($C_{opp}$)
A student asked: *"Sir, the model says End 1 gives a +0.5% gain. Should I use it?"*
**No.**
*   You only get **ONE** Power Play per game.
*   Let $G_t$ be the max possible gain in End $t$.
*   You should only use the Power Play at time $t$ if the current gain $g_t$ is greater than the expected future gain $E[G_{future}]$.
$$
\text{Use PP if } g_t > E[\text{max}(g_{t+1}, ..., g_8)]
$$
*   We concluded that saving the PP for a potential End 6 "Emergency" (worth +26%) is statistically better than burning it for a +0.5% gain in End 1.
