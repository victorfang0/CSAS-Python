# Appendix D: File Structure & Key Scripts

To ensure reproducibility, the following file structure and key scripts are provided in the attached code repository.

## D.1 Directory Structure
*   **`DATA/`**: Contains the raw input files (`Stones.csv`, `Ends.csv`, `Games.csv`).
*   **`models/`**: Stores the trained Random Forest model (`wp_rf.pkl`) for reuse.
*   **`analysis/`**: Output directory for all generated plots and statistical tables.
*   **`src/`**: Source code for all modeling and visualization pipelines.

## D.2 Key Scripts (`src/`)

### Modeling
*   **`RF_modeltraining/train_model.py`**:
    *   *Purpose:* Loads cleaned data, trains the Random Forest classifier (Win Probability Model), and saves the `.pkl` file.
    *   *Key Logic:* Implements the 80/20 Stratified Split and Hyperparameters described in Appendix B.

### Strategic Analysis
*   **`visualize_wpa_strategy.py`**:
    *   *Purpose:* Generates the **Strategy Heatmap** (Appendix A).
    *   *Key Logic:* Runs the "Twin Earths" simulation, calculating the WPA for every possible game state.

### Execution Analysis
*   **`analyze_magic_spot.py`**:
    *   *Purpose:* Performs the detailed "Magic Spot" analysis (Appendix C).
    *   *Key Logic:* Calculates Centroid Euclidean distances and generates the Delta Bar Chart and Scatter Plots.
*   **`visualize_execution_contours.py`**:
    *   *Purpose:* Generates the KDE Contour plots.
    *   *Key Logic:* Overlays the density of Winning vs. Losing guard placements to visually demonstrate the Null Result.

### Diagnostics
*   **`visualize_rf.py`**:
    *   *Purpose:* Generates Model Diagnostics (Appendix B).
    *   *Key Logic:* Produces the Feature Importance Bar Chart and ROC Curve to validate model performance.
