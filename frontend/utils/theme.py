"""
frontend/utils/theme.py
=======================
Claymorphism design system for StudyIntel.
Light + Dark themes with full Streamlit element overrides.
"""

import streamlit as st

# ── Colour tokens ─────────────────────────────────────────────────────────────
LIGHT = {
    "bg":           "#F0F4F8",
    "bg2":          "#E8EFF7",
    "surface":      "#FFFFFF",
    "surface2":     "#F7FAFC",
    "border":       "rgba(200,214,229,0.8)",
    "text":         "#1A202C",
    "text_muted":   "#718096",
    "text_sub":     "#A0AEC0",
    "primary":      "#0EA5E9",
    "primary_soft": "rgba(14,165,233,0.12)",
    "coral":        "#F97316",
    "coral_soft":   "rgba(249,115,22,0.12)",
    "mint":         "#10B981",
    "mint_soft":    "rgba(16,185,129,0.12)",
    "amber":        "#F59E0B",
    "red":          "#EF4444",
    "shadow_a":     "rgba(163,177,198,0.55)",
    "shadow_b":     "rgba(255,255,255,0.95)",
    "shadow_in":    "rgba(255,255,255,0.9)",
    "card_grad":    "linear-gradient(145deg, #FFFFFF 0%, #EEF4FB 100%)",
    "metric_grad":  "linear-gradient(145deg, #FFFFFF 0%, #E8F4FD 100%)",
    "sidebar_bg":   "#FFFFFF",
    "app_bg":       "#F0F4F8",
    "input_bg":     "#F7FAFC",
    "form_bg":      "#FFFFFF",
}

DARK = {
    "bg":           "#0D1117",
    "bg2":          "#161B22",
    "surface":      "#1C2333",
    "surface2":     "#21293A",
    "border":       "rgba(255,255,255,0.08)",
    "text":         "#E6EDF3",
    "text_muted":   "#8B949E",
    "text_sub":     "#6E7681",
    "primary":      "#38BDF8",
    "primary_soft": "rgba(56,189,248,0.12)",
    "coral":        "#FB923C",
    "coral_soft":   "rgba(251,146,60,0.12)",
    "mint":         "#34D399",
    "mint_soft":    "rgba(52,211,153,0.12)",
    "amber":        "#FBBF24",
    "red":          "#F87171",
    "shadow_a":     "rgba(0,0,0,0.55)",
    "shadow_b":     "rgba(255,255,255,0.03)",
    "shadow_in":    "rgba(255,255,255,0.04)",
    "card_grad":    "linear-gradient(145deg, #1C2333 0%, #161B22 100%)",
    "metric_grad":  "linear-gradient(145deg, #1E2A3A 0%, #141C28 100%)",
    "sidebar_bg":   "#161B22",
    "app_bg":       "#0D1117",
    "input_bg":     "#21293A",
    "form_bg":      "#161B22",
}


def get_theme_colors():
    if st.session_state.get("theme", "light") == "dark":
        return DARK
    else:
        return LIGHT


