"""
frontend/pages/3_Subject_Analysis.py
Per-subject performance: cards, pie, bar, scatter, table.
"""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / "backend"
FRONTEND_DIR = Path(__file__).resolve().parent.parent
for d in (str(BACKEND_DIR), str(FRONTEND_DIR)):
    if d not in sys.path:
        sys.path.insert(0, d)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in from the Home page first.")
    st.stop()
if "theme" not in st.session_state:
    st.session_state.theme = "light"

from utils.theme import inject_css, get_theme_colors, render_theme_toggle, score_badge, plotly_layout
inject_css()
c = get_theme_colors()

username = st.session_state.username

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""<div style="padding:0 0.5rem;">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.35rem;
                    font-weight:700; color:{c['text']};">🧠 StudyIntel</div>
        <div style="font-size:0.8rem; color:{c['text_muted']};">
            Hey, <b style="color:{c['primary']}">{username}</b> 👋
        </div></div>""", unsafe_allow_html=True)
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

from database.crud import get_logs_dataframe
from src.analytics.subject import get_subject_analytics

df = get_logs_dataframe(username)

st.markdown('<div class="page-title">📚 Subject <span class="accent">Analysis</span></div>', unsafe_allow_html=True)
st.markdown(f'<p class="page-subtitle">Per-subject performance breakdown.</p>', unsafe_allow_html=True)

if df.empty:
    st.info("No logs yet. Log some sessions to see subject breakdown!")
    st.stop()

data = get_subject_analytics(df)
breakdown = pd.DataFrame(data["subject_breakdown"]).sort_values("total_study_hours", ascending=False)

# Colour palette (not purple — teal + coral + mint family)
palette = [c["primary"], c["coral"], c["mint"], c["amber"],
           "#6366F1", "#EC4899", "#14B8A6", "#8B5CF6"]

# ── Subject cards ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Subject Overview</div>', unsafe_allow_html=True)

n = min(len(breakdown), 4)
cols = st.columns(n if n > 0 else 1)
for idx, (col, (_, row)) in enumerate(zip(cols, breakdown.iterrows())):
    pct = row.get("study_percentage", 0)
    avg_p = row.get("average_productivity_rating", 0)
    badge_cls, badge_lbl = score_badge(avg_p)
    clr = palette[idx % len(palette)]
    with col:
        st.markdown(f"""
        <div class="subj-card" style="border-top: 3px solid {clr};">
            <div class="subj-name">{row['subject']}</div>
            <div class="subj-score" style="color:{clr};">{avg_p:.1f}<span style="font-size:0.9rem; color:{c['text_sub']};">/10</span></div>
            <div class="subj-stat">{row['total_study_hours']:.1f}h total · {pct:.0f}% share</div>
            <div class="subj-stat">{int(row['total_study_sessions'])} sessions</div>
            <div style="margin-top:0.7rem;"><span class="{badge_cls}">{badge_lbl}</span></div>
        </div>
        """, unsafe_allow_html=True)

# second row if more than 4 subjects
if len(breakdown) > 4:
    extra = breakdown.iloc[4:]
    e_cols = st.columns(min(len(extra), 4))
    for idx, (col, (_, row)) in enumerate(zip(e_cols, extra.iterrows())):
        pct = row.get("study_percentage", 0)
        avg_p = row.get("average_productivity_rating", 0)
        badge_cls, badge_lbl = score_badge(avg_p)
        clr = palette[(idx + 4) % len(palette)]
        with col:
            st.markdown(f"""
            <div class="subj-card" style="border-top:3px solid {clr};">
                <div class="subj-name">{row['subject']}</div>
                <div class="subj-score" style="color:{clr};">{avg_p:.1f}<span style="font-size:0.9rem; color:{c['text_sub']};">/10</span></div>
                <div class="subj-stat">{row['total_study_hours']:.1f}h · {pct:.0f}%</div>
                <div style="margin-top:0.6rem;"><span class="{badge_cls}">{badge_lbl}</span></div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Pie + Bar ─────────────────────────────────────────────────────────────────
col_pie, col_bar = st.columns(2)

