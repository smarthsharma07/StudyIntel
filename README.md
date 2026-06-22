# 🧠 StudyIntel

**AI-Powered Study Productivity Intelligence Platform**

StudyIntel is an end-to-end Machine Learning and Analytics platform that helps students understand, track, and improve their study habits.

The system combines **data analytics**, **predictive machine learning**, and **explainable AI (SHAP)** to provide personalized productivity insights based on study behavior, wellness indicators, and learning patterns.

---

##  Features

###  Productivity Prediction

Predicts daily study productivity using a trained CatBoost regression model.

###  Explainable AI (SHAP)

Provides transparent explanations showing which factors increased or decreased productivity predictions.

### 📊 Advanced Analytics Dashboard

* Daily Analytics
* Weekly Analytics
* Monthly Analytics
* Study Streak Tracking
* Subject Performance Analysis
* Historical Study Trends

### 👤 Multi-User Support

Each user's data is stored independently using username-scoped SQLite storage.

###  Subject Analytics

Analyze:

* Study hours by subject
* Productivity by subject
* Difficulty vs Productivity
* Time allocation patterns

###  Study Session Logging

Track:

* Study Hours
* Sleep Hours
* Screen Time
* Exercise
* Mood
* Energy Levels
* Task Difficulty
* Goal Completion
* Distractions
* Study Sessions

###  Interactive Frontend

Built with Streamlit and Plotly for a responsive analytics experience.

---

#  System Architecture

```text
┌──────────────────────────┐
│      Streamlit UI        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Input Validation Layer │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ SQLite Database Storage  │
│ (User-Scoped Logs)       │
└────────────┬─────────────┘
             │
      ┌──────┴──────┐
      ▼             ▼

┌──────────────┐  ┌─────────────────┐
│ Analytics    │  │ Feature         │
│ Engine       │  │ Engineering     │
└──────┬───────┘  └────────┬────────┘
       │                   │
       ▼                   ▼

┌──────────────┐  ┌─────────────────┐
│ Daily        │  │ Preprocessing   │
│ Weekly       │  │ Pipeline        │
│ Monthly      │  └────────┬────────┘
│ Streaks      │           │
└──────────────┘           ▼

                 ┌─────────────────┐
                 │ CatBoost Model  │
                 └────────┬────────┘
                          │
                          ▼

                 ┌─────────────────┐
                 │ SHAP Explainer  │
                 └────────┬────────┘
                          │
                          ▼

                 ┌─────────────────┐
                 │ User Insights   │
                 └─────────────────┘
```

---

#  Machine Learning Pipeline

## Model

**CatBoost Regressor**

Chosen after evaluating multiple models and hyperparameter tuning.

Reasons:

* Excellent handling of tabular data
* Native categorical feature support
* Robust performance on unseen subjects
* Strong explainability support

---

## Feature Engineering

Generated Features:

| Feature                |
| ---------------------- |
| study_efficiency       |
| distraction_rate       |
| screen_study_ratio     |
| wellness_score         |
| optimal_sleep          |
| goal_efficiency        |
| study_sleep_ratio      |
| exercise_study_ratio   |
| sessions_per_hour      |
| average_session_length |
| day_of_week            |
| month                  |
| is_weekend             |
| is_exam_season         |

---

## Explainability

SHAP explanations identify:

### Positive Contributors

Examples:

* High goal completion
* Low distractions
* Strong wellness score
* Healthy study-to-screen ratio

### Negative Contributors

Examples:

* Excessive screen time
* Low energy levels
* Poor sleep habits
* High distraction rates

---

#  Analytics Modules

## Daily Analytics

* Daily productivity overview
* Study statistics
* Wellness indicators

## Weekly Analytics

* Weekly study hours
* Weekly productivity trends
* Consistency tracking

## Monthly Analytics

* Monthly breakdowns
* Long-term performance tracking

## Streak Tracking

* Current streak
* Longest streak
* Study consistency analysis

## Subject Analytics

* Productivity by subject
* Time allocation
* Difficulty vs productivity
* Subject-wise rankings

---

#  Database Design

SQLite is used as the primary source of truth.

### Study Logs Table

| Column              | Type    |
| ------------------- | ------- |
| id                  | INTEGER |
| username            | TEXT    |
| date                | TEXT    |
| sleep_hours         | REAL    |
| study_hours         | REAL    |
| screen_time         | REAL    |
| exercise_minutes    | INTEGER |
| mood_score          | INTEGER |
| energy_level        | INTEGER |
| task_difficulty     | INTEGER |
| study_sessions      | INTEGER |
| distractions        | INTEGER |
| goal_completion     | REAL    |
| subject             | TEXT    |
| productivity_rating | REAL    |

---

#  Project Structure

```text
StudyIntel/

├── frontend/
│   └── streamlit_app.py
│
├── database/
│   ├── db.py
│   ├── crud.py
│   ├── schema.py
│   └── study_logs.db
│
├── src/
│   ├── analytics/
│   ├── data/
│   ├── explainability/
│   ├── features/
│   ├── models/
│   ├── preprocessing/
│   ├── services/
│   └── utils/
│
├── scripts/
│   ├── build_dataset.py
│   ├── gen_data.py
│   └── migrate_db.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

#  Backend Workflow

```text
User Input
    │
    ▼
Validation
    │
    ▼
SQLite Storage
    │
    ▼
Fetch User History
    │
    ├── Analytics Engine
    │
    ▼
Feature Engineering
    │
    ▼
Preprocessing
    │
    ▼
CatBoost Prediction
    │
    ▼
SHAP Explanation
    │
    ▼
Frontend Dashboard
```

---

#  Testing

The backend was validated through integration testing.

Verified:

✅ Data Validation

✅ SQLite Storage

✅ Analytics Generation

✅ Feature Engineering

✅ Preprocessing Pipeline

✅ Prediction Pipeline

✅ SHAP Explainability

✅ Multi-User Isolation

✅ Unseen Subject Handling

Example unseen subjects successfully tested:

* DSA
* RTL Design

---

#  Tech Stack

### Backend

* Python
* Pandas
* NumPy
* SQLite

### Machine Learning

* CatBoost
* Scikit-Learn
* SHAP

### Visualization

* Plotly
* Matplotlib

### Frontend

* Streamlit

### Development

* Git
* GitHub

---

#  Future Improvements

* User Authentication
* Cloud Database (PostgreSQL)
* Automated Model Retraining
* User Goal Recommendations
* Personalized Study Plans
* Study Forecasting
* Mobile-Friendly Interface
* FastAPI Deployment

---

#  Author

**Smarth Sharma**


---

## ⭐ If you found this project interesting, consider starring the repository.