def _dark_overrides(c: dict) -> str:
    """
    Comprehensive CSS that overrides every Streamlit native element for dark mode.
    This is the section that was missing before — without it dark mode only
    changed our custom .clay-* classes but left Streamlit's own elements white.
    """
    return f"""
/* ═══ DARK MODE — Full Streamlit override ═══ */

/* App shell */
.stApp {{
    background-color: {c['app_bg']} !important;
    background: {c['app_bg']} !important;
}}
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
.main {{
    background-color: {c['app_bg']} !important;
}}
.block-container {{
    background-color: transparent !important;
}}

/* Header bar */
[data-testid="stHeader"] {{
    background-color: transparent !important;
    background: transparent !important;
    border-bottom: none !important;
}}

/* Sidebar */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div:first-child {{
    background-color: {c['sidebar_bg']} !important;
    border-right: 1px solid {c['border']} !important;
}}

/* ── All generic text ── */
p, span, li, td, th, em, strong, small, caption,
h1, h2, h3, h4, h5, h6,
.stMarkdown p, .stMarkdown span, .stMarkdown li,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] em,
[data-testid="stMarkdownContainer"] strong {{
    color: {c['text']} !important;
}}

/* ── Widget labels ── */
label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
.stTextInput  > label,
.stNumberInput > label,
.stSelectbox  > label,
.stSlider     > label,
.stCheckbox   > label,
.stRadio      > label,
.stDateInput  > label,
.stTextArea   > label {{
    color: {c['text']} !important;
}}

/* ── Text inputs ── */
.stTextInput  > div > div > input,
.stNumberInput > div > div > input,
.stTextArea   > div > div > textarea {{
    background-color: {c['input_bg']} !important;
    color: {c['text']} !important;
    border-color: {c['border']} !important;
    caret-color: {c['primary']} !important;
}}
.stTextInput  > div > div > input::placeholder,
.stNumberInput > div > div > input::placeholder,
.stTextArea   > div > div > textarea::placeholder {{
    color: {c['text_sub']} !important;
}}
/* number input arrows container */
.stNumberInput > div > div {{
    background-color: {c['input_bg']} !important;
    border-color: {c['border']} !important;
}}
.stNumberInput button svg, .stNumberInput button {{
    fill: {c['text_muted']} !important;
    color: {c['text_muted']} !important;
}}

/* ── Date input ── */
.stDateInput > div > div > input {{
    background-color: {c['input_bg']} !important;
    color: {c['text']} !important;
    border-color: {c['border']} !important;
}}

/* ── Selectbox ── */
.stSelectbox > div > div > div,
[data-baseweb="select"] > div {{
    background-color: {c['input_bg']} !important;
    border-color: {c['border']} !important;
    color: {c['text']} !important;
}}
[data-baseweb="select"] span,
[data-baseweb="select"] div {{
    color: {c['text']} !important;
    background-color: transparent !important;
}}
/* Dropdown popover */
[data-baseweb="popover"],
[data-baseweb="popover"] > div {{
    background-color: {c['surface']} !important;
    border: 1px solid {c['border']} !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5) !important;
}}
[data-baseweb="menu"] li,
[data-baseweb="menu"] ul {{
    background-color: {c['surface']} !important;
    color: {c['text']} !important;
}}
[data-baseweb="menu"] li:hover {{
    background-color: {c['primary_soft']} !important;
}}

/* ── Slider ── */
[data-testid="stSlider"] p,
[data-testid="stSlider"] span,
[data-testid="stSlider"] div[data-baseweb="tooltip"] {{
    color: {c['text_muted']} !important;
}}
[data-testid="stThumbValue"] {{
    color: {c['text']} !important;
}}

/* ── Radio ── */
[data-testid="stRadio"] label p,
[data-testid="stRadio"] label span {{
    color: {c['text']} !important;
}}
[data-testid="stRadio"] div[data-baseweb="radio"] > div {{
    border-color: {c['primary']} !important;
}}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] label span {{
    color: {c['text']} !important;
}}

/* ── Form container ── */
[data-testid="stForm"] {{
    background-color: {c['form_bg']} !important;
    border-color: {c['border']} !important;
    border-radius: 20px !important;
}}

/* ── Native metrics ── */
[data-testid="metric-container"] {{
    background-color: {c['surface']} !important;
    border: 1px solid {c['border']} !important;
    border-radius: 16px !important;
}}
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"],
[data-testid="stMetricDelta"] {{
    color: {c['text']} !important;
}}

/* ── Dataframe / table ── */
[data-testid="stDataFrame"] > div,
[data-testid="stDataFrame"] iframe {{
    background-color: {c['surface']} !important;
    color: {c['text']} !important;
}}

/* ── Tabs ── */
[data-baseweb="tab-list"] {{
    background-color: {c['surface']} !important;
}}
[role="tab"] p, [role="tab"] span {{
    color: {c['text_muted']} !important;
}}
[aria-selected="true"] p, [aria-selected="true"] span {{
    color: #ffffff !important;
}}

/* ── Alert / info / success / error boxes ── */
[data-testid="stAlert"],
[data-testid="stAlert"] > div {{
    background-color: {c['surface']} !important;
    border-color: {c['border']} !important;
}}
[data-testid="stAlert"] p,
[data-testid="stAlert"] span {{
    color: {c['text']} !important;
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background-color: {c['surface']} !important;
    border-color: {c['border']} !important;
}}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {{
    color: {c['text']} !important;
}}

/* ── Spinner ── */
[data-testid="stSpinner"] p {{
    color: {c['text_muted']} !important;
}}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {{
    background-color: {c['primary']} !important;
    color: white !important;
}}

/* ── Sidebar text ── */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] div {{
    color: {c['text']} !important;
}}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a {{
    color: {c['text_muted']} !important;
}}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {{
    color: {c['primary']} !important;
    background-color: {c['primary_soft']} !important;
}}

/* ── Caption / info text ── */
[data-testid="stCaptionContainer"] p {{
    color: {c['text_sub']} !important;
}}

/* ── Divider ── */
hr {{
    border-top-color: {c['border']} !important;
}}
"""


