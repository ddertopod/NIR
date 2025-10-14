from data_loader import load_data, train_test_split_data
from features import build_preprocessor
from model import train_model
from evaluate import evaluate_model, SENSITIVE_FEATURES
from shapExp import explain_model
from debias import debias_model
from config import Config
from optimize_threshhold import optimize_threshold  
import numpy as np

def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split_data(X, y)

    preprocessor = build_preprocessor(X_train)
    model = train_model(X_train, y_train, preprocessor)

    print("\n=== Базовая модель ===")
    y_proba = model.predict_proba(X_test)[:, 1]
    best_thresh, best_f1 = optimize_threshold(model, X_test, y_test, positive_class=0)

    y_pred_opt = np.where(y_proba < best_thresh, 0, 1)

    evaluate_model(model, X_test, y_test, y_pred_override=y_pred_opt, y_proba_override=y_proba)

    print(f"\n[THRESHOLD OPTIMIZER] Лучший порог для класса 0: {best_thresh:.3f} — F1: {best_f1:.3f}")

    X_explain = X_test.sample(300, random_state=Config.RANDOM_STATE)
    y_explain = y_test.loc[X_explain.index]
    explain_model(model, X_explain, y_explain)

    debias_model(model, X_test, y_test)

if __name__ == "__main__":
    main()
