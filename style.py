"""
Shared visual theme for the GenoLineage dashboard.
Import inject_custom_css() and call it at the top of every page so the
look stays consistent across the whole multi-page app.
"""

import streamlit as st


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* ---- App background: deep navy with subtle gradient ---- */
.stApp {
    background: linear-gradient(160deg, #0b1120 0%, #10192e 45%, #0d1424 100%);
    color: #e6ecf5;
}

/* ---- Sidebar styling ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #131c33 100%);
    border-right: 1px solid rgba(94, 234, 212, 0.15);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #5eead4;
}

/* ---- Sidebar text & nav links: fix dim/gray look ---- */
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #e6ecf5 !important;
    opacity: 1 !important;
}

section[data-testid="stSidebarNav"] a {
    color: #c7d2fe !important;
    opacity: 1 !important;
    font-weight: 500;
}

section[data-testid="stSidebarNav"] a:hover {
    color: #5eead4 !important;
}

section[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: #5eead4 !important;
    font-weight: 700;
}

/* ---- Headings ---- */
h1 {
    background: linear-gradient(90deg, #5eead4, #818cf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}
h2, h3 {
    color: #c7d2fe !important;
    font-weight: 600 !important;
}

/* ---- Hero banner card ---- */
.hero-banner {
    background: linear-gradient(120deg, rgba(94,234,212,0.12), rgba(129,140,248,0.10));
    border: 1px solid rgba(94, 234, 212, 0.25);
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

/* ---- Metric / stat cards ---- */
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
    transition: transform 0.15s ease, border-color 0.15s ease;
}
.stat-card:hover {
    transform: translateY(-3px);
    border-color: rgba(94, 234, 212, 0.4);
}
.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #5eead4;
    font-family: 'JetBrains Mono', monospace;
}
.stat-label {
    font-size: 13px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}

/* ---- Module badge pills ---- */
.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
    margin-right: 8px;
}
.badge-dp   { background: rgba(94,234,212,0.15); color: #5eead4; border: 1px solid rgba(94,234,212,0.35); }
.badge-rec  { background: rgba(129,140,248,0.15); color: #a5b4fc; border: 1px solid rgba(129,140,248,0.35); }
.badge-greedy { background: rgba(244,114,182,0.15); color: #f9a8d4; border: 1px solid rgba(244,114,182,0.35); }

/* ---- DNA sequence monospace display ---- */
.seq-box {
    font-family: 'JetBrains Mono', monospace;
    background: #0a0f1e;
    border: 1px solid rgba(94,234,212,0.2);
    border-radius: 10px;
    padding: 14px 16px;
    word-break: break-all;
    font-size: 13px;
    color: #5eead4;
    line-height: 1.6;
}

/* ---- Buttons ---- */
.stButton > button {
    background: linear-gradient(90deg, #5eead4, #818cf8);
    color: #0a0f1e;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.4rem;
    transition: opacity 0.15s ease;
}
.stButton > button:hover {
    opacity: 0.85;
    color: #0a0f1e;
}

/* ---- Risk level tags ---- */
.risk-high   { color: #f87171; font-weight: 700; }
.risk-medium { color: #fbbf24; font-weight: 700; }
.risk-low    { color: #4ade80; font-weight: 700; }
.risk-none   { color: #94a3b8; font-weight: 700; }

/* ---- Dataframe / table tweaks ---- */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* ---- Divider ---- */
hr {
    border-color: rgba(255,255,255,0.08);
}
</style>
"""


def inject_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def hero_banner(title, subtitle):
    st.markdown(
        f"""
        <div class="hero-banner">
            <h1 style="margin-bottom:4px;">{title}</h1>
            <p style="color:#94a3b8; font-size:15px; margin:0;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_card_row(stats):
    """stats: list of (value, label) tuples"""
    cols = st.columns(len(stats))
    for col, (value, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-value">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def risk_tag(pct):
    """Returns an HTML span colored by risk severity."""
    if pct >= 50:
        return f'<span class="risk-high">{pct:.1f}% — High</span>'
    elif pct >= 20:
        return f'<span class="risk-medium">{pct:.1f}% — Moderate</span>'
    elif pct > 0:
        return f'<span class="risk-low">{pct:.1f}% — Low</span>'
    else:
        return f'<span class="risk-none">0% — None detected</span>'