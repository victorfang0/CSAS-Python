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
Most students would answer this by looking at **Average Points**.
They would say: *"Well, teams score 2.5 points with the Power Play and 1.5 points without it. So, use it immediately!"*

**Here is why that is wrong.**
Imagine you are winning 8-0 in the last end. 
*   Does scoring 2 more points (10-0) help you? **No.** You were already going to win.
*   Does the Power Play risk letting the opponent score? **Yes.**
*   In this case, "more points" is actually **bad strategy** because it introduces risk.

### The Graduate Concept: "Comparative Gain"
We don't care about points. We care about **Winning**.
We introduced a metric called **WPA (Win Probability Added)**.
We ask:
1.  What is my % chance to win if I play safe? (e.g., 80%).
2.  What is my % chance to win if I use the Power Play? (e.g., 75%).

If the number goes *down*, the Power Play was a bad idea, even if you scored points!
**Our Strategy:** We will build an AI model to calculate this "Win %" for every single moment in a game.
