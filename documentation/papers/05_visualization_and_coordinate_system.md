# Step 5: Visualization & Mapping
*Or: "Drawing a map when you only have GPS coordinates."*

Finally, we looked at the stone locations. The user wanted to see "The Dots."
We opened the file `Stones.csv` and found a list of coordinates $(x_i, y_i)$.
To a human, these numbers are meaningless. We had to draw a map.

## 1. Statistical Forensics
We didn't know where the "House" (the target) was. The data didn't tell us. So we used detective work.
We modeled the stone locations as a 2D density function:
$$
D(x, y) = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}(x_i, y_i)
$$

**The Result:**
We observed the centroid $(\mu_x, \mu_y)$ of the cluster density:
$$
\mu_x \approx 765, \quad \mu_y \approx 740
$$
This point represents the **Button** (the center of the rings).

## 2. Finding the Scale ($\lambda$)
We needed to determine the conversion factor $\lambda$ (pixels per foot).
*   We measured the variance of the stone cluster distribution.
*   We observed that the cluster density drops to near-zero at a radius $r_{pixel} \approx 600$.
*   We know the standard World Curling Federation House radius is $r_{real} = 6$ feet.
$$
\lambda = \frac{r_{pixel}}{r_{real}} = \frac{600 \text{ px}}{6 \text{ ft}} = 100 \text{ px/ft}
$$

## 3. Drawing the Diagram
Once we had the Center $C(765, 740)$ and the Scale $\lambda = 100$, we could define the House geometrically.
We drew circles for the standard rings:
*   **12-Foot Ring:** $R_{12} = 6 \text{ ft} \times 100 = 600 \text{ px}$
*   **8-Foot Ring:** $R_{8} = 4 \text{ ft} \times 100 = 400 \text{ px}$
*   **4-Foot Ring:** $R_{4} = 2 \text{ ft} \times 100 = 200 \text{ px}$
*   **Button:** $R_{1} = 0.5 \text{ ft} \times 100 = 50 \text{ px}$

When we overlaid the actual data on top of our drawing, it lined up perfectly. This confirms our linear transformation model was correct.

## 4. Why this matters
Now that we have this map, we can answer the tactical questions.
*   *"Where is the optimal guard placement coordinate $(x_g, y_g)$?"*
*   We can analyzing the spatial distribution of winning vs losing guards to find the optimal coordinate vector:
$$
\vec{v}_{opt} = \text{argmax}_{\vec{v}} P(Win | \vec{v})
$$
    
And that, class, is how you use Data Science to solve Curling.
