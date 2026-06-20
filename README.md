# StudyIntel

Machine Learning-powered Study Intelligence Platform that helps students analyze study habits, discover productivity patterns, and predict future productivity using analytics and explainable machine learning.

---

## Overview

StudyIntel is an end-to-end data analytics and machine learning project designed to help students understand how their daily habits affect productivity.

The platform combines:

* Study Tracking
* Analytics & Insights
* Productivity Prediction
* Explainable AI (SHAP)
* Personalized Learning Analytics

---

## Features

### Study Logging

* Daily Study Tracking
* Multi-Subject Study Entries
* Data Validation System
* SQLite Database Storage
* CSV Data Export

### Analytics Engine

* Daily Analytics
* Weekly Analytics
* Monthly Analytics
* Subject Analytics
* Study Streak Analysis
* Consistency Tracking
* Productivity Trends
* Habit Monitoring

### Machine Learning

* Productivity Score Prediction
* Feature Engineering Pipeline
* Model Benchmarking
* Hyperparameter Tuning
* Explainable AI (Upcoming)

---

## Project Architecture

```text
User Input
     ↓
Validation Layer
     ↓
SQLite Database
     ↓
Analytics Engine
     ↓
Machine Learning Engine
     ↓
Prediction & Insights
```

---

## Current Progress

### Data Layer

* Study Log Schema Design
* Validation Rules
* CSV Logging System
* Data Loading Pipeline
* SQLite Database Integration
* CRUD Operations

### Analytics Engine

* Daily Analytics
* Weekly Analytics
* Monthly Analytics
* Subject Analytics
* Streak Analytics
* Date Aggregation Utilities
* Consistency Tracking

### Machine Learning Pipeline

* Exploratory Data Analysis (EDA)
* Synthetic Dataset Generation (18,000+ Records)
* Feature Engineering
* Data Preprocessing
* Train/Test Split
* Model Benchmarking
* Hyperparameter Optimization

---

## Dataset Features

### Raw Features

| Feature             | Description                |
| ------------------- | -------------------------- |
| Date                | Study date                 |
| Sleep Hours         | Hours slept                |
| Study Hours         | Hours studied              |
| Screen Time         | Daily screen usage         |
| Exercise Minutes    | Exercise duration          |
| Mood Score          | Self-reported mood         |
| Energy Level        | Self-reported energy       |
| Task Difficulty     | Perceived difficulty       |
| Study Sessions      | Number of sessions         |
| Distractions        | Number of distractions     |
| Goal Completion     | Goal completion percentage |
| Subject             | Subject studied            |
| Productivity Rating | Target variable            |

---

### Engineered Features

* Study Efficiency
* Distraction Rate
* Screen-to-Study Ratio
* Wellness Score
* Goal Efficiency
* Optimal Sleep Flag
* Weekend Indicator
* Exam Season Indicator
* Day of Week
* Month

---

## Model Benchmarking

| Model         | R² Score   | RMSE       |
| ------------- | ---------- | ---------- |
| Random Forest | 0.8753     | 0.5647     |
| XGBoost       | 0.8786     | 0.5572     |
| LightGBM      | 0.8796     | 0.5548     |
| CatBoost      | **0.8879** | **0.5355** |

### Selected Model

**CatBoost Regressor**

Performance:

* R² Score: **0.8879**
* RMSE: **0.5355**

CatBoost achieved the strongest overall performance and was selected as the production model for StudyIntel v1.

---

## Technology Stack

### Backend

* Python
* Pandas
* NumPy
* SQLite

### Machine Learning

* Scikit-Learn
* CatBoost
* LightGBM
* XGBoost

### Visualization

* Matplotlib
* Seaborn

### Frontend (Planned)

* Streamlit

---

## Roadmap

### Version 1.0

* Analytics Dashboard
* Productivity Prediction
* SQLite Integration
* Model Deployment
* SHAP Explainability

### Version 1.1

* Personalized Analytics
* User History Tracking
* Enhanced Dashboard Visualizations

### Version 1.2

* Productivity Classification Models
* Goal Achievement Prediction
* Burnout Risk Detection
* Advanced Recommendation System

---

## Project Status

**Current Phase:** Analytics Engine Complete ✅

### Completed

* Data Pipeline
* Database Layer
* Analytics Engine
* Regression Model Selection

### In Progress

* Model Persistence
* Prediction Module
* SHAP Explainability
* Streamlit Dashboard

---

Built as a portfolio project focused on Data Analytics, Machine Learning Engineering, and Explainable AI.
