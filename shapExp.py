import shap
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import RocCurveDisplay

def explain_model(model, X_sample, y_sample, max_display=20):
    print("SHAP объяснение модели...")
    preprocessor = model.named_steps['prep']
    classifier = model.named_steps['clf']
    X_prepared = preprocessor.transform(X_sample)
    if hasattr(X_prepared, "toarray"):
        X_prepared = X_prepared.toarray()
    feature_names = preprocessor.get_feature_names_out(input_features=X_sample.columns)
    X_prepared_df = pd.DataFrame(X_prepared, columns=feature_names, index=X_sample.index)
    explainer = shap.Explainer(classifier)
    shap_values = explainer(X_prepared_df)
    plt.figure()
    shap.plots.beeswarm(shap_values, max_display=max_display, show=False)
    plt.savefig("shap_beeswarm.png", bbox_inches='tight')
    plt.close()
    print("SHAP plot сохранён как shap_beeswarm.png")

    print("ROC-кривая...")
    RocCurveDisplay.from_estimator(model, X_sample, y_sample)
    plt.savefig("roc_curve.png", bbox_inches='tight')
    plt.close()
    print("ROC curve сохранена как roc_curve.png")

