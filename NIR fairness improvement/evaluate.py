from sklearn.metrics import roc_auc_score, classification_report
import numpy as np

SENSITIVE_FEATURES = {
    'applicant_sex': 'Sex',
    'applicant_race_1': 'Race',
    'applicant_ethnicity': 'Ethnicity'
}

def evaluate_model(model, X_test, y_test, y_pred_override=None):
    if y_pred_override is not None:
        preds = y_pred_override
        proba = None
    else:
        preds = model.predict(X_test)
        proba = model.predict_proba(X_test)[:, 1]

    print("=== Классический отчёт по классификации ===")
    print(classification_report(y_test, preds, digits=3))
    if proba is not None:
        print("ROC AUC:", roc_auc_score(y_test, proba))

    print("\n=== Метрики честности ===")
    for col, name in SENSITIVE_FEATURES.items():
        if col not in X_test.columns:
            print(f"[!] Признак '{col}' не найден в X_test. Пропускаем.")
            continue

        print(f"\n{name} ({col})")
        sensitive_feature = X_test[col].values
        groups = np.unique(sensitive_feature)

        for group in groups:
            idx = (sensitive_feature == group)
            if idx.sum() == 0:
                continue

            group_name = f"{name} = {group}"
            dp = preds[idx].mean()

            tp = ((preds[idx] == 1) & (y_test[idx] == 1)).sum()
            fn = ((preds[idx] == 0) & (y_test[idx] == 1)).sum()
            tpr = tp / (tp + fn) if (tp + fn) > 0 else float('nan')

            fp = ((preds[idx] == 1) & (y_test[idx] == 0)).sum()
            tn = ((preds[idx] == 0) & (y_test[idx] == 0)).sum()
            fpr = fp / (fp + tn) if (fp + tn) > 0 else float('nan')

            print(f"[{group_name}] Demographic Parity = {dp:.3f}, TPR = {tpr:.3f}, FPR = {fpr:.3f}")
