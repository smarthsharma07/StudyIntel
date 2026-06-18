import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

from lightgbm import LGBMRegressor

df = pd.read_csv(
    r"C:\Users\Smarth Sharma\Desktop\StudyIntel-1\backend\data\processed\studyintel_processed.csv"
)

TARGET = "productivity_rating"
if "date" in df.columns:
    df = df.drop(columns=["date"])
X = df.drop(columns=[TARGET])
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(f"Train Shape: {X_train.shape}")
print(f"Test Shape : {X_test.shape}")

model = LGBMRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
    verbose=-1
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

r2 = r2_score(y_test, predictions)

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

print("\n===== LIGHTGBM RESULTS =====")

print(f"R² Score : {r2:.4f}")
print(f"MAE      : {mae:.4f}")
print(f"RMSE     : {rmse:.4f}")

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\n===== FEATURE IMPORTANCE =====")
print(importance_df)

joblib.dump(
    model,
    "artifacts/lightgbm_v1.pkl"
)

print("\nModel Saved")