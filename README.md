# CSAS 2026 Data Challenge: Mixed Doubles Curling

## Project Overview
This repository contains the code, data, and analysis for the **CSAS 2026 Data Challenge**.
**Topic:** Mixed Doubles Curling Power Play Optimization.
**Goal:** To determine the optimal strategic usage of the "Power Play" mechanic using Win Probability Added (WPA) modeling.

## Directory Structure

### 1. Documentation (`/documentation`)
*   **Papers:** Contains the detailed narrative explaining the methodology and results.
    *   `papers/00_FULL_DRAFT_REPORT.md`: The compiled manuscript.
    *   `papers/06_shot_selection_and_execution.md`: Analysis of rock placement.
    *   `papers/04_strategic_analysis_wpa.md`: The Strategy Heatmap analysis.
*   **Artifacts:** generated figures and processed data, each with a `.md` descriptor explaining its content.
    *   `optimal_strategy_heatmap.png`: The primary result (When to use Power Play).
    *   `shot_selection_analysis.png`: The analysis of guard execution.
    *   `modeling_data.csv`: The feature-engineered dataset.

### 2. Source Code (`/src`)
*   **Data Pipeline:**
    *   `feature_engineering.py`: Merges raw `Ends.csv` and `Games.csv`, resolves ID conflicts, and calculates `ScoreDiff`.
*   **Modeling:**
    *   `train_model.py`: Trains the Random Forest Classifier (AUC 0.89) to predict `Won_Game`.
*   **Analysis:**
    *   `optimal_strategy.py`: Simulates game states to generate the Strategy Heatmap.
    *   `analyze_rock_location.py`: analyzes stone coordinates to test the "Magic Spot" hypothesis.
    *   `visualize_sheet.py`: Reverse-engineers the curling sheet coordinate system.

## How to Reproduce Results

### Prerequisites
*   Python 3.8+
*   Required Libraries: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`

### Steps
1.  **Install Dependencies:**
    ```bash
    pip install pandas numpy scikit-learn matplotlib seaborn
    ```
2.  **Run the Pipeline:**
    *   **Step 1 (Data):** `python3 src/feature_engineering.py`
        *   *Output:* `analysis/modeling_data.csv`
    *   **Step 2 (Model):** `python3 src/train_model.py`
        *   *Output:* `models/wp_rf.pkl` and `analysis/modeling_data_with_probs.csv`
    *   **Step 3 (Strategy):** `python3 src/optimal_strategy.py`
        *   *Output:* `analysis/optimal_strategy_heatmap.png`
    *   **Step 4 (Tactics):** `python3 src/analyze_rock_location.py`
        *   *Output:* `analysis/shot_selection_analysis.png`

## Authors
*   *Anonymized for CSAS Submission*
