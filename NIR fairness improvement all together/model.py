import xgboost as xgb
from sklearn.pipeline import Pipeline
from config import Config

def train_model(X_train, y_train, preprocessor):
    model = xgb.XGBClassifier(
        random_state=Config.RANDOM_STATE,
        eval_metric='logloss',
        n_estimators=150,
        max_depth=5,
        colsample_bytree=0.8,
        subsample=1.0,
        learning_rate=0.1
    )

    pipeline = Pipeline([
        ('prep', preprocessor),
        ('clf', model)
    ])

    pipeline.fit(X_train, y_train)
    return pipeline