def get_css(c: dict) -> str:
    """Full claymorphism CSS for the active theme."""
    is_dark = st.session_state.get("theme", "light") == "dark"

    dark_section = _dark_overrides(c) if is_dark else ""

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Space+Grotesk:wght@500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {{
    font-family: 'DM Sans', 'Inter', sans-serif;
}}
.stApp {{
    background-color: {c['app_bg']};
}}

/* Hide Streamlit Toolbar, MainMenu, Footer, Deploy button, and Github icon */
#MainMenu, footer, [data-testid="stToolbar"], .stAppDeployButton, #GithubIcon {{
    visibility: hidden !important;
    display: none !important;
}}

/* Style the Streamlit Header to be transparent */
[data-testid="stHeader"], header {{
    background-color: transparent !important;
    background: transparent !important;
    box-shadow: none !important;
    border-bottom: none !important;
}}

/* Ensure the sidebar collapse/expand toggle button and its container are visible and clickable */
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] *,
[data-testid="stSidebarCollapseButton"],
[data-testid="stBaseButton-headerNoPadding"],
[data-testid="baseButton-header"],
header button {{
    visibility: visible !important;
}}

/* Ensure toggle button icon matches theme color */
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stBaseButton-headerNoPadding"] svg,
header button svg {{
    fill: {c['text']} !important;
    color: {c['text']} !important;
}}

section[data-testid="stSidebar"] {{
    background-color: {c['sidebar_bg']} !important;
    border-right: 1px solid {c['border']};
    box-shadow: 4px 0 20px {c['shadow_a']};
}}
.block-container {{
    padding-top: 3.75rem !important;
    background-color: transparent !important;
}}
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {c['primary']}88; border-radius: 4px; }}

/* ═══ SPLASH SCREEN ═══ */
.splash-container {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: radial-gradient(circle at center, {c['bg2']} 0%, {c['bg']} 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 999999;
    animation: fadeIn 0.5s ease both;
}}
.splash-logo {{
    font-size: 6rem;
    animation: pulseSlow 2s ease-in-out infinite, floatBob 3s ease-in-out infinite;
    margin-bottom: 1.5rem;
    filter: drop-shadow(0 10px 20px {c['shadow_a']});
}}
.splash-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: {c['text']};
    letter-spacing: -0.04em;
    margin-bottom: 0.5rem;
    text-shadow: 0 4px 10px {c['shadow_a']};
}}
.splash-subtitle {{
    font-size: 1.1rem;
    color: {c['text_muted']};
    margin-bottom: 3rem;
}}
.splash-loader {{
    width: 240px;
    height: 6px;
    background: {c['border']};
    border-radius: 3px;
    overflow: hidden;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
}}
.splash-loader-bar {{
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, {c['primary']} 0%, {c['coral']} 50%, {c['mint']} 100%);
    border-radius: 3px;
    animation: splashProgress 2.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    transform-origin: left;
}}

@keyframes splashProgress {{
    0% {{ transform: scaleX(0); }}
    50% {{ transform: scaleX(0.7); }}
    100% {{ transform: scaleX(1); }}
}}

