import argparse
import joblib
import numpy as np
import pandas as pd
import os
import sys

# Feature extraction functions
def hash_length(h):
    return len(h)

def hex_ratio(h):
    return sum(c in "0123456789abcdefABCDEF" for c in h) / len(h)

def digit_ratio(h):
    return sum(c.isdigit() for c in h) / len(h)

def uppercase_ratio(h):
    return sum(c.isupper() for c in h) / len(h)

# Predict the algorithm for a new hash
def predict_algorithm(model_path, hash_value):
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        model, categories = joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {str(e)}", file=sys.stderr)
        sys.exit(1)

    if not hash_value:
        print("Error: No hash value provided.", file=sys.stderr)
        sys.exit(1)

    # Extract features with the correct column names
    feature_names = ["length", "hex_ratio", "digit_ratio", "uppercase_ratio"]
    features = np.array([
        hash_length(hash_value),
        hex_ratio(hash_value),
        digit_ratio(hash_value),
        uppercase_ratio(hash_value)
    ]).reshape(1, -1)

    features_df = pd.DataFrame(features, columns=feature_names)  # Ensure named columns

    try:
        prediction = model.predict(features_df)
        return categories[prediction[0]]
    except Exception as e:
        print(f"Prediction error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict hashing algorithm using a trained model.")
    parser.add_argument("model_file", help="Path to the trained model file")
    parser.add_argument("hash_value", help="Hash to predict the algorithm for")
    args = parser.parse_args()

    result = predict_algorithm(args.model_file, args.hash_value)
    print(f"{result}")
