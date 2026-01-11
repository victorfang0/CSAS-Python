
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score
import os
import pickle

DATA_PATH = "/Users/victor/Desktop/CSAS/analysis/modeling_data.csv"
MODEL_DIR = "/Users/victor/Desktop/CSAS/models/"

def train_wp_model():
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    # Feature Engineering for Model
    # We want to predict 'Won_Game' based on State features
    features = ['EndID', 'ScoreDiff', 'Hammer', 'PowerPlay_Active']
    target = 'Won_Game'
    
    # Preprocessing
    # Hammer is boolean, convert to int
    df['Hammer'] = df['Hammer'].astype(int)
    df['PowerPlay_Active'] = df['PowerPlay_Active'].astype(int)
    
    X = df[features]
    y = df[target].astype(int)
    
    print(f"Dataset Shape: {X.shape}")
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # RandomForest Classifier (Robust replacement for XGBoost)
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluation
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, probs)
    
    print(f"\n--- Model Results ---")
    print(f"Accuracy: {acc:.4f}")
    print(f"AUC Score: {auc:.4f}")
    
    # Feature Importance
    print("\nFeature Importance:")
    importances = model.feature_importances_
    for name, imp in zip(features, importances):
        print(f"{name}: {imp:.4f}")
        
    # Full Dataset Prediction for Analysis (WPA Calculation later)
    df['WinProb'] = model.predict_proba(X)[:, 1]
    
    # Save Model
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, "wp_rf.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved to {model_path}")
    
    # Save Augmented Data
    aug_path = DATA_PATH.replace(".csv", "_with_probs.csv")
    df.to_csv(aug_path, index=False)
    print(f"Data with WinProb saved to {aug_path}")

if __name__ == "__main__":
    train_wp_model()
