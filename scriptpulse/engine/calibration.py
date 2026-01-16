from typing import List
import numpy as np
from sklearn.linear_model import LogisticRegression

# FROZEN WEIGHTS (MANDATORY)
W = 1.0
B = 0.0

def calibrate_strain(accum_effort: List[float]) -> List[float]:
    """
    Maps accumulated effort values to strain probabilities using a frozen Logistic Regression model.
    Inference only.
    """
    if not accum_effort:
        return []

    # Initialize model
    model = LogisticRegression(solver='liblinear')
    
    # Manually set parameters (Inference-only, no training)
    # coef_ shape: (1, n_features) -> (1, 1)
    model.coef_ = np.array([[W]])
    # intercept_ shape: (1,)
    model.intercept_ = np.array([B])
    # classes_ shape: (2,)
    model.classes_ = np.array([0, 1])

    # Sklearn expects 2D array: (n_samples, n_features)
    # Our feature is 'accumulated effort' (scalar per sample)
    X = np.array(accum_effort).reshape(-1, 1)

    # Predict probabilities
    # predict_proba returns (n_samples, 2), we want P(class=1) -> column 1
    probs = model.predict_proba(X)[:, 1]

    # Return as list of floats
    return probs.tolist()
