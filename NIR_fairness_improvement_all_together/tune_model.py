import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, f1_score
from config import Config

def train_model(X_train, y_train, preprocessor):
    base_model = xgb.XGBClassifier(
        random_state=Config.RANDOM_STATE,
        eval_metric='logloss'
    )

    pipeline = Pipeline([
        ('prep', preprocessor),
        ('clf', base_model)
    ])

    param_grid = {
        'clf__n_estimators': [100, 150],
        'clf__max_depth': [3, 5],
        'clf__learning_rate': [0.05, 0.1],
        'clf__subsample': [0.8, 1.0],
        'clf__colsample_bytree': [0.8, 1.0]
    }
    f1_class0 = make_scorer(f1_score, pos_label=0)
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=3,
        scoring=f1_class0,
        verbose=2,
        n_jobs=-1
    )

    print("[MODEL] Запуск подбора гиперпараметров...")
    grid_search.fit(X_train, y_train)
    print("[MODEL] Подбор завершён.")
    print("Лучшие параметры:", grid_search.best_params_)
    print("ROC AUC (валидация):", grid_search.best_score_)

    return grid_search.best_estimator_
