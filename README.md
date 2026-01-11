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
Install the necessary Python headers:
```bash
pip install -r requirements.txt
```
*Validated on Python 3.9+ with pandas 2.0+*

### 2. Execution Order
Run the following scripts in the specified order to reproduce the analysis pipeline:

1.  **Data Cleaning & Feature Engineering:**
    ```bash
    python3 src/feature_engineering.py
    ```
    *Output:* Generates `modeling_data.csv` (Merged game states with calculated Score Differentials).

2.  **Model Training:**
    ```bash
    python3 src/train_model.py
    ```
    *Output:* Trains the Random Forest model, saves it to `models/`, and produces `modeling_data_with_probs.csv`.

3.  **Strategy Analysis (The "When"):**
    ```bash
    python3 src/optimal_strategy.py
    ```
    *Output:* Generates `analysis/optimal_strategy_heatmap.png` (The WPA Decision Matrix).

4.  **Tactic Analysis (The "How"):**
    ```bash
    python3 src/analyze_rock_location_stats.py
    ```
    *Output:* Prints statistical comparison of winning vs. losing stone coordinates to console.

---

## 📂 File Dictionary

### Core Pipeline
*   `src/feature_engineering.py`: Merges raw `Ends.csv` and `Games.csv` using composite keys and calculates the running Score Differential.
*   `src/train_model.py`: Trains a Random Forest Classifier to predict `Won_Game` using features `ScoreDiff`, `EndID`, `Hammer`, and `PowerPlay`.
*   `src/optimal_strategy.py`: Simulates outcomes for all possible game states to calculate Win Probability Added (WPA) and generates the strategy heatmap.
*   `src/analyze_rock_location.py`: Filters Power Play ends to isolate the first thrown stone and visualizes its location for winning vs. losing outcomes.
*   `src/analyze_rock_location_stats.py`: Calculates the precise centroids (X,Y) of guard stones to test for statistical significance in placement.

### Visualization & Forensics
*   `src/visualize_sheet.py`: Plots raw stone coordinates to reverse-engineer the physical dimensions of the curling sheet.
*   `src/check_coords.py`: Performs initial sanity checks on coordinate ranges to filter out sentinel error values (e.g., 4095).
*   `src/find_center.py`: Uses density clustering to mathematically identify the exact center of the House (Button).
*   `src/calibrate_coords.py`: Calculates the pixel-to-foot scale factor based on standard ring radii.

### Documentation Resources
*   `documentation/papers/`: Contains the full narrative report and analysis chapters.
*   `documentation/artifacts/`: Contains generated figures (Heatmaps, Maps) with technical descriptor files.
