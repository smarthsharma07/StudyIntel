import datetime

COLUMN_RULES = {

    "date": {
        "type": "date",
        "format": "%Y-%m-%d",
        "min_year": 2020,
        "max_year": 2100
    },

    "sleep_hours": {
        "type": float,
        "min": 2.0,
        "max": 16.0
    },

    "study_hours": {
        "type": float,
        "min": 0.0,
        "max": 18.0
    },

    "screen_time": {
        "type": float,
        "min": 0.0,
        "max": 18.0
    },

    "exercise_minutes": {
        "type": int,
        "min": 0,
        "max": 180
    },

    "mood_score": {
        "type": int,
        "min": 1,
        "max": 10
    },

    "energy_level": {
        "type": int,
        "min": 1,
        "max": 10
    },

    "task_difficulty": {
        "type": int,
        "min": 1,
        "max": 5
    },

    "study_sessions": {
        "type": int,
        "min": 1,
        "max": 20
    },

    "distractions": {
        "type": int,
        "min": 0,
        "max": 100
    },

    "goal_completion": {
        "type": float,
        "min": 0.0,
        "max": 100.0
    },

    "subject": {
        "type": str
    },

    "productivity_rating": {
        "type": int,
        "min": 1,
        "max": 10
    }
}
def validate_date(date_string: str) -> bool:
    try:
        date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")

        if date_obj.year < 2020 or date_obj.year > 2100:
            return False

        return True

    except ValueError:
        return False