from sklearn.metrics import f1_score
import numpy as np

def optimize_threshold(model, X, y, positive_class=0):
    thresholds = np.linspace(0.1, 0.9, 50)
    probs = model.predict_proba(X)[:, 1]
    best_thresh = 0.5
    best_f1 = -1

    for thresh in thresholds:
        preds = (probs >= thresh).astype(int)
        f1 = f1_score(y, preds, pos_label=positive_class)
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = thresh

    return best_thresh, best_f1