/* ═══ CLAY CARDS ═══ */
.clay-card {{
    background: {c['card_grad']};
    border-radius: 24px;
    box-shadow: 8px 8px 20px {c['shadow_a']}, -5px -5px 14px {c['shadow_b']}, inset 0 1px 0 {c['shadow_in']};
    border: 1px solid {c['border']};
    padding: 1.6rem 1.8rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: fadeSlideUp 0.4s ease both;
}}
.clay-card:hover {{
    transform: translateY(-3px);
    box-shadow: 12px 14px 28px {c['shadow_a']}, -5px -5px 14px {c['shadow_b']}, inset 0 1px 0 {c['shadow_in']};
}}
.clay-card-sm {{
    background: {c['card_grad']};
    border-radius: 18px;
    box-shadow: 5px 5px 14px {c['shadow_a']}, -3px -3px 10px {c['shadow_b']}, inset 0 1px 0 {c['shadow_in']};
    border: 1px solid {c['border']};
    padding: 1.2rem 1.4rem;
    transition: transform 0.18s ease;
}}
.clay-card-sm:hover {{ transform: translateY(-2px); }}

/* ═══ PLOTLY CHARTS AS CLAY CARDS ═══ */
div[data-testid="stPlotlyChart"] {{
    background: {c['card_grad']};
    border-radius: 24px;
    box-shadow: 8px 8px 20px {c['shadow_a']}, -5px -5px 14px {c['shadow_b']}, inset 0 1px 0 {c['shadow_in']};
    border: 1px solid {c['border']};
    padding: 1.2rem;
    margin-bottom: 1.5rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: fadeSlideUp 0.4s ease both;
}}
div[data-testid="stPlotlyChart"]:hover {{
    transform: translateY(-3px);
    box-shadow: 12px 14px 28px {c['shadow_a']}, -5px -5px 14px {c['shadow_b']}, inset 0 1px 0 {c['shadow_in']};
}}

/* ═══ METRIC TILES ═══ */
.clay-metric {{
    background: {c['metric_grad']};
    border-radius: 20px;
    box-shadow: 6px 6px 16px {c['shadow_a']}, -4px -4px 12px {c['shadow_b']}, inset 0 1px 0 {c['shadow_in']};
    border: 1px solid {c['border']};
    padding: 1.3rem 1.2rem;
    text-align: center;
    animation: fadeSlideUp 0.45s ease both;
    transition: transform 0.2s ease;
}}
.clay-metric:hover {{ transform: translateY(-3px) scale(1.02); }}
.metric-label {{
    font-size: 0.7rem; font-weight: 600; color: {c['text_muted']};
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;
}}
.metric-value {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.1rem; font-weight: 700; color: {c['primary']}; line-height: 1.1;
}}
.metric-sub {{ font-size: 0.72rem; color: {c['text_sub']}; margin-top: 0.3rem; }}

/* ═══ TYPOGRAPHY ═══ */
.page-title {{
    font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700;
    color: {c['text']}; letter-spacing: -0.02em; margin-bottom: 0.3rem;
    line-height: 1.35 !important;
    animation: fadeSlideUp 0.3s ease both;
}}
.page-title span.accent {{ color: {c['primary']}; }}
.page-subtitle {{
    font-size: 0.9rem; color: {c['text_muted']}; margin-bottom: 2rem;
    line-height: 1.45 !important;
    animation: fadeSlideUp 0.35s ease both;
}}
.section-header {{
    font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 600;
    color: {c['text_muted']}; text-transform: uppercase; letter-spacing: 0.09em;
    margin: 1.8rem 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;
}}
.section-header::after {{
    content: ''; flex: 1; height: 1px; background: {c['border']}; margin-left: 0.4rem;
}}

