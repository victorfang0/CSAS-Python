# Step 1: The Strategy & Thought Process
*Or: "How we decided what to solve, and why."*

Hello class. Before we write a single line of code, we have to talk about **Curling**.

## 1. The Context: What is "Mixed Doubles" Curling?
Imagine Chess, but played on ice with 40-pound granite rocks. 
In traditional Curling, you have 4 players. In **Mixed Doubles**, you only have 2 (one male, one female). Because there are fewer players, the game is faster, more aggressive, and higher scoring.

### The Key Mechanic: The Power Play
Usually, stones are placed in the center to start an end. It's safe. It's standard.
But once per game, each team can call a **Power Play**.
*   **What it does:** It moves the starting stones to the *side* (the "wings").
*   **Why it matters:** This creates an "Open Board." It’s like taking the pawns off the chessboard. It invites chaos. It allows for big scores, but also big mistakes.

## 2. Our Research Question
The coach (the user) came to me with a question:
> *"Sir, when is the exact right time to play this Wildcard? Do I use it early to get ahead? Or save it for a rainy day?"*

## 3. The "High School" Approach vs. The "Graduate" Approach
Most students would answer this by looking at **Expected Points ($E[P]$)**.
They would define the value of the Power Play ($V_{pp}$) as:
$$
V_{pp} = E[Points | PowerPlay] - E[Points | Normal]
$$

**Here is why that is wrong.**
Imagine you are winning 8-0 in the last end ($S = +8, E = 8$).
*   Does scoring 2 more points (10-0) help you? **No.** You were already going to win ($P(Win) \approx 1.0$).
*   Does the Power Play risk letting the opponent score? **Yes.**
*   In this case, maximizing $E[Points]$ is actually **bad strategy** because it introduces variance ($\sigma^2$) that you don't need.

### The Graduate Concept: "Win Probability Added" (WPA)
We don't care about points ($P$). We care about Winning ($W$).
We introduced a metric called **WPA**.
We define the Game State vector $\vec{x}$ as:
$$
\vec{x} = \{ \text{ScoreDiff}, \text{EndNumber}, \text{Hammer} \}
$$

The Win Probability function $f(\vec{x})$ gives us the probability of winning given state $\vec{x}$.
$$
P(Win) = f(\vec{x})
$$

Therefore, the value of the Power Play is the **Comparative Gain**:
$$
WPA(\vec{x}) = P(Win | \vec{x}, PowerPlay=1) - P(Win | \vec{x}, PowerPlay=0)
$$

**Our Strategy:** We will build an AI model to estimate the function $f(\vec{x})$ for every possible game state.
