"""
frontend/pages/2_Dashboard.py
Analytics dashboard: trends, wellness, distribution, monthly table.
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
from plotly.subplots import make_subplots

if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in from the Home page first.")
    st.stop()
if "theme" not in st.session_state:
    st.session_state.theme = "light"

from utils.theme import inject_css, get_theme_colors, render_theme_toggle, plotly_layout, hex_to_rgba
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

# ── Load data ─────────────────────────────────────────────────────────────────
from database.crud import get_logs_dataframe
from src.analytics.streaks import get_streak_summary
from src.analytics.weekly import get_weekly_summary
from src.utils.aggregation import get_daily_aggregated
from src.utils.date_utils import fill_missing_dates

df = get_logs_dataframe(username)

st.markdown('<div class="page-title">📊 <span class="accent">Dashboard</span></div>', unsafe_allow_html=True)
st.markdown(f'<p class="page-subtitle">Your complete study analytics, {username}.</p>', unsafe_allow_html=True)

if df.empty:
    st.markdown(f"""
    <div class="clay-card" style="text-align:center; padding:3rem;">
        <div style="font-size:3rem; margin-bottom:1rem;">📊</div>
        <div style="font-weight:600; color:{c['text']}; font-size:1.1rem;">No data yet</div>
        <div style="color:{c['text_muted']}; margin-top:0.4rem;">Log your first session to see your dashboard.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── KPI Row ───────────────────────────────────────────────────────────────────
weekly = get_weekly_summary(df) or {}
streak = get_streak_summary(df)

