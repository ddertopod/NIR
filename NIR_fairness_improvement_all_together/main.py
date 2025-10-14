from data_loader import load_data, train_test_split_data
from features import build_preprocessor
from .model import train_model
from .evaluate import evaluate_model, SENSITIVE_FEATURES
from shapExp import explain_model
from .debias import debias_model
from config import Config

def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split_data(X, y)
    preprocessor = build_preprocessor(X_train)
    model = train_model(X_train, y_train, preprocessor)
    print("\n=== Базовая модель ===")
    evaluate_model(model, X_test, y_test)
    X_explain = X_test.sample(300, random_state=Config.RANDOM_STATE)
    y_explain = y_test.loc[X_explain.index]
    explain_model(model, X_explain, y_explain)
    
    debias_model(model, X_test, y_test)
    X_explain = X_test.sample(300, random_state=Config.RANDOM_STATE)
    y_explain = y_test.loc[X_explain.index]
    explain_model(model, X_explain, y_explain)

if __name__ == "__main__":
    main()