/* ═══ BADGES ═══ */
.badge-green {{
    display: inline-block; background: {c['mint_soft']}; color: {c['mint']};
    border: 1px solid {c['mint']}; border-radius: 20px;
    padding: 0.2rem 0.75rem; font-size: 0.72rem; font-weight: 600;
}}
.badge-amber {{
    display: inline-block; background: rgba(245,158,11,0.12); color: {c['amber']};
    border: 1px solid {c['amber']}; border-radius: 20px;
    padding: 0.2rem 0.75rem; font-size: 0.72rem; font-weight: 600;
}}
.badge-red {{
    display: inline-block; background: rgba(239,68,68,0.12); color: {c['red']};
    border: 1px solid {c['red']}; border-radius: 20px;
    padding: 0.2rem 0.75rem; font-size: 0.72rem; font-weight: 600;
}}

/* ═══ SHAP BARS ═══ */
.shap-pos {{
    background: {c['mint_soft']}; border-left: 3px solid {c['mint']};
    border-radius: 0 12px 12px 0; padding: 0.6rem 1rem; margin: 0.35rem 0;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 0.88rem; color: {c['text']}; font-weight: 500;
}}
.shap-neg {{
    background: rgba(239,68,68,0.08); border-left: 3px solid {c['red']};
    border-radius: 0 12px 12px 0; padding: 0.6rem 1rem; margin: 0.35rem 0;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 0.88rem; color: {c['text']}; font-weight: 500;
}}

/* ═══ BUTTONS ═══ */
.stButton > button {{
    background: {c['primary']} !important;
    color: #fff !important; border: none !important; border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 0.95rem !important; padding: 0.65rem 1.8rem !important;
    box-shadow: 4px 4px 12px {c['shadow_a']}, -2px -2px 8px {c['shadow_b']} !important;
    transition: all 0.2s ease !important;
}}
.stButton > button:hover {{
    background: {c['coral']} !important; transform: translateY(-2px) !important;
    box-shadow: 6px 6px 18px {c['shadow_a']}, -2px -2px 8px {c['shadow_b']} !important;
}}
.stButton > button:active {{ transform: translateY(0) !important; }}

/* ═══ INPUTS ═══ */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {{
    background: {c['input_bg']} !important; border: 1.5px solid {c['border']} !important;
    border-radius: 12px !important; color: {c['text']} !important;
    padding: 0.6rem 0.9rem !important; font-family: 'DM Sans', sans-serif !important;
    box-shadow: inset 2px 2px 6px {c['shadow_a']}, inset -1px -1px 4px {c['shadow_b']} !important;
}}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {{
    border-color: {c['primary']} !important;
    box-shadow: inset 2px 2px 6px {c['shadow_a']}, 0 0 0 3px {c['primary_soft']} !important;
    outline: none !important;
}}
.stTextInput > div > div > input::placeholder {{ color: {c['text_sub']} !important; }}
.stNumberInput > div > div {{
    background: {c['input_bg']} !important; border: 1.5px solid {c['border']} !important;
    border-radius: 12px !important;
}}

/* ═══ SELECTBOX ═══ */
.stSelectbox > div > div > div,
[data-baseweb="select"] > div {{
    background: {c['input_bg']} !important; border: 1.5px solid {c['border']} !important;
    border-radius: 12px !important; color: {c['text']} !important;
}}

/* ═══ TABS ═══ */
.stTabs [data-baseweb="tab-list"] {{
    background: {c['surface']} !important; border-radius: 16px !important;
    padding: 0.3rem !important;
    box-shadow: inset 2px 2px 8px {c['shadow_a']}, inset -2px -2px 6px {c['shadow_b']};
    gap: 0.2rem;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 12px !important; padding: 0.45rem 1.2rem !important;
    color: {c['text_muted']} !important; font-weight: 500 !important;
}}
.stTabs [aria-selected="true"] {{
    background: {c['primary']} !important; color: white !important;
    box-shadow: 3px 3px 10px {c['shadow_a']} !important;
}}

/* ═══ FORM ═══ */
[data-testid="stForm"] {{
    background-color: {c['form_bg']} !important;
    border: 1px solid {c['border']} !important;
    border-radius: 20px !important;
    padding: 1.2rem !important;
}}

