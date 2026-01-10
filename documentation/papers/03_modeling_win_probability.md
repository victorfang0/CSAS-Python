# Step 3: The AI Model
*Or: "Teaching a computer to predict the future."*

We have our clean data. Now, we want to answer the big question: **"If I am down by 2 in End 6, will I win?"**

## 1. Why we can't just use an Average
You might ask, *"Professor, why not just search the database for all games where a team was down by 2 in End 6 and count how many won?"*

That's a great question. The problem is **Sample Size**.
*   We might only have 3 examples of that *exact* situation.
*   Maybe in one of them, the team had the best player in the world.
*   In another, the ice melted.
*   3 examples isn't enough to trust.

## 2. Enter "The Random Forest"
Instead of memorizing history, we train an AI to learn **patterns**. We chose an algorithm called the **Random Forest**.

### How it works (The Committee)
Imagine I give this problem to 100 students (the "Trees").
*   **Student 1** looks mostly at the Score: *"He's losing, so he'll probably lose."*
*   **Student 2** looks at the Hammer: *"But he has the Hammer, so he might comeback."*
*   **Student 3** looks at the End Number: *"It's only End 2, there's plenty of time."*

The "Random Forest" takes the vote of all 100 students.
*   If 89 students say "Win", the model gives an **89% Win Probability**.
*   This "wisdom of the crowd" creates a much more accurate prediction than any single rule.

## 3. Our Results
We graded the model (using a "Test Set" it had never seen before).
*   **It got an "A" (AUC 0.89).**
*   This means if you give it two games, one where the team won and one where they lost, it can correctly identify the winner **89% of the time** just by looking at the scoreboard.

Now that we have a "Virtual Expert" that knows success rates, we can use it to test our Power Play strategy.
