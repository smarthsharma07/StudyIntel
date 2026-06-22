"""
frontend/pages/1_Log_Study.py
Log a study session → instant AI prediction → SHAP explanation.
"""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / "backend"
FRONTEND_DIR = Path(__file__).resolve().parent.parent
for d in (str(BACKEND_DIR), str(FRONTEND_DIR)):
    if d not in sys.path:
        sys.path.insert(0, d)

import streamlit as st
import plotly.graph_objects as go

if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in from the Home page first.")
    st.stop()
if "theme" not in st.session_state:
    st.session_state.theme = "light"

from utils.theme import inject_css, get_theme_colors, render_theme_toggle, score_color, score_badge, plotly_layout, hex_to_rgba
inject_css()
c = get_theme_colors()

username = st.session_state.username


def generate_insights_narrative(shap_data: dict) -> str:
    """
    Generate a friendly natural language narrative explaining the SHAP values.
    """
    pred = shap_data["prediction"]
    base = shap_data["base_value"]
    pos = shap_data["positive_factors"]
    neg = shap_data["negative_factors"]

    friendly_names = {
        "sleep_hours": "Sleep",
        "study_hours": "Study Time",
        "screen_time": "Screen Time",
        "exercise_minutes": "Exercise",
        "mood_score": "Mood",
        "energy_level": "Energy Level",
        "task_difficulty": "Task Difficulty",
        "study_sessions": "Study Sessions",
        "distractions": "Distractions",
        "goal_completion": "Goal Completion",
        "subject": "Subject",
        "distraction_rate": "Distraction Frequency",
        "screen_study_ratio": "Screen-to-Study Ratio",
        "wellness_score": "Overall Wellness",
        "study_efficiency": "Study Efficiency",
        "goal_efficiency": "Goal Efficiency",
        "average_session_length": "Average Session Length",
        "study_sleep_ratio": "Study-to-Sleep Ratio",
        "exercise_study_ratio": "Exercise-to-Study Ratio",
        "sessions_per_hour": "Sessions Per Hour",
        "optimal_sleep": "Optimal Sleep Flag",
    }

    pos_list = []
    for _, row in pos.iterrows():
        name = friendly_names.get(row['feature'], row['feature'])
        pos_list.append(f"**{name}** (added +{row['shap_value']:.2f})")

    neg_list = []
    for _, row in neg.iterrows():
        name = friendly_names.get(row['feature'], row['feature'])
        neg_list.append(f"**{name}** (deducted {row['shap_value']:.2f})")

    if pred >= 7.5:
        tone = "Awesome job! Your study routine today is highly optimized."
    elif pred >= 5.0:
        tone = "You are on track, but there is room for improvement."
    else:
        tone = "Today's session encountered some headwinds. Let's adjust."

    intro = f"{tone} The AI predicted a productivity score of **{pred:.1f}/10** (baseline average is **{base:.1f}**)."

    drivers = ""
    if pos_list:
        drivers += f" The key driver{'s' if len(pos_list)>1 else ''} boosting your score {'are' if len(pos_list)>1 else 'is'} {', '.join(pos_list[:2])}."
    if neg_list:
        drivers += f" Conversely, the main factor{'s' if len(neg_list)>1 else ''} dragging it down {'are' if len(neg_list)>1 else 'is'} {', '.join(neg_list[:2])}."

    recommendation = ""
    if not neg.empty:
        top_neg_feat = neg.iloc[0]['feature']
        tips = {
            "distractions": "try putting your phone in another room or blocking notifications during study blocks.",
            "sleep_hours": "aim to get 7-8 hours of sleep tonight to boost your cognitive performance tomorrow.",
            "screen_time": "try limiting your non-study screen time to under 2 hours daily.",
            "energy_level": "consider taking short active breaks or stretching if you feel low on energy.",
            "mood_score": "try starting your next session with a small win, or taking a few minutes to unwind before starting.",
            "task_difficulty": "consider breaking complex or difficult tasks into smaller, more manageable sub-tasks.",
            "goal_completion": "try setting smaller, more achievable micro-goals for your next study block.",
            "distraction_rate": "try using the Pomodoro technique to maintain high focus for shorter, uninterrupted periods.",
            "screen_study_ratio": "try replacing non-study screen time with physical activity or study-related reading.",
            "wellness_score": "prioritize balance today by sleeping early, exercising, or taking time for self-care."
        }
        tip = tips.get(top_neg_feat, f"focus on improving your **{friendly_names.get(top_neg_feat, top_neg_feat)}** metric.")
        recommendation = f"💡 **Actionable Tip**: To increase your productivity next time, {tip}"

    return f"{intro}\n\n{drivers}\n\n{recommendation}"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:0 0.5rem;">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.35rem;
                    font-weight:700; color:{c['text']};">🧠 StudyIntel</div>
        <div style="font-size:0.8rem; color:{c['text_muted']};">
            Hey, <b style="color:{c['primary']}">{username}</b> 👋
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py",                         label="🏠  Home")
    st.page_link("pages/1_Log_Study.py",            label="📝  Log Study Session")
    st.page_link("pages/2_Dashboard.py",            label="📊  Dashboard")
    st.page_link("pages/3_Subject_Analysis.py",     label="📚  Subject Analysis")
    st.page_link("pages/4_History.py",              label="📋  History")
    st.divider()
    render_theme_toggle()
    if st.button("🚪  Sign Out", use_container_width=True):
        st.session_state.username = None
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">📝 Log Study <span class="accent">Session</span></div>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Record your session metrics and receive an instant AI-powered productivity prediction.</p>', unsafe_allow_html=True)

