from src.utils.validation_rules import validate_date, COLUMN_RULES
from src.data.study_log import StudyLog
def validate_study_log(log:StudyLog) -> bool:
    """ 
    used to validate the study log object
    Returns True if valid else false.
    """
    if not validate_date(log.date):
        return False
    
    numeric_fields = [
        "sleep_hours",
        "study_hours",
        "screen_time",
        "exercise_minutes",
        "mood_score",
        "energy_level",
        "task_difficulty",
        "study_sessions",
        "distractions",
        "goal_completion",
        "productivity_rating"
    ]
    for field in numeric_fields:
        value = getattr(log, field)
        rules = COLUMN_RULES.get(field)
        if value < rules["min"] or value > rules["max"]:
            return False
    return True