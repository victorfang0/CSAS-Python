# CSAS 2026 Data Challenge - Code Submission
## Overview
This folder contains the Python scripts used to generate the models and visualizations for the report "To Make a Difference, Comparative Gain, and Power Play Optimization".
## Dependencies
- Python 3.x
- pandas, numpy, scikit-learn, matplotlib, seaborn
## File Descriptions
1. **train_model.py**: Loads the cleaned data, trains the Random Forest classifier used for Win Probability Added (WPA) calculation, and saves the model (.pkl).
2. **visualize_wpa_strategy.py**: Generates the Strategy Heatmap (Figure 3 & 10 in the report) showing optimal Power Play usage.
3. **visualize_execution_contours.py**: Generates the KDE Contour plots (Figure 13) analyzing stone placement.
4. **visualize_rf.py**: Generates model diagnostics, feature importance bar charts, and the ROC Curve (Figures 4 & 5).
## Data Availability
This code relies on the standard competition data (`Ends.csv`, `Games.csv`, `Stones.csv`) provided by CSAS/Curlit. Per submission guidelines, these files are not included here. To run the code, place these CSVs in the root directory relative to the scripts.
