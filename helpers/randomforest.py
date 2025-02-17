import json
import argparse
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Feature extraction functions
def hash_length(h):
    return len(h)

def hex_ratio(h):
    return sum(c in "0123456789abcdefABCDEF" for c in h) / len(h)

def digit_ratio(h):
    return sum(c.isdigit() for c in h) / len(h)

def uppercase_ratio(h):
    return sum(c.isupper() for c in h) / len(h)

# Load and preprocess JSON data
def load_data(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    
    records = []
    for index, entry in enumerate(data):
        plaintext = entry.get("rockyou", "UNKNOWN")
        for algo, h in entry.items():
            if algo != "rockyou":
                records.append({
                    "index": index,
                    "plaintext": plaintext,
                    "algorithm": algo.replace("rock", ""),
                    "hash": h
                })
    
    df = pd.DataFrame(records)
    return df

# Extract features from hashes
def extract_features(df):
    df["length"] = df["hash"].apply(hash_length)
    df["hex_ratio"] = df["hash"].apply(hex_ratio)
    df["digit_ratio"] = df["hash"].apply(digit_ratio)
    df["uppercase_ratio"] = df["hash"].apply(uppercase_ratio)
    
    df["algorithm"] = df["algorithm"].astype("category")
    df["algorithm_code"] = df["algorithm"].cat.codes
    
    return df

# Train the model and save checkpoint
def train_model(df, model_path):
    X = df.drop(columns=["index", "plaintext", "hash", "algorithm", "algorithm_code"])
    y = df["algorithm_code"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    
    joblib.dump((model, df["algorithm"].cat.categories), model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model to detect hashing algorithms.")
    parser.add_argument("json_file", help="Path to the JSON dataset file")
    parser.add_argument("model_output", help="Path to save the trained model", default="hash_model.pkl")
    args = parser.parse_args()
    
    df = load_data(args.json_file)
    df = extract_features(df)
    train_model(df, args.model_output)
