# CSAS 2026 Data Challenge: Mixed Doubles Curling

## Project Overview
**Topic:** Mixed Doubles Curling Power Play Optimization.
**Goal:** To determine the optimal strategic usage of the "Power Play" mechanic using Win Probability Added (WPA) modeling.
**Method:** This project utilizes a Random Forest classifier (AUC 0.89) to estimate win probability from game state features and simulates outcomes to derive a Comparative Gain metric.

---

## ⚠️ Data Privacy & Setup
**Per CSAS rules, the raw challenge data is not included in this repository as the organizers already possess it.**

### Comparison
To run this code, you must place the official challenge CSV files into a local directory named `data/`.

**Required File Structure:**
```
/ (Root)
├── data/
│   ├── Ends.csv
│   ├── Games.csv
│   └── Stones.csv
├── src/
├── documentation/
├── requirements.txt
└── README.md
```

**External Data:**
No external public datasets were used in this analysis. All findings are derived strictly from the provided competition data.

---

## 🛠 Reproducibility Instructions

### 1. Requirements
Install the necessary Python libraries:
```bash
pip install -r requirements.txt
```
*Validated on Python 3.9+ with pandas 2.0+*

### 2. Execution Order
Run the following scripts in the specified order to reproduce the analysis pipeline:

1.  **Data Cleaning & Feature Engineering:**
    ```bash
    python3 src/pipeline/feature_engineering.py
    ```
    *Output:* Generates `modeling_data.csv` (Merged game states with calculated Score Differentials).

2.  **Model Training:**
    ```bash
    python3 src/modeling/train_model.py
    ```
    *Output:* Trains the Random Forest model, saves it to `models/`, and produces `modeling_data_with_probs.csv`.

3.  **Strategy Analysis (The "When"):**
    ```bash
    python3 src/analysis/core/optimal_strategy.py
    ```
    *Output:* Generates `analysis/optimal_strategy_heatmap.png` (The WPA Decision Matrix).

4.  **Tactic Analysis (The "How"):**
    ```bash
    python3 src/analysis/core/analyze_rock_location_stats.py
    ```
    *Output:* Prints statistical comparison of winning vs. losing stone coordinates to console.

---

## 📂 File Dictionary

### 1. Pipeline (`src/pipeline/`)
*   `feature_engineering.py`: Merges raw `Ends.csv` and `Games.csv` using composite keys and calculates the running Score Differential.
*   `eda_preview.py` & `eda_deep_dive.py`: Exploratory Data Analysis scripts used for initial dataset investigation.

### 2. Modeling (`src/modeling/`)
*   `train_model.py`: Trains a Random Forest Classifier to predict `Won_Game` using features `ScoreDiff`, `EndID`, `Hammer`, and `PowerPlay`.

### 3. Analysis (`src/analysis/`)
#### Core (`src/analysis/core/`)
*   `optimal_strategy.py`: Simulates outcomes for all possible game states to calculate WPA and generates the strategy heatmap.
*   `analyze_rock_location.py`: Visualizes the location of the first thrown stone for winning vs. losing outcomes.
*   `analyze_rock_location_stats.py`: Calculates statistical centroids (X,Y) of guard stones.

#### Sensitivity (`src/analysis/sensitivity/`)
*   `sensitivity_execution.py`: Tests if the "Null Result" holds across different scoring thresholds (2, 3, 4, 5 pts).
*   `sensitivity_strategy.py`: Bootstraps the WPA model 20x to verify the stability of the "Catch-Up Rule".

#### Legacy (`src/analysis/legacy/`)
*   `basic_analysis.py`: Initial exploration (Avg Points) discarded in favor of WPA.

### 4. Utilities (`src/utils/`)
*   `visualize_sheet.py`: Plots raw stone coordinates to reverse-engineer the physical dimensions of the curling sheet.
*   `check_coords.py`: Performs initial sanity checks on coordinate ranges.
*   `find_center.py`: Uses density clustering to identify the exact center of the House.
*   `calibrate_coords.py`: Calculates the pixel-to-foot scale factor.

### Documentation Resources
*   `documentation/papers/`: Contains the full narrative report and analysis chapters.
*   `documentation/artifacts/`: Contains generated figures (Heatmaps, Maps) with technical descriptor files.
