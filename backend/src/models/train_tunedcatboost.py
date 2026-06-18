import pandas as pd
import joblib

from catboost import CatBoostRegressor

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV
)

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

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

cat_model = CatBoostRegressor(
    loss_function="RMSE",
    verbose=0,
    random_seed=42
)

param_grid = {

    "iterations": [
        200,
        400,
        600,
        800
    ],

    "depth": [
        4,
        6,
        8,
        10
    ],

    "learning_rate": [
        0.01,
        0.03,
        0.05,
        0.1
    ],

    "l2_leaf_reg": [
        1,
        3,
        5,
        7,
        9
    ],

    "subsample": [
        0.7,
        0.8,
        0.9,
        1.0
    ]
}

search = RandomizedSearchCV(

    estimator=cat_model,

    param_distributions=param_grid,

    n_iter=20,

    scoring="r2",

    cv=5,

    verbose=2,

    random_state=42,

    n_jobs=4
)

search.fit(
    X_train,
    y_train
)

best_model = search.best_estimator_

print("\n===== BEST PARAMETERS =====")
print(search.best_params_)

predictions = best_model.predict(
    X_test
)
r2 = r2_score(
    y_test,
    predictions
)

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

print("\n===== TUNED CATBOOST RESULTS =====")

print(f"R² Score : {r2:.4f}")
print(f"MAE      : {mae:.4f}")
print(f"RMSE     : {rmse:.4f}")

joblib.dump(
    best_model,
    "artifacts/tuned_catboost.pkl"
)

print("\nTuned Model Saved")