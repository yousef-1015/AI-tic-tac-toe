# trainer.py
import pandas as pd
import os
from ml_model import LinearModel

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def train(silent=False):
    dataset_path = os.path.join(SCRIPT_DIR, "tictactoe_dataset.csv")
    df = pd.read_csv(dataset_path)

    # Safety: remove hidden spaces
    df.columns = df.columns.str.strip()

    X = df[
        [
            "f1_X_count",
            "f2_O_count",
            "f3_X_almost_win",
            "f4_O_almost_win",
            "f5_X_center",
            "f6_X_corners"
        ]
    ].values

    y = df["label"].values

    model = LinearModel()
    lr = 0.01  # Increased from 0.001
    epochs = 200  # Increased from 50

    for epoch in range(epochs):
        total_error = 0
        for features, label in zip(X, y):
            prediction = model.predict_from_features(features)
            error = label - prediction
            total_error += abs(error)

            for i in range(len(model.weights)):
                model.weights[i] += lr * error * features[i]

            model.bias += lr * error
        
        # Print progress every 50 epochs
        if not silent and (epoch + 1) % 50 == 0:
            avg_error = total_error / len(X)
            print(f"Epoch {epoch + 1}/{epochs} - Avg Error: {avg_error:.4f}")

    if not silent:
        print("Training finished successfully")
        print("Weights:", model.weights)
        print("Bias:", model.bias)

    return model

if __name__ == "__main__":
    train()
