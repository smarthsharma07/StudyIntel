import pandas as pd
import joblib

from src.features.feature_engineering import (
    engineer_features
)

from src.explainability.explain import (
    explain_prediction
)


MODEL_PATH = (
    r"C:\Users\Smarth Sharma\Desktop\StudyIntel-1"
    r"\backend\artifacts\trained models\catboost_v1.pkl"
)


TEST_CASES = {

    "GOOD DAY": {
        "expected_range": "8.5 - 10.0",
        "data": {
            "date": ["2026-06-20"],
            "sleep_hours": [8],
            "study_hours": [6],
            "screen_time": [2],
            "exercise_minutes": [45],
            "mood_score": [9],
            "energy_level": [9],
            "task_difficulty": [5],
            "study_sessions": [4],
            "distractions": [1],
            "goal_completion": [95],
            "subject": ["DSA"]
        }
    },

    "AVERAGE DAY": {
        "expected_range": "5.0 - 7.5",
        "data": {
            "date": ["2026-06-20"],
            "sleep_hours": [7],
            "study_hours": [3],
            "screen_time": [5],
            "exercise_minutes": [20],
            "mood_score": [5],
            "energy_level": [5],
            "task_difficulty": [6],
            "study_sessions": [2],
            "distractions": [4],
            "goal_completion": [55],
            "subject": ["DSA"]
        }
    },

    "BAD DAY": {
        "expected_range": "0.0 - 4.0",
        "data": {
            "date": ["2026-06-20"],
            "sleep_hours": [3],
            "study_hours": [1],
            "screen_time": [10],
            "exercise_minutes": [0],
            "mood_score": [2],
            "energy_level": [2],
            "task_difficulty": [8],
            "study_sessions": [1],
            "distractions": [10],
            "goal_completion": [10],
            "subject": ["DSA"]
        }
    }
}


def run_test_case(
    case_name: str,
    case_data: dict,
    model
):

    print("\n")
    print("=" * 80)
    print(case_name)
    print("=" * 80)

    print(
        f"Expected Prediction Range: "
        f"{case_data['expected_range']}"
    )

    raw_df = pd.DataFrame(
        case_data["data"]
    )

    engineered_df = engineer_features(
        raw_df
    )

    prediction_df = engineered_df[
        model.feature_names_
    ]

    results = explain_prediction(
        model=model,
        prediction_df=prediction_df,
        top_n=5
    )

    print(
        f"\nBase Productivity: "
        f"{results['base_value']:.2f}"
    )

    print(
        f"Predicted Productivity: "
        f"{results['prediction']:.2f}"
    )

    print("\nTOP POSITIVE FACTORS")
    print("-" * 40)

    for _, row in results[
        "positive_factors"
    ].iterrows():

        print(
            f"{row['feature']}: "
            f"+{row['shap_value']:.3f}"
        )

    print("\nTOP NEGATIVE FACTORS")
    print("-" * 40)

    for _, row in results[
        "negative_factors"
    ].iterrows():

        print(
            f"{row['feature']}: "
            f"{row['shap_value']:.3f}"
        )

    print("\nFULL SHAP TABLE")
    print("-" * 40)

    print(
        results["shap_dataframe"]
        .sort_values(
            "shap_value",
            ascending=False
        )
    )


def main():

    model = joblib.load(
        MODEL_PATH
    )

    print("=" * 80)
    print("STUDYINTEL SHAP VALIDATION")
    print("=" * 80)

    for case_name, case_data in (
        TEST_CASES.items()
    ):

        run_test_case(
            case_name,
            case_data,
            model
        )


if __name__ == "__main__":
    main()