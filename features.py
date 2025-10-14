from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

def build_preprocessor(df):
    cat_features = [
        'loan_type', 'property_type', 'owner_occupancy', 'preapproval',
        'applicant_ethnicity', 'applicant_race_1', 'applicant_sex',
        'purchaser_type', 'hoepa_status', 'lien_status'
    ]
    
    num_features = [
        'loan_amount_000s', 'applicant_income_000s', 'rate_spread',
        'population', 'minority_population', 'hud_median_family_income',
        'tract_to_msamd_income', 'number_of_owner_occupied_units',
        'number_of_1_to_4_family_units'
    ]

    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ])
    
    return preprocessor