with col_pie:
    st.markdown('<div class="section-header">Time Allocation</div>', unsafe_allow_html=True)
    fig_pie = go.Figure(go.Pie(
        labels=breakdown["subject"],
        values=breakdown["total_study_hours"],
        hole=0.6,
        marker=dict(
            colors=palette[:len(breakdown)],
            line=dict(color=c["bg"], width=3),
        ),
        textinfo="label+percent",
        textfont=dict(color=c["text"], size=11),
        hovertemplate="<b>%{label}</b><br>%{value:.1f}h (%{percent})<extra></extra>",
    ))
    fig_pie.add_annotation(
        text=f"<b>{df['study_hours'].sum():.0f}h</b><br>Total",
        x=0.5, y=0.5, showarrow=False,
        font=dict(color=c["text"], size=13, family="Space Grotesk"),
    )
    lay_p = plotly_layout(c, height=300)
    lay_p["showlegend"] = False
    lay_p["margin"] = dict(l=10,r=10,t=10,b=10)
    fig_pie.update_layout(**lay_p)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_bar:
    st.markdown('<div class="section-header">Avg Productivity by Subject</div>', unsafe_allow_html=True)
    sb = breakdown.sort_values("average_productivity_rating", ascending=True)
    bar_colors = [
        c["mint"] if p >= 7.5 else c["amber"] if p >= 5 else c["red"]
        for p in sb["average_productivity_rating"]
    ]
    fig_bar = go.Figure(go.Bar(
        x=sb["average_productivity_rating"], y=sb["subject"],
        orientation="h",
        marker=dict(color=bar_colors, opacity=0.85, line=dict(width=0), cornerradius=8),
        text=[f"{p:.1f}" for p in sb["average_productivity_rating"]],
        textposition="outside",
        textfont=dict(color=c["text_muted"], size=11),
        hovertemplate="<b>%{y}</b><br>Avg: %{x:.1f}/10<extra></extra>",
    ))
    fig_bar.add_vline(x=5,   line_dash="dash", line_color=c["red"],  line_width=1, opacity=0.4)
    fig_bar.add_vline(x=7.5, line_dash="dash", line_color=c["mint"], line_width=1, opacity=0.4)
    lay_b = plotly_layout(c, height=300)
    lay_b["margin"] = dict(l=8,r=8,t=10,b=8)
    lay_b["xaxis"]["range"] = [0, 10.5]
    lay_b["yaxis"]["tickfont"] = dict(color=c["text"], size=12)
    fig_bar.update_layout(**lay_b)
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Scatter ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Task Difficulty vs Productivity (by Subject)</div>', unsafe_allow_html=True)
sc_df = df.dropna(subset=["task_difficulty","productivity_rating"])
fig_s = px.scatter(
    sc_df, x="task_difficulty", y="productivity_rating",
    color="subject", size="study_hours",
    color_discrete_sequence=palette,
    labels={"task_difficulty":"Task Difficulty (1-5)","productivity_rating":"Productivity (1-10)"},
    hover_data=["date","study_hours","mood_score"],
)
fig_s.update_traces(marker=dict(opacity=0.8, line=dict(width=0.5, color=c["bg"])))
lay_s = plotly_layout(c, height=300)
lay_s["margin"] = dict(l=8,r=8,t=10,b=8)
lay_s["legend"] = dict(font=dict(color=c["text_muted"]), bgcolor="rgba(0,0,0,0)")
fig_s.update_layout(**lay_s)
st.plotly_chart(fig_s, use_container_width=True)

# ── Table ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Full Subject Table</div>', unsafe_allow_html=True)
disp = breakdown.copy()
disp.columns = ["Subject","Study Hrs","Avg Productivity","Avg Difficulty","Sessions","Study %"]
for col in ["Study Hrs","Avg Productivity","Avg Difficulty","Study %"]:
    disp[col] = disp[col].round(1)
st.dataframe(disp, use_container_width=True, hide_index=True,
    column_config={
        "Avg Productivity": st.column_config.ProgressColumn("Avg Productivity", min_value=0, max_value=10, format="%.1f"),
        "Study %": st.column_config.ProgressColumn("Study %", min_value=0, max_value=100, format="%.0f%%"),
    })