/* ═══ DATAFRAME ═══ */
.stDataFrame {{ border-radius: 18px !important; overflow: hidden;
    box-shadow: 5px 5px 16px {c['shadow_a']}, -3px -3px 10px {c['shadow_b']}; }}

/* ═══ ALERTS ═══ */
[data-testid="stAlert"] {{
    border-radius: 16px !important; border: 1px solid {c['border']} !important;
    box-shadow: 3px 3px 10px {c['shadow_a']} !important;
}}

/* ═══ HR ═══ */
hr {{ border: none !important; border-top: 1px solid {c['border']} !important; margin: 1.2rem 0 !important; }}

/* ═══ PAGE LINKS (sidebar nav) ═══ */
[data-testid="stPageLink"] > a {{
    display: flex !important; align-items: center !important; gap: 0.6rem !important;
    padding: 0.55rem 1rem !important; border-radius: 12px !important;
    color: {c['text_muted']} !important; font-weight: 500 !important;
    font-size: 0.9rem !important; text-decoration: none !important;
    transition: all 0.18s ease !important; margin-bottom: 0.2rem !important;
}}
[data-testid="stPageLink"] > a:hover {{
    background: {c['primary_soft']} !important; color: {c['primary']} !important;
    transform: translateX(3px) !important;
}}

/* ═══ SUBJECT CARDS ═══ */
.subj-card {{
    background: {c['card_grad']}; border-radius: 20px;
    box-shadow: 6px 6px 16px {c['shadow_a']}, -4px -4px 12px {c['shadow_b']};
    border: 1px solid {c['border']}; padding: 1.4rem;
    animation: fadeSlideUp 0.4s ease both; transition: transform 0.2s;
}}
.subj-card:hover {{ transform: translateY(-3px); }}
.subj-name {{ font-family:'Space Grotesk',sans-serif; font-size:1rem; font-weight:600; color:{c['text']}; }}
.subj-score {{ font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700; color:{c['primary']}; margin:0.3rem 0; }}
.subj-stat {{ font-size:0.8rem; color:{c['text_sub']}; }}

/* ═══ SCORE ═══ */
.score-big {{
    font-family:'Space Grotesk',sans-serif; font-size:5.5rem; font-weight:800;
    text-align:center; line-height:1; animation: pulseSlow 2s ease-in-out infinite;
}}

/* ═══ LABEL COLOUR ═══ */
label {{ color: {c['text']} !important; font-weight: 500 !important; }}
.stMarkdown p {{ color: {c['text']} !important; }}

/* ═══ ANIMATIONS ═══ */
@keyframes fadeSlideUp {{ from {{ opacity:0; transform:translateY(14px); }} to {{ opacity:1; transform:translateY(0); }} }}
@keyframes fadeIn      {{ from {{ opacity:0; }} to {{ opacity:1; }} }}
@keyframes floatBob    {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-9px); }} }}
@keyframes pulseSlow   {{ 0%,100% {{ transform:scale(1); opacity:1; }} 50% {{ transform:scale(1.04); opacity:0.85; }} }}

