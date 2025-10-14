import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def analyze_correlations(df, top_n=10):
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    
    corr_matrix = numeric_df.corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, cmap='coolwarm', annot=False, fmt=".2f")
    plt.title("Корреляционная матрица числовых признаков")
    plt.tight_layout()
    plt.show()

    corr_pairs = (
        corr_matrix.where(~np.eye(corr_matrix.shape[0], dtype=bool))  
        .stack()
        .abs()
        .sort_values(ascending=False)
    )

    print(f"\nТоп-{top_n} коррелирующих пар признаков (по модулю):\n")
    for (f1, f2), corr in corr_pairs.drop_duplicates().head(top_n).items():
        print(f"{f1} — {f2}: корреляция = {corr:.3f}")
