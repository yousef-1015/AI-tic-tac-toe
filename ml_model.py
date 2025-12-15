# ml_model.py

class LinearModel:
    def __init__(self):
        # 6 features
        self.weights = [0.0] * 6
        self.bias = 0.0

    def predict_from_features(self, features):
        return sum(w * x for w, x in zip(self.weights, features)) + self.bias
