import pandas as pd
from sklearn.model_selection import train_test_split
from config import Config

def load_data():
    df = pd.read_csv(Config.DATA_PATH)
    y = (df['action_taken'] == 1).astype(int)
    X = df.drop(columns=['action_taken'])
    return X, y

def train_test_split_data(X, y):
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=Config.RANDOM_STATE)
