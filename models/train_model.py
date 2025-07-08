# train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(__file__), '../data')
# Load data

df=pd.read_csv(os.path.join(DATA_PATH, 'demand_training_data.csv'))
# Features and target
X = df[["district", "month", "festival_flag", "income_level", "kirana_density", "sku"]]
y = df["demand"]

# Categorical encoding
categorical_cols = ["district", "month", "income_level", "kirana_density", "sku"]
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
])

# Model pipeline
model = Pipeline([
    ("preprocess", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train model
model.fit(X, y)

# Save model
MODEL_PATH = os.path.join(BASE_DIR, "demand_model.pkl")  # 👈 Save in same folder
joblib.dump(model, MODEL_PATH)

print("✅ Model trained and saved at:", MODEL_PATH)
