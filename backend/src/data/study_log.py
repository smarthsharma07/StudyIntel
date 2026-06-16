from dataclasses import dataclass

@dataclass
class StudyLog:
    date: str
    sleep_hours: float
    study_hours: float
    screen_time: float
    exercise_minutes: int
    mood_score: int
    energy_level: int
    task_difficulty: int
    study_sessions: int
    distractions: int
    goal_completion: float
    subject: str
    productivity_rating: int