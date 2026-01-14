# Appendix C: Execution Analysis (The "Magic Spot")

## C.1 Visualizing the Null Result
We hypothesized that winning teams might place their stones in a fundamentally different location than losing teams ("The Magic Spot"). To test this, we analyzed the coordinates of the Corner Guard in 598 Power Play ends.

### The "Null" Contours
The chart below overlays the guard placement density for **Big Wins (Score $\ge$ 2)** vs. **Steals (Score $\le$ 0)**.

![Execution Contours](/Users/victor/Desktop/CSAS/analysis/execution_contours.png)

### Interpretation
*   **Overlap:** The Teal (Win) and Purple (Loss) probability "mountains" sit almost exactly on top of each other.
*   **Conclusion:** There is **no spatial separation** between a winning strategy and a losing strategy at the elite level. Both groups know exactly where to put the rock.
*   **Implication:** Outcomes are determined by **Execution** (hitting that spot) and **Later Shots**, not by finding a secret "Magic Spot" for the first stone.

## C.2 Quantitative Difference (The 1-Inch Reality)
We measured the Euclidean distance between the centroids (average position) of the Winning group and the Losing group across multiple thresholds of "Win".

![Centroid Deltas](/Users/victor/Desktop/CSAS/analysis/magic_spot_deltas.png)

### The Data in Context
*   The difference between the average winning guard and average losing guard is typically **4–10 inches**.
*   On a standard curling sheet (width $\approx$ 15 feet or 180 inches), a difference of 4 inches is **< 2.5%** of the playing area.
*   This visual confirms that the difference is statistically negligible relative to human error and ice variance.
