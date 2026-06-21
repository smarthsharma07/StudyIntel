# StudyIntel

Machine Learning-powered Study Intelligence Platform that helps students analyze study habits, discover productivity patterns, and predict future productivity using analytics and explainable machine learning.

---

## Overview

StudyIntel is an end-to-end Data Analytics and Machine Learning project designed to help students understand how daily habits influence productivity.

The platform combines:

* Study Tracking
* Learning Analytics
* Productivity Prediction
* Explainable AI (SHAP)
* Habit Monitoring
* Personalized Insights

---

## Features

### Study Logging

* Daily Study Tracking
* Multi-Subject Study Entries
* Input Validation System
* SQLite Database Storage
* CSV Data Export

### Analytics Engine

* Daily Analytics
* Weekly Analytics
* Monthly Analytics
* Subject Analytics
* Study Streak Tracking
* Consistency Analysis
* Productivity Trends
* Habit Monitoring

### Machine Learning

* Productivity Score Prediction
* Feature Engineering Pipeline
* Model Benchmarking
* Hyperparameter Optimization
* Model Persistence
* Inference Pipeline
* SHAP Explainability

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
Feature Engineering
     ↓
CatBoost Model
     ↓
Prediction & SHAP Insights
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
* Model Persistence
* Prediction Pipeline
* SHAP Explainability

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
* Study-to-Sleep Ratio
* Exercise-to-Study Ratio
* Sessions per Hour
* Average Session Length

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

The production model uses CatBoost's native categorical feature handling and supports end-to-end inference without manual categorical encoding.

---

## Explainable AI (SHAP)

StudyIntel includes SHAP-based explainability to provide transparent productivity predictions.

Features:

* Local Prediction Explanations
* Feature Contribution Analysis
* Positive Productivity Drivers
* Negative Productivity Drivers
* SHAP Validation Across Multiple Productivity Scenarios

Example Insights:

```text
Predicted Productivity: 7.61

Top Positive Factors
+ Optimal Sleep
+ Low Distractions
+ Task Difficulty

Top Negative Factors
- Low Energy Level
- Low Mood Score
- Low Goal Completion
```

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
* SHAP

### Visualization

* Matplotlib
* Seaborn

### Frontend (Planned)

* Streamlit

---

## Dataset Notice

StudyIntel v1 uses a synthetic dataset generated from realistic study-behavior patterns to design, validate, and benchmark the analytics and machine learning pipeline.

Future versions will incorporate real user study logs collected through the platform, enabling periodic retraining and improved prediction quality.

---

## Roadmap

### Version 1.0

* Analytics Dashboard
* Productivity Prediction
* SQLite Integration
* SHAP Explainability
* Streamlit Dashboard
* Model Deployment

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

**Current Phase:** Explainability & Dashboard Development 🚧

### Completed

* Data Pipeline
* Database Layer
* Analytics Engine
* Feature Engineering
* Model Benchmarking
* CatBoost Model Selection
* Model Persistence
* Prediction Pipeline
* SHAP Explainability Module

### In Progress

* SHAP Visualizations
* Streamlit Dashboard
* Deployment

---

Built as a portfolio project focused on Data Analytics, Machine Learning Engineering, and Explainable AI.
