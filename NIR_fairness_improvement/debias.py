from fairlearn.postprocessing import ThresholdOptimizer
import numpy as np
from sklearn.metrics import classification_report, roc_auc_score
from .evaluate import evaluate_model

def debias_model(model, X_test, y_test, sensitive_column):
    print(f"\n=== Equalized Odds по признаку '{sensitive_column}' ===")

    postprocessor = ThresholdOptimizer(
        estimator=model,
        constraints="equalized_odds",
        predict_method="predict_proba",
        prefit=True
    )
    postprocessor.fit(X_test, y_test, sensitive_features=X_test[sensitive_column])

    y_pred_post = postprocessor.predict(X_test, sensitive_features=X_test[sensitive_column])

    evaluate_model(model, X_test, y_test, y_pred_override=y_pred_post)