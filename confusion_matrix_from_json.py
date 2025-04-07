import json
import argparse
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Feature extraction functions
def hash_length(h): return len(h)
def hex_ratio(h): return sum(c in "0123456789abcdefABCDEF" for c in h) / len(h)
def digit_ratio(h): return sum(c.isdigit() for c in h) / len(h)
def uppercase_ratio(h): return sum(c.isupper() for c in h) / len(h)

def extract_features(hashes):
    return pd.DataFrame([{
        "length": hash_length(h),
        "hex_ratio": hex_ratio(h),
        "digit_ratio": digit_ratio(h),
        "uppercase_ratio": uppercase_ratio(h)
    } for h in hashes])

def flatten_json_to_hash_label_pairs(json_data):
    pairs = []
    for entry in json_data:
        for key, hashed in entry.items():
            if key != "rockyou":  # Skip plaintext
                label = key.replace("rock", "")  # Extract just the algorithm name
                pairs.append((hashed, label))
    return pairs

def main(model_path, json_file):
    if not os.path.exists(model_path) or not os.path.exists(json_file):
        print("Model file or JSON file not found.")
        return

    # Load model
    model, categories = joblib.load(model_path)

    # Load and flatten JSON
    with open(json_file, 'r') as f:
        data = json.load(f)
    hash_label_pairs = flatten_json_to_hash_label_pairs(data)
    
    hashes, y_true = zip(*hash_label_pairs)
    X_test = extract_features(hashes)
    y_pred = [categories[i] for i in model.predict(X_test)]

    # Display results
    print("Classification Report:\n")
    print(classification_report(y_true, y_pred))

    cm = confusion_matrix(y_true, y_pred, labels=categories)
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=categories, yticklabels=categories, cmap="coolwarm")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test model on JSON hash data and generate confusion matrix.")
    parser.add_argument("model_file", help="Path to the trained .pkl model")
    parser.add_argument("json_file", help="Path to the JSON file with hash data")
    args = parser.parse_args()
    main(args.model_file, args.json_file)
