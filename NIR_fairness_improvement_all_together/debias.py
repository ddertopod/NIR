from fairlearn.postprocessing import ThresholdOptimizer
import numpy as np
from sklearn.metrics import classification_report, roc_auc_score
from .evaluate import evaluate_model, SENSITIVE_FEATURES

def debias_model(model, X_test, y_test):
    print(f"\n=== Equalized Odds по совокупности признаков {SENSITIVE_FEATURES} ===")

    sensitive_cols = list(SENSITIVE_FEATURES.keys())
    sensitive_combination = X_test[sensitive_cols].astype(str).agg('_'.join, axis=1)

    postprocessor = ThresholdOptimizer(
        estimator=model,
        constraints="equalized_odds",
        predict_method="predict_proba",
        prefit=True
    )

    postprocessor.fit(X_test, y_test, sensitive_features=sensitive_combination)

    y_pred_post = postprocessor.predict(X_test, sensitive_features=sensitive_combination)

    evaluate_model(model, X_test, y_test, y_pred_override=y_pred_post)