k1,k2,k3,k4,k5,k6 = st.columns(6)
kpis = [
    (k1, "🔥 Streak",       f"{streak['current_streak']}d",                 "current"),
    (k2, "🏆 Best Streak",  f"{streak['longest_streak']}d",                 "all-time"),
    (k3, "📚 This Week",    f"{weekly.get('total_study_hours',0):.1f}h",    "study hours"),
    (k4, "✅ Consistency",  f"{streak.get('consistency_score',0):.0f}%",    "days active"),
    (k5, "⭐ Avg Score",    f"{df['productivity_rating'].mean():.1f}",      "out of 10"),
    (k6, "⏳ All-time",     f"{df['study_hours'].sum():.0f}h",              "total studied"),
]
for col, lbl, val, sub in kpis:
    with col:
        st.markdown(f"""
        <div class="clay-metric">
            <div class="metric-label">{lbl}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">🔥 Study Activity (Streak Grid)</div>', unsafe_allow_html=True)
from utils.theme import render_github_contribution_graph
st.html(render_github_contribution_graph(df, c))

# ── Timeline ──────────────────────────────────────────────────────────────────
daily_df = get_daily_aggregated(df)
daily_df = fill_missing_dates(daily_df)
daily_df["date"] = pd.to_datetime(daily_df["date"])
daily_df = daily_df.sort_values("date")

st.markdown('<div class="section-header">📈 Study & Productivity Timeline</div>', unsafe_allow_html=True)
range_map = {"Last 30 Days": 30, "Last 60 Days": 60, "Last 90 Days": 90, "All Time": None}
sel = st.radio("Range", list(range_map.keys()), horizontal=True, index=0, label_visibility="collapsed")
plot_df = daily_df.tail(range_map[sel]) if range_map[sel] else daily_df

fig_t = make_subplots(specs=[[{"secondary_y": True}]])
fig_t.add_trace(go.Bar(
    x=plot_df["date"], y=plot_df["study_hours"], name="Study Hours",
    marker=dict(
        color=plot_df["study_hours"],
        colorscale=[[0, c["primary_soft"]], [1, c["primary"]]],
        showscale=False, opacity=0.85,
        cornerradius=8,
    ),
    hovertemplate="<b>%{x|%b %d}</b><br>Study: %{y:.1f}h<extra></extra>",
), secondary_y=False)
fig_t.add_trace(go.Scatter(
    x=plot_df["date"],
    y=plot_df["productivity_rating"].where(plot_df["productivity_rating"] > 0),
    name="Productivity", mode="lines+markers",
    line=dict(color=c["coral"], width=2.5, shape="spline", smoothing=0.7),
    marker=dict(size=5, color=c["coral"]),
    hovertemplate="<b>%{x|%b %d}</b><br>Productivity: %{y:.1f}/10<extra></extra>",
), secondary_y=True)

lay = plotly_layout(c, height=330)
lay["legend"] = dict(orientation="h", x=0, y=1.12, font=dict(color=c["text_muted"], size=11))
lay["hovermode"] = "x unified"
lay["margin"] = dict(l=8, r=8, t=10, b=8)
fig_t.update_layout(**lay)
fig_t.update_yaxes(title_text="Study Hours", secondary_y=False,
    gridcolor=c["border"], tickfont=dict(color=c["text_sub"]))
fig_t.update_yaxes(title_text="Productivity (1-10)", secondary_y=True,
    range=[0,10], tickfont=dict(color=c["text_sub"]), gridcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_t, use_container_width=True)

# ── Two column charts ─────────────────────────────────────────────────────────
cl, cr = st.columns(2)

with cl:
    st.markdown('<div class="section-header">💪 Wellness Indicators (7-day avg)</div>', unsafe_allow_html=True)
    w = plot_df.copy()
    w["sleep_7"] = w["sleep_hours"].rolling(7, min_periods=1).mean()
    w["mood_7"]  = w["mood_score"].rolling(7, min_periods=1).mean()
    w["nrgy_7"]  = w["energy_level"].rolling(7, min_periods=1).mean()
    fig_well = go.Figure()
    for col_name, label, clr in [
        ("sleep_7","Sleep (h)", c["primary"]),
        ("mood_7", "Mood /10",  c["coral"]),
        ("nrgy_7", "Energy /10",c["mint"]),
    ]:
        fig_well.add_trace(go.Scatter(
            x=w["date"], y=w[col_name], name=label,
            mode="lines", line=dict(color=clr, width=2.2, shape="spline", smoothing=0.7),
            fill="tozeroy",
            fillcolor=hex_to_rgba(clr, 0.08),
        ))
    lay_w = plotly_layout(c, height=280)
    lay_w["legend"] = dict(orientation="h", x=0, y=1.15, font=dict(color=c["text_muted"],size=11))
    lay_w["hovermode"] = "x unified"
    lay_w["margin"] = dict(l=8,r=8,t=10,b=8)
    fig_well.update_layout(**lay_w)
    st.plotly_chart(fig_well, use_container_width=True)

with cr:
    st.markdown('<div class="section-header">📊 Productivity Distribution</div>', unsafe_allow_html=True)
    prod = df["productivity_rating"].dropna()
    bar_colors = []
    for v in sorted(prod.unique()):
        if v >= 7.5:   bar_colors.append(c["mint"])
        elif v >= 5.0: bar_colors.append(c["amber"])
        else:          bar_colors.append(c["red"])

    fig_dist = go.Figure(go.Histogram(
        x=prod, nbinsx=10,
        marker=dict(
            colorscale=[[0, c["red"]], [0.5, c["amber"]], [1, c["mint"]]],
            color=prod,
            opacity=0.85,
            line=dict(width=0.5, color=c["bg"]),
            cornerradius=8,
        ),
        hovertemplate="Score %{x}: %{y} entries<extra></extra>",
    ))
    fig_dist.add_vline(x=prod.mean(), line_dash="dash",
        line_color=c["primary"], line_width=2,
        annotation_text=f"  avg {prod.mean():.1f}",
        annotation_font=dict(color=c["primary"], size=11))
    lay_d = plotly_layout(c, height=280)
    lay_d["margin"] = dict(l=8,r=8,t=10,b=8)
    lay_d["xaxis"]["title"] = "Productivity Score"
    lay_d["yaxis"]["title"] = "Days"
    fig_dist.update_layout(**lay_d)
    st.plotly_chart(fig_dist, use_container_width=True)

# ── Scatter ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🖥 Screen Time vs Productivity</div>', unsafe_allow_html=True)
sc_df = df.dropna(subset=["screen_time","productivity_rating"])
fig_sc = px.scatter(
    sc_df, x="screen_time", y="productivity_rating",
    color="mood_score", size="study_hours",
    color_continuous_scale=[[0, c["red"]], [0.5, c["amber"]], [1, c["mint"]]],
    labels={"screen_time":"Screen Time (hrs)","productivity_rating":"Productivity","mood_score":"Mood"},
    hover_data=["date","subject","study_hours"],
)
sc_df_lay = plotly_layout(c, height=310)
sc_df_lay["margin"] = dict(l=8,r=8,t=10,b=8)
fig_sc.update_layout(**sc_df_lay)
fig_sc.update_traces(marker=dict(opacity=0.78, line=dict(width=0.5, color=c["bg"])))
st.plotly_chart(fig_sc, use_container_width=True)

# ── Monthly table ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📆 Monthly Breakdown</div>', unsafe_allow_html=True)
mt = df.copy()
mt["month"] = pd.to_datetime(mt["date"]).dt.to_period("M")
tbl = mt.groupby("month").agg(
    total_hours=("study_hours","sum"),
    avg_prod=("productivity_rating","mean"),
    avg_mood=("mood_score","mean"),
    avg_sleep=("sleep_hours","mean"),
    sessions=("study_sessions","sum"),
    days=("date","nunique"),
).reset_index()
tbl.columns = ["Month","Study Hrs","Avg Productivity","Avg Mood","Avg Sleep","Sessions","Days Active"]
tbl["Month"] = tbl["Month"].astype(str)
for col in ["Study Hrs","Avg Productivity","Avg Mood","Avg Sleep"]:
    tbl[col] = tbl[col].round(1)

st.dataframe(tbl, use_container_width=True, hide_index=True,
    column_config={
        "Avg Productivity": st.column_config.ProgressColumn("Avg Productivity", min_value=0, max_value=10, format="%.1f"),
        "Avg Mood":         st.column_config.ProgressColumn("Avg Mood",         min_value=0, max_value=10, format="%.1f"),
    })
