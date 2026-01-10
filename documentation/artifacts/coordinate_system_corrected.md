# Artifact: Coordinate System Map

**File:** `coordinate_system_corrected.png`
**Type:** Visualization (PNG)

## What this is
This chart maps the reverse-engineered coordinate system of the raw data to the physical reality of the Curling Sheet.

## How we built it
1.  We plotted the density of 150,000+ stone locations from `Stones.csv`.
2.  We identified the high-density cluster at **(765, 740)** as the "Button" (Center).
3.  We observed the distribution radius and calculated the scale factor: **100 pixels = 1 Foot**.
4.  We overlaid the official World Curling Federation ring sizes (12ft, 8ft, 4ft) to verify the fit.

## How to interpret it
*   **X-Axis:** Width of the sheet (0-1500 px). Center line is at X=765.
*   **Y-Axis:** Length of the sheet. Tee Line is at Y=740.
*   **White/Red/Blue Rings:** Represent the House. Stones inside these rings score points.
*   **Use Case:** This map is the "Rosetta Stone" that allows us to translate raw data integers into meaningful Curling strategy.