import datetime

# ── Form ──────────────────────────────────────────────────────────────────────
with st.form("log_form", clear_on_submit=False):
    st.markdown('<div class="section-header">📅 Session Details</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        log_date = st.date_input("Date", value=datetime.date.today(),
                                  min_value=datetime.date(2020,1,1),
                                  max_value=datetime.date.today())
        subject = st.text_input("Subject", placeholder="Mathematics, DSA, Physics…",
                                 help="Any subject — even ones never seen by the model.")
        study_hours = st.number_input("⏱ Study Hours", 0.0, 18.0, 4.0, 0.5)
        study_sessions = st.number_input("🔁 Sessions", 1, 20, 3, 1)
        sleep_hours = st.number_input("😴 Sleep Hours (last night)", 2.0, 16.0, 7.0, 0.5)
        screen_time = st.number_input("📱 Screen Time (hrs, non-study)", 0.0, 18.0, 2.0, 0.5)

    with col_b:
        exercise_minutes = st.slider("🏃 Exercise (minutes)", 0, 180, 30, 5)
        mood_score       = st.slider("😊 Mood Score", 1, 10, 7)
        energy_level     = st.slider("⚡ Energy Level", 1, 10, 7)
        task_difficulty  = st.slider("🧩 Task Difficulty (1=easy, 5=hard)", 1, 5, 3)
        distractions     = st.number_input("😵 Distractions count", 0, 100, 3)
        goal_completion  = st.slider("🎯 Goal Completion (%)", 0.0, 100.0, 80.0, 5.0)

    st.markdown('<div class="section-header">🌟 Self-Assessment</div>', unsafe_allow_html=True)
    productivity_rating = st.slider(
        "Your self-rated productivity (stored as target, NOT fed to model)",
        1, 10, 7,
        help="This is what the AI was trained to predict. It's saved to the database but is never a model input — zero data leakage."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🚀  Submit & Get Prediction", use_container_width=True)

# ── Process ───────────────────────────────────────────────────────────────────
if submitted:
    subj = subject.strip()
    if not subj:
        st.error("Please enter a subject name.")
        st.stop()

    log_dict = {
        "date": str(log_date),
        "sleep_hours": float(sleep_hours),
        "study_hours": float(study_hours),
        "screen_time": float(screen_time),
        "exercise_minutes": int(exercise_minutes),
        "mood_score": int(mood_score),
        "energy_level": int(energy_level),
        "task_difficulty": int(task_difficulty),
        "study_sessions": int(study_sessions),
        "distractions": int(distractions),
        "goal_completion": float(goal_completion),
        "subject": subj,
        "productivity_rating": int(productivity_rating),
    }

    with st.spinner("Running AI pipeline…"):
        try:
            from src.services.pipeline import process_study_log
            result = process_study_log(username=username, study_log_dict=log_dict)
        except ValueError as ve:
            st.error(f"Validation error: {ve}")
            st.stop()
        except Exception as ex:
            st.error(f"Pipeline error: {ex}")
            st.exception(ex)
            st.stop()

    pred      = result["prediction"]
    shap_data = result["shap"]
    analytics = result["analytics"]

    sc = score_color(c, pred)
    badge_cls, badge_lbl = score_badge(pred)

    st.markdown("---")
    # ── Score + Gauge ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🎯 AI Prediction Result</div>', unsafe_allow_html=True)

    left, right = st.columns([1, 2])

    with left:
        st.markdown(f"""
        <div class="clay-card" style="text-align:center; padding:2.5rem 1.5rem;">
            <div style="font-size:0.75rem; font-weight:600; color:{c['text_muted']};
                        text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.8rem;">
                Predicted Score
            </div>
            <div class="score-big" style="color:{sc};">{pred:.1f}</div>
            <div style="font-size:0.9rem; color:{c['text_sub']}; margin-top:0.2rem;">/ 10</div>
            <div style="margin-top:0.9rem;">
                <span class="{badge_cls}">{"🔥" if pred>=7.5 else "📈" if pred>=5 else "💪"} {badge_lbl}</span>
            </div>
            <div style="font-size:0.75rem; color:{c['text_sub']}; margin-top:0.9rem;">
                Base avg: {shap_data['base_value']:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pred,
            number=dict(font=dict(color=sc, size=42, family="Space Grotesk"), suffix="/10"),
            gauge=dict(
                axis=dict(range=[0, 10], tickcolor=c["text_sub"],
                          tickfont=dict(color=c["text_sub"], size=10)),
                bar=dict(color=sc, thickness=0.28),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 5],    color=f"rgba(239,68,68,0.07)"),
                    dict(range=[5, 7.5],  color=f"rgba(245,158,11,0.07)"),
                    dict(range=[7.5, 10], color=f"rgba(16,185,129,0.07)"),
                ],
                threshold=dict(
                    line=dict(color=c["primary"], width=3),
                    thickness=0.85,
                    value=shap_data["base_value"],
                ),
            ),
        ))
        layout = plotly_layout(c, height=260)
        layout["margin"] = dict(l=20, r=20, t=30, b=10)
        fig_g.update_layout(**layout)
        st.plotly_chart(fig_g, use_container_width=True)

    # ── SHAP waterfall ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔍 Why This Score? (SHAP Explanation)</div>', unsafe_allow_html=True)

    narrative = generate_insights_narrative(shap_data)
    st.markdown(f"""
    <div class="clay-card" style="margin-bottom:1.5rem; border-left: 5px solid {c['primary']};">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.15rem; font-weight:700; color:{c['text']}; margin-bottom:0.6rem;">💡 StudyIntel AI Insights</div>
        <div style="font-size:0.92rem; color:{c['text']}; line-height:1.5;">
            {narrative}
        </div>
    </div>
    """, unsafe_allow_html=True)

    shap_df = shap_data["shap_dataframe"].copy()
    shap_df = shap_df.sort_values("shap_value", key=abs, ascending=True)

    colors = [c["mint"] if v >= 0 else c["red"] for v in shap_df["shap_value"]]

    fig_w = go.Figure(go.Bar(
        x=shap_df["shap_value"],
        y=shap_df["feature"],
        orientation="h",
        marker=dict(color=colors, opacity=0.85, line=dict(width=0), cornerradius=8),
        text=[f"{v:+.3f}" for v in shap_df["shap_value"]],
        textposition="outside",
        textfont=dict(color=c["text_muted"], size=10),
        hovertemplate="<b>%{y}</b><br>SHAP: %{x:+.3f}<extra></extra>",
    ))
    layout_w = plotly_layout(c, height=460)
    layout_w["title"] = dict(
        text=f"Feature contributions  ·  base = {shap_data['base_value']:.2f}",
        font=dict(color=c["text_muted"], size=12),
    )
    layout_w["xaxis"]["title"] = "SHAP value (impact on score)"
    layout_w["xaxis"]["title_font"] = dict(color=c["text_sub"])
    layout_w["margin"] = dict(l=10, r=10, t=50, b=10)
    fig_w.update_layout(**layout_w)
    st.plotly_chart(fig_w, use_container_width=True)

    # ── Factor cards ──────────────────────────────────────────────────────────
    pos_col, neg_col = st.columns(2)
    with pos_col:
        st.markdown(f"<p style='font-weight:600; color:{c['mint']}; margin-bottom:0.5rem;'>✅ Boosting your score</p>", unsafe_allow_html=True)
        for _, row in shap_data["positive_factors"].iterrows():
            st.markdown(
                f'<div class="shap-pos"><span><b>{row["feature"]}</b> = {row["value"]}</span>'
                f'<span style="color:{c["mint"]}; font-weight:700;">+{row["shap_value"]:.3f}</span></div>',
                unsafe_allow_html=True)

    with neg_col:
        st.markdown(f"<p style='font-weight:600; color:{c['red']}; margin-bottom:0.5rem;'>❌ Hurting your score</p>", unsafe_allow_html=True)
        for _, row in shap_data["negative_factors"].iterrows():
            st.markdown(
                f'<div class="shap-neg"><span><b>{row["feature"]}</b> = {row["value"]}</span>'
                f'<span style="color:{c["red"]}; font-weight:700;">{row["shap_value"]:.3f}</span></div>',
                unsafe_allow_html=True)

    # ── Today's summary metrics ───────────────────────────────────────────────
    daily = analytics.get("daily")
    if daily:
        st.markdown('<div class="section-header">📅 Today\'s Summary</div>', unsafe_allow_html=True)
        d1, d2, d3, d4, d5 = st.columns(5)
        for col, lbl, val in [
            (d1, "Study Hours",  f"{daily['total_study_hours']:.1f}h"),
            (d2, "Sleep",        f"{daily['average_sleep_hours']:.1f}h"),
            (d3, "Mood",         f"{daily['average_mood_score']:.0f}/10"),
            (d4, "Goal",         f"{daily['average_goal_completion']:.0f}%"),
            (d5, "Sessions",     str(daily["total_study_sessions"])),
        ]:
            with col:
                st.markdown(f"""
                <div class="clay-metric">
                    <div class="metric-label">{lbl}</div>
                    <div class="metric-value" style="font-size:1.6rem;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.success("Log saved! Head to **📊 Dashboard** to see your trends.")
