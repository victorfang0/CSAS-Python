# Step 1: Thought Process & Strategy

## 1. Initial Intuition: "Comparative Gain"
You started with a key question: *"When is the best time to use the Power Play?"*
Your intuition led you to the concept of **Comparative Gain**: Not just measuring raw points, but measuring the *relative advantage* gained by using the PP compared to a normal end.

### The "High School" vs "Graduate" Pivot
*   **Level 1 (Basic):** Calculate average points.
    *   *Flaw:* Scoring 2 points when down 8-0 is mathematically "good" (positive points), but strategically useless (you still lose 99.9% of the time).
*   **Level 2 (Graduate):** **Win Probability Added (WPA)**.
    *   *Concept:* We measure success by "Did this action increase my probability of winning the championship/match?"
    *   *Formal Definition:*
        $$ WPA = P(\text{Win} | \text{Use PP}) - P(\text{Win} | \text{Don't Use PP}) $$

## 2. Defining the Metrics
To calculate WPA, we needed to define the **Game State**. In Curling (Mixed Doubles), the state is defined by three variables:
1.  **Score Differential ($S$):** (My Score - Opponent Score). Range: -infinity to +infinity.
2.  **End Number ($E$):** The time remaining. Range: 1-8.
3.  **Hammer ($H$):** Who has the last rock advantage? (0 or 1).

## 3. The Hypothesis
Our hypothesis was that the Power Play is a **high-variance catch-up mechanic**.
*   It moves rocks to the side, creating an "open" game.
*   Open games favor scoring (both for you and the opponent).
*   Therefore, it should be used when **trailing** (to create volatility) and avoided when **leading** (to minimize volatility).

## 4. Operationalizing the Plan
We broke the study into three technical phases:
1.  **Ingestion:** Getting the messy CSVs into a structured "State Table".
2.  **Modeling:** Training an AI to predict "Win %" from any state.
3.  **Simulation:** Using the AI to play out "What If" scenarios for every possible game situation.
