import pandas as pd
import joblib

from src.features.feature_engineering import engineer_features


MODEL_PATH = (
    r"C:\Users\Smarth Sharma\Desktop\StudyIntel-1"
    r"\backend\artifacts\trained models\catboost_v1.pkl"
)


def main():

    print("=" * 60)
    print("RAW USER INPUT")
    print("=" * 60)

    raw_df = pd.DataFrame({
        "date": ["2026-06-20"],
        "sleep_hours": [3],
        "study_hours": [1],
        "screen_time": [10],
        "exercise_minutes": [30],
        "mood_score": [2],
        "energy_level": [7],
        "task_difficulty": [6],
        "study_sessions": [4],
        "distractions": [2],
        "goal_completion": [10],
        "subject": ["DSA"],
        
    })

    print(raw_df)

    print("\n" + "=" * 60)
    print("ENGINEERING FEATURES")
    print("=" * 60)

    engineered_df = engineer_features(raw_df)

    print("\nEngineered Columns:")
    print(engineered_df.columns.tolist())

    print("\nEngineered Data:")
    print(engineered_df.head())

    print("\n" + "=" * 60)
    print("LOADING MODEL")
    print("=" * 60)

    model = joblib.load(MODEL_PATH)

    print(type(model))

    print("\n" + "=" * 60)
    print("MODEL EXPECTED FEATURES")
    print("=" * 60)

    print(model.feature_names_)

    print("\n" + "=" * 60)
    print("CHECKING FEATURE MATCH")
    print("=" * 60)

    missing_features = (
        set(model.feature_names_)
        - set(engineered_df.columns)
    )

    extra_features = (
        set(engineered_df.columns)
        - set(model.feature_names_)
    )

    print("Missing Features:")
    print(missing_features)

    print("\nExtra Features:")
    print(extra_features)

    if missing_features:
        print("\nFEATURE MISMATCH")
        return

    prediction_df = engineered_df[
        model.feature_names_
    ].copy()

    # Important for CatBoost
    prediction_df["subject"] = (
        prediction_df["subject"]
        .astype(str)
    )

    print("\nPrediction Data:")
    print(prediction_df.head())

    print("\nPrediction Data Types:")
    print(prediction_df.dtypes)

    print("\n" + "=" * 60)
    print("RUNNING PREDICTION")
    print("=" * 60)

    prediction = model.predict(
        prediction_df
    )

    print(
        f"\nPredicted Productivity: "
        f"{prediction[0]:.2f}"
    )

    print("\nINFERENCE PIPELINE SUCCESS")


if __name__ == "__main__":
    main()