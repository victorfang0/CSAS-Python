# Step 5: Visualization & Mapping
*Or: "Drawing a map when you only have GPS coordinates."*

Finally, we looked at the stone locations. The user wanted to see "The Dots."
We opened the file `Stones.csv` and found a list of numbers like `x=765`, `y=2000`.
To a human, these numbers are meaningless. We had to draw a map.

## 1. Statistical Forensics
We didn't know where the "House" (the target) was. The data didn't tell us. So we used detective work.
*   We assumed that in professional curling, players are good (usually).
*   Therefore, most stones should land near the target.
*   We plotted **150,000 stones** on a graph (a Heatmap).

**The Result:**
We saw a massive, glowing red dot of stones clustered at one specific point: **(765, 740)**.
*   That *must* be the Button (the center).

## 2. Finding the Scale
We knew the digital center. But how big is a "foot"?
*   We measured the spread of the stones.
*   We know a real Curling House is **12 feet wide** (6 foot radius).
*   In our data, the stone cluster faded away about **600 pixels** from the center.
*   **Math:** $$ 600 \text{ pixels} \div 6 \text{ feet} = 100 \text{ pixels per foot} $$.

## 3. Drawing the Diagram
Once we had the Center (765, 740) and the Scale (100px = 1ft), we could draw the rings ourselves.
*   We told python: *"Draw a blue circle at radius 600"*. (12ft Ring)
*   *"Draw a white circle at radius 400"*. (8ft Ring)
*   *"Draw a red circle at radius 200"*. (4ft Ring)

When we overlaid the actual data on top of our drawing, it lined up perfectly. This confirms our math was right.

## 4. Why this matters
Now that we have this map, we can answer the tactical questions.
*   *"When practicing Power Plays, do we place the guard stone at x=500 or x=600?"*
*   Before, those were just numbers. Now, we know exactly where that is on the ice.
*   We can analyze if **Corner Guards** (protecting the side) are better than **Center Guards** (protecting the button) during a Power Play.

And that, class, is how you use Data Science to solve Curling.
