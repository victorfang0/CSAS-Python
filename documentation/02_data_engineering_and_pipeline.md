# Step 2: Data Engineering
*Or: "Why real-world data is always broken, and how we fixed it."*

Alright, we have our strategy. Now we need data. We downloaded two files: `Ends.csv` (the scoreboard) and `Games.csv` (the teams).
I opened them up, and immediately, I found a disaster.

## 1. The "John Smith" Problem (ID Collisions)
Imagine if our school database listed students only by "First Name".
If I searched for "John", I’d get John from 9th grade, John from 10th grade, and John the janitor. I wouldn't know who is who.

**This happened in our data.**
*   The file listed `GameID: 1`. 
*   But "Game 1" happened in the Olympics. And "Game 1" happened in the World Cup. And "Game 1" happened in the National Qualifiers.
*   When we merged them, the computer thought they were all the same game! It was mixing up Olympic scores with High School scores.

### The Fix: Composite Keys
We had to create a "Full Name" for each game.
Instead of looking for `GameID`, we told the computer to group by **Two Columns**: `CompetitionID` + `GameID`.
*   *Before:* "Game 1" (Ambiguous).
*   *After:* "Competition 5, Game 1" (Unique).
**Lesson:** Always check your identifiers. Unique IDs are rarely unique in the real world.

## 2. Translating "Curling" to "Spreadsheet"
Understanding the game isn't enough; we have to explain it to a computer using numbers. This is called **Feature Engineering**.

*   **The Hammer (Last Rock):** 
    *   *Concept:* The team that throws the last rock has a huge advantage. They usually score.
    *   *The Rule:* If you score in an end, you give the Hammer to the other team. If you score 0, you keep it.
    *   *The Code:* We wrote a loop that tracked who scored. If Team A scored > 0, we flipped the value `Hammer_Team` to Team B.
*   **Score Differential:**
    *   *Concept:* Are we winning or losing?
    *   *The Code:* We simply calculated `My_Total_Score - Opponent_Total_Score`.
    *   *Why:* Being down by 2 is very different from being down by 20. The model needs to know the pressure.

We saved this clean, translated data into `modeling_data.csv`. Now, the computer is ready to learn.
