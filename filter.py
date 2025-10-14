import pandas as pd
from config import Config
from corr import analyze_correlations
df = pd.read_csv(Config.NOT_FILTERED_DATA_PATH, low_memory=False)
df.columns = [col.lower().strip() for col in df.columns]
initial_columns = len(df.columns)
print(f"Фильтрация начинается. Базовое кол-во строк: {len(df)}")
print(f"Базовое кол-во колонок: {initial_columns}")
df = df[
    (df['loan_purpose'] == 1) &
    (df['action_taken'].isin([1, 3])) &
    (df['applicant_sex'].isin([1, 2])) &
    (df['applicant_race_1'].isin([1, 2, 3, 4, 5])) &
    (df['applicant_ethnicity'].isin([1, 2])) &
    (df['applicant_income_000s'] != 'NA')
]
df = df[[col for col in df.columns if "_name" not in col]]
after_name_columns = len(df.columns)
empty_cols = df.columns[df.isna().all()]
df = df.drop(columns=empty_cols)
after_empty_columns = len(df.columns)
race_cols_to_drop = [
    'applicant_race_3', 'applicant_race_4', 'applicant_race_5',
    'co_applicant_race_3', 'co_applicant_race_4', 'co_applicant_race_5'
]
existing_race_cols = [col for col in race_cols_to_drop if col in df.columns]
df = df.drop(columns=existing_race_cols)
after_race_columns = len(df.columns)
denial_cols = ['denial_reason_1', 'denial_reason_2', 'denial_reason_3']
existing_denial_cols = [col for col in denial_cols if col in df.columns]
df = df.drop(columns=existing_denial_cols)
after_denial_columns = len(df.columns)
analyze_correlations(df,15)
df.to_csv(Config.DATA_PATH, index=False)
print(f"Фильтрация завершена. Осталось строк: {len(df)}")
print(f"Удалено колонок с '_name': {initial_columns - after_name_columns}")
print(f"Удалено полностью пустых колонок: {after_name_columns - after_empty_columns}")
print(f"Удалено колонок с race_3-5: {after_empty_columns - after_race_columns}")
print(f"Удалено колонок отказов: {after_race_columns - after_denial_columns}")
print(f"Итоговое количество колонок: {after_denial_columns}")