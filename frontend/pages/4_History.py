"""
frontend/pages/4_History.py
Filterable study log table with CSV export.
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

if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in from the Home page first.")
    st.stop()
if "theme" not in st.session_state:
    st.session_state.theme = "light"

from utils.theme import inject_css, get_theme_colors, render_theme_toggle
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

df = get_logs_dataframe(username)

st.markdown('<div class="page-title">📋 Study Log <span class="accent">History</span></div>', unsafe_allow_html=True)
st.markdown(f'<p class="page-subtitle">All sessions for {username} — filter, sort, and export.</p>', unsafe_allow_html=True)

if df.empty:
    st.markdown(f"""
    <div class="clay-card" style="text-align:center; padding:3rem;">
        <div style="font-size:3rem; margin-bottom:1rem;">📋</div>
        <div style="font-weight:600; color:{c['text']}; font-size:1.1rem;">No logs yet</div>
        <div style="color:{c['text_muted']}; margin-top:0.4rem;">Add your first session from <b>Log Study Session</b>.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Filters ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

with f1:
    subjects = ["All"] + sorted(df["subject"].unique().tolist())
    sel_sub = st.selectbox("Subject", subjects)

with f2:
    df["date"] = pd.to_datetime(df["date"])
    min_d, max_d = df["date"].min().date(), df["date"].max().date()
    date_range = st.date_input("Date Range", value=(min_d, max_d),
                                min_value=min_d, max_value=max_d)

with f3:
    prod_filter = st.slider("Productivity", 1, 10,
                             (int(df["productivity_rating"].min()),
                              int(df["productivity_rating"].max())))

with f4:
    sort_col = st.selectbox("Sort by", ["date","productivity_rating","study_hours","mood_score"])
    sort_asc = st.checkbox("Ascending", value=False)

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = df.copy()
if sel_sub != "All":
    filtered = filtered[filtered["subject"] == sel_sub]
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    s_d, e_d = date_range
    filtered = filtered[(filtered["date"].dt.date >= s_d) & (filtered["date"].dt.date <= e_d)]
filtered = filtered[
    (filtered["productivity_rating"] >= prod_filter[0]) &
    (filtered["productivity_rating"] <= prod_filter[1])
]
filtered = filtered.sort_values(sort_col, ascending=sort_asc)

# ── Result bar ────────────────────────────────────────────────────────────────
rc, ec = st.columns([3, 1])
with rc:
    st.markdown(f'<p style="color:{c["text_muted"]}; font-size:0.88rem; margin-top:0.8rem;">Showing <b style="color:{c["primary"]}">{len(filtered)}</b> of {len(df)} logs</p>', unsafe_allow_html=True)
with ec:
    csv = filtered.drop(columns=["id","username"], errors="ignore").to_csv(index=False)
    st.download_button("⬇ Export CSV", data=csv,
        file_name=f"studyintel_{username}.csv", mime="text/csv",
        use_container_width=True)

# ── Table ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Log Table</div>', unsafe_allow_html=True)

disp = filtered.drop(columns=["id","username"], errors="ignore").copy()
disp["date"] = disp["date"].dt.strftime("%Y-%m-%d")

priority = ["date","subject","productivity_rating","study_hours","sleep_hours",
            "mood_score","energy_level","goal_completion","distractions",
            "study_sessions","exercise_minutes","screen_time","task_difficulty"]
other = [col for col in disp.columns if col not in priority]
disp = disp[priority + other]

st.dataframe(
    disp, use_container_width=True, hide_index=True,
    height=min(580, 40 + 35 * len(disp)),
    column_config={
        "productivity_rating": st.column_config.ProgressColumn("Productivity", min_value=0, max_value=10, format="%.0f"),
        "mood_score":          st.column_config.ProgressColumn("Mood",         min_value=0, max_value=10, format="%.0f"),
        "energy_level":        st.column_config.ProgressColumn("Energy",       min_value=0, max_value=10, format="%.0f"),
        "goal_completion":     st.column_config.ProgressColumn("Goal %",       min_value=0, max_value=100, format="%.0f%%"),
        "study_hours":         st.column_config.NumberColumn("Study Hrs",  format="%.1f"),
        "sleep_hours":         st.column_config.NumberColumn("Sleep Hrs",  format="%.1f"),
        "screen_time":         st.column_config.NumberColumn("Screen Hrs", format="%.1f"),
    }
)

# ── Summary stats ─────────────────────────────────────────────────────────────
if not filtered.empty:
    st.markdown('<div class="section-header">Summary for Selection</div>', unsafe_allow_html=True)
    s1, s2, s3, s4, s5 = st.columns(5)
    for col, lbl, val in [
        (s1, "Avg Productivity",    f"{filtered['productivity_rating'].mean():.1f}"),
        (s2, "Total Study Hrs",     f"{filtered['study_hours'].sum():.1f}h"),
        (s3, "Avg Sleep",           f"{filtered['sleep_hours'].mean():.1f}h"),
        (s4, "Avg Mood",            f"{filtered['mood_score'].mean():.1f}"),
        (s5, "Total Distractions",  str(int(filtered['distractions'].sum()))),
    ]:
        with col:
            st.markdown(f"""
            <div class="clay-metric">
                <div class="metric-label">{lbl}</div>
                <div class="metric-value" style="font-size:1.5rem;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
