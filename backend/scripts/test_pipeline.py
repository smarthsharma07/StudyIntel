"""
scripts/test_pipeline.py
========================
Integration test for the full StudyIntel backend pipeline.

Exercises:
  - Validation
  - DB insert (user-scoped)
  - DB fetch (user-scoped)
  - Analytics (daily / weekly / monthly / streaks)
  - Feature engineering
  - Preprocessing (CatBoost-safe, no LabelEncoder)
  - Prediction
  - SHAP explanation

Run from the backend/ directory:
    python scripts/test_pipeline.py
"""

import sys
import traceback
from pathlib import Path
from pprint import pprint

# Make sure backend/ is on the path for absolute imports
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from src.services.pipeline import process_study_log

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

TEST_CASES = [
    {
        "name": "GOOD DAY (known subject: Mathematics)",
        "username": "test_user_integration",
        "log": {
            "date": "2026-06-20",
            "sleep_hours": 8.0,
            "study_hours": 6.0,
            "screen_time": 2.0,
            "exercise_minutes": 45,
            "mood_score": 9,
            "energy_level": 9,
            "task_difficulty": 4,
            "study_sessions": 4,
            "distractions": 1,
            "goal_completion": 95.0,
            "subject": "Mathematics",
            "productivity_rating": 9,
        },
    },
    {
        "name": "AVERAGE DAY (unseen subject: DSA)",
        "username": "test_user_integration",
        "log": {
            "date": "2026-06-21",
            "sleep_hours": 7.0,
            "study_hours": 3.0,
            "screen_time": 5.0,
            "exercise_minutes": 20,
            "mood_score": 5,
            "energy_level": 5,
            "task_difficulty": 3,
            "study_sessions": 2,
            "distractions": 4,
            "goal_completion": 55.0,
            "subject": "DSA",
            "productivity_rating": 5,
        },
    },
    {
        "name": "BAD DAY (unseen subject: RTL Design)",
        "username": "test_user_integration",
        "log": {
            "date": "2026-06-22",
            "sleep_hours": 3.0,
            "study_hours": 1.0,
            "screen_time": 10.0,
            "exercise_minutes": 0,
            "mood_score": 2,
            "energy_level": 2,
            "task_difficulty": 5,
            "study_sessions": 1,
            "distractions": 10,
            "goal_completion": 10.0,
            "subject": "RTL Design",
            "productivity_rating": 2,
        },
    },
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_test(case: dict) -> bool:
    name = case["name"]
    username = case["username"]
    log = case["log"]

    print(f"\n{'=' * 70}")
    print(f"TEST: {name}")
    print(f"{'=' * 70}")

    try:
        results = process_study_log(username=username, study_log_dict=log)

        # --- Prediction ---
        pred = results["prediction"]
        assert isinstance(pred, float), "prediction must be float"
        assert 0.0 <= pred <= 10.0, f"prediction {pred} out of [0,10] range"
        print(f"\n[PASS] Prediction: {pred:.2f}")

        # --- Analytics ---
        analytics = results["analytics"]
        for key in ("daily", "weekly", "monthly", "streaks"):
            assert key in analytics, f"Missing analytics key: {key}"
        print(f"[PASS] Analytics keys present: {list(analytics.keys())}")
        print("       Daily summary:", analytics["daily"])

        # --- SHAP ---
        shap = results["shap"]
        for key in ("prediction", "base_value", "positive_factors",
                    "negative_factors", "shap_dataframe"):
            assert key in shap, f"Missing SHAP key: {key}"
        print(f"[PASS] SHAP base value: {shap['base_value']:.4f}")
        print("       Top positive factors:")
        print(shap["positive_factors"].to_string(index=False))
        print("       Top negative factors:")
        print(shap["negative_factors"].to_string(index=False))

        return True

    except Exception as exc:
        print(f"\n[FAIL] {name}")
        print(f"       Error: {exc}")
        traceback.print_exc()
        return False


def main():
    print("\n" + "=" * 70)
    print("STUDYINTEL PIPELINE INTEGRATION TEST")
    print("=" * 70)

    passed = 0
    failed = 0

    for case in TEST_CASES:
        ok = run_test(case)
        if ok:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 70}")
    print(f"RESULTS:  {passed} passed  |  {failed} failed")
    print("=" * 70)

    if failed:
        print("SOME TESTS FAILED – review the output above.")
        sys.exit(1)
    else:
        print("ALL TESTS PASSED [OK]")


if __name__ == "__main__":
    main()
