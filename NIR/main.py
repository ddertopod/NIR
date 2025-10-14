from data_loader import load_data, train_test_split_data
from features import build_preprocessor
from model import train_model
from evaluate import evaluate_model
from shapExp import explain_model

def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split_data(X, y)
    preprocessor = build_preprocessor(X_train)
    model = train_model(X_train, y_train, preprocessor)
    evaluate_model(model, X_test, y_test)
    X_explain = X_test.sample(300, random_state=42)
    y_explain = y_test.loc[X_explain.index]
    explain_model(model, X_explain, y_explain)

if __name__ == "__main__":
    main()

