"""
frontend/app.py — StudyIntel entry point.
Run: python -m streamlit run frontend/app.py
"""

import sys
from pathlib import Path

BACKEND_DIR  = Path(__file__).resolve().parent.parent / "backend"
FRONTEND_DIR = Path(__file__).resolve().parent
for d in (str(BACKEND_DIR), str(FRONTEND_DIR)):
    if d not in sys.path:
        sys.path.insert(0, d)

import streamlit as st

st.set_page_config(
    page_title="StudyIntel",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Defaults ──────────────────────────────────────────────────────────────────
if "theme"       not in st.session_state: st.session_state.theme       = "light"
if "username"    not in st.session_state: st.session_state.username    = None
if "splash_done" not in st.session_state: st.session_state.splash_done = False

from utils.theme import inject_css, get_theme_colors, render_theme_toggle
inject_css()
c = get_theme_colors()

import time
if not st.session_state.splash_done:
    st.markdown(f"""
    <div class="splash-container">
        <div class="splash-logo">🧠</div>
        <div class="splash-title">StudyIntel</div>
        <div class="splash-subtitle">Initialising AI engines...</div>
        <div class="splash-loader">
            <div class="splash-loader-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2.2)
    st.session_state.splash_done = True
    st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# LOGIN SCREEN
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.username is None:
    _, mid, _ = st.columns([1, 1.3, 1])
    with mid:
        # ── Animated brand ────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="text-align:center; margin-top:3.5rem; margin-bottom:0.5rem;">
            <div style="font-size:4.5rem; animation:floatBob 3s ease-in-out infinite;
                        display:inline-block; margin-bottom:0.7rem;">🧠</div>
            <div style="font-family:'Space Grotesk',sans-serif; font-size:2.5rem;
                        font-weight:700; color:{c['text']}; letter-spacing:-0.03em;">
                StudyIntel
            </div>
            <div style="font-size:0.92rem; color:{c['text_muted']};
                        margin-top:0.3rem; margin-bottom:2.4rem;">
                AI-powered study productivity tracker
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Username input (single box) ───────────────────────────────────────
        st.markdown(
            f"<p style='color:{c['text']}; font-weight:600; font-size:0.95rem;"
            f" margin-bottom:0.3rem;'>Enter your username</p>",
            unsafe_allow_html=True,
        )
        username_input = st.text_input(
            "username",
            label_visibility="collapsed",
            placeholder="e.g. alex_k, jess42, study_ninja",
            key="login_input",
        )
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        # ── Continue button ───────────────────────────────────────────────────
        if st.button("Continue →", use_container_width=True, key="login_btn"):
            uname = username_input.strip()
            if len(uname) < 2:
                st.error("Username must be at least 2 characters.")
            else:
                st.session_state.username = uname
                st.rerun()

        # ── Feature pills ─────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="display:flex; gap:0.7rem; justify-content:center;
                    flex-wrap:wrap; margin-top:1.8rem;
                    animation:fadeSlideUp 0.55s ease 0.25s both;">
            <span style="background:{c['primary_soft']}; color:{c['primary']};
                border:1px solid {c['primary']}; border-radius:20px;
                padding:0.3rem 0.9rem; font-size:0.78rem; font-weight:600;">
                🤖 AI Prediction
            </span>
            <span style="background:{c['coral_soft']}; color:{c['coral']};
                border:1px solid {c['coral']}; border-radius:20px;
                padding:0.3rem 0.9rem; font-size:0.78rem; font-weight:600;">
                📊 Live Analytics
            </span>
            <span style="background:{c['mint_soft']}; color:{c['mint']};
                border:1px solid {c['mint']}; border-radius:20px;
                padding:0.3rem 0.9rem; font-size:0.78rem; font-weight:600;">
                🔍 SHAP Insights
            </span>
        </div>
        <p style="text-align:center; color:{c['text_sub']}; font-size:0.76rem;
                  margin-top:1.4rem;">
            No password needed — username keeps your data separate
        </p>
        """, unsafe_allow_html=True)

        # ── Theme toggle ──────────────────────────────────────────────────────
        st.markdown("<div style='margin-top:1.5rem;'>", unsafe_allow_html=True)
        render_theme_toggle()
        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR (authenticated)
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding:0 0.5rem;">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.35rem;
                    font-weight:700; color:{c['text']}; margin-bottom:0.2rem;">
            🧠 StudyIntel
        </div>
        <div style="font-size:0.8rem; color:{c['text_muted']};">
            Hey, <b style="color:{c['primary']}">{st.session_state.username}</b> 👋
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown(
        f"<p style='color:{c['text_sub']}; font-size:0.72rem; font-weight:600;"
        f" text-transform:uppercase; letter-spacing:0.1em;"
        f" margin:0 0 0.5rem 0.5rem;'>Navigation</p>",
        unsafe_allow_html=True,
    )
    st.page_link("app.py",                         label="🏠  Home")
    st.page_link("pages/1_Log_Study.py",            label="📝  Log Study Session")
    st.page_link("pages/2_Dashboard.py",            label="📊  Dashboard")
    st.page_link("pages/3_Subject_Analysis.py",     label="📚  Subject Analysis")
    st.page_link("pages/4_History.py",              label="📋  History")
    st.divider()
    render_theme_toggle()
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    if st.button("🚪  Sign Out", use_container_width=True, key="signout_btn"):
        st.session_state.username = None
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# HOME CONTENT
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="page-title">Welcome back, '
    f'<span class="accent">{st.session_state.username}</span> 👋</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="page-subtitle">Here\'s a snapshot of your study progress.</p>',
    unsafe_allow_html=True,
)

try:
    from database.crud import get_logs_dataframe
    from src.analytics.streaks import get_streak_summary

    df = get_logs_dataframe(st.session_state.username)

    if df.empty:
        st.markdown(f"""
        <div class="clay-card" style="text-align:center; padding:3rem 2rem;">
            <div style="font-size:3.5rem; margin-bottom:1rem;">📝</div>
            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.2rem;
                        font-weight:600; color:{c['text']}; margin-bottom:0.5rem;">
                No study logs yet
            </div>
            <div style="color:{c['text_muted']}; font-size:0.9rem;">
                Head to <b>Log Study Session</b> to record your first session!
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        streak = get_streak_summary(df)
        st.markdown('<div class="section-header">Quick Stats</div>',
                    unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        for col, label, val, sub in [
            (c1, "Total Logs",       str(len(df)),                              "sessions recorded"),
            (c2, "Current Streak",   f"{streak['current_streak']}d",            "days in a row"),
            (c3, "Avg Productivity", f"{df['productivity_rating'].mean():.1f}", "out of 10"),
            (c4, "Total Study",      f"{df['study_hours'].sum():.0f}h",         "all-time hours"),
        ]:
            with col:
                st.markdown(f"""
                <div class="clay-metric">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{val}</div>
                    <div class="metric-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">🔥 Study Activity (Streak Grid)</div>', unsafe_allow_html=True)
        from utils.theme import render_github_contribution_graph
        st.html(render_github_contribution_graph(df, c))
        st.success("Use the sidebar to navigate. Head to 📊 **Dashboard** for full charts!")

except Exception as e:
    st.warning(f"Could not load stats: {e}")