{dark_section}
</style>
"""


def inject_css():
    c = get_theme_colors()
    st.markdown(get_css(c), unsafe_allow_html=True)


def render_theme_toggle():
    is_dark = st.session_state.get("theme", "light") == "dark"
    icon  = "☀️" if is_dark else "🌙"
    label = "Light mode" if is_dark else "Dark mode"
    if st.button(f"{icon}  {label}", use_container_width=True, key="theme_toggle_btn"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()


def score_color(c: dict, val: float) -> str:
    if val >= 7.5: return c["mint"]
    if val >= 5.0: return c["amber"]
    return c["red"]


def score_badge(val: float) -> tuple:
    if val >= 7.5: return "badge-green", "Excellent"
    if val >= 5.0: return "badge-amber", "Good"
    return "badge-red", "Needs Work"


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        rgb = tuple(int(hex_color[i:i+1]*2, 16) for i in range(3))
    else:
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})"


def plotly_layout(c: dict, height: int = 320, **kwargs) -> dict:
    return dict(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=c["text_muted"], family="DM Sans, Inter, sans-serif"),
        margin=dict(l=8, r=8, t=36, b=8),
        transition=dict(duration=500, easing="cubic-in-out"),
        xaxis=dict(
            gridcolor=c["border"],
            tickfont=dict(color=c["text_sub"], size=11),
            linecolor=c["border"],
            zerolinecolor=c["border"],
        ),
        yaxis=dict(
            gridcolor=c["border"],
            tickfont=dict(color=c["text_sub"], size=11),
            linecolor=c["border"],
            zerolinecolor=c["border"],
        ),
        hoverlabel=dict(
            bgcolor=c["surface"],
            bordercolor=c["border"],
            font=dict(color=c["text"], family="DM Sans"),
        ),
        **kwargs,
    )


def render_github_contribution_graph(df, c: dict) -> str:
    """
    Renders a beautiful GitHub-style contribution grid for the last 12 weeks of study.
    """
    import datetime
    import pandas as pd

    if df.empty:
        return ""

    # 1. Clean data and aggregate hours by date
    df_clean = df.copy()
    df_clean["date_str"] = pd.to_datetime(df_clean["date"]).dt.strftime("%Y-%m-%d")
    daily_hours = df_clean.groupby("date_str")["study_hours"].sum().to_dict()

    # 2. Setup dates (last 12 weeks, aligned to Sunday)
    today = datetime.date.today()
    # 12 weeks ago is 12 * 7 = 84 days
    start_date = today - datetime.timedelta(days=83)
    # Align start_date to Sunday (Python weekday() = 6 is Sunday)
    while start_date.weekday() != 6:
        start_date -= datetime.timedelta(days=1)

    # Generate list of dates from start_date to today
    dates = []
    curr = start_date
    while curr <= today:
        dates.append(curr)
        curr += datetime.timedelta(days=1)

    # Group dates into columns of 7 days (Sunday to Saturday)
    cols_data = []
    for i in range(0, len(dates), 7):
        cols_data.append(dates[i:i+7])

    # 3. Build HTML/CSS
    def get_color(hours: float) -> str:
        if hours <= 0:
            return c["bg2"]
        elif hours <= 1.5:
            return c["primary_soft"]
        elif hours <= 3.5:
            return hex_to_rgba(c["primary"], 0.45)
        elif hours <= 5.5:
            return hex_to_rgba(c["primary"], 0.75)
        else:
            return c["primary"]

    # Weekday labels aligned to the grid
    labels_html = f'<div style="display:flex; flex-direction:column; justify-content:space-between; height:94px; margin-right:8px; font-size:0.68rem; color:{c["text_muted"]}; padding: 2px 0;"><div>Sun</div><div>Tue</div><div>Thu</div><div>Sat</div></div>'

    cols_html = []
    for col in cols_data:
        squares = []
        for d in col:
            d_str = d.strftime("%Y-%m-%d")
            hours = daily_hours.get(d_str, 0.0)
            color = get_color(hours)
            tooltip = f"{hours:.1f} hrs on {d.strftime('%b %d, %Y')}"
            squares.append(f'<div title="{tooltip}" style="width:10px; height:10px; background-color:{color}; border-radius:2px; transition:transform 0.1s ease; cursor:pointer;" onmouseover="this.style.transform=\'scale(1.3)\'" onmouseout="this.style.transform=\'scale(1)\'"></div>')
        # Pad incomplete column
        while len(squares) < 7:
            squares.append('<div style="width:10px; height:10px;"></div>')

        col_html = f'<div style="display:flex; flex-direction:column; gap:4px;">{"".join(squares)}</div>'
        cols_html.append(col_html)

    grid_html = f'<div style="display:flex; justify-content:center; align-items:center; background:{c["surface"]}; border:1px solid {c["border"]}; border-radius:16px; padding:1.2rem; box-shadow:8px 8px 20px {c["shadow_a"]}, inset 0 1px 0 {c["shadow_in"]}; width:fit-content; margin:0.5rem auto 1.8rem auto;">{labels_html}<div style="display:flex; gap:4px;">{"".join(cols_html)}</div></div>'
    return grid_html
