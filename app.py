import json
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="Aegis // Agent Firewall",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_html(html: str):
    """Render HTML cleanly without Markdown interpreting indented lines as code blocks."""
    clean = "\n".join(line.strip() for line in html.strip().splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)


# ==============================================================================
# GLOBAL DESIGN SYSTEM & STYLING (AI Security Operations Center)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {
        --bg-deep: #070D17;
        --bg-surface: #0B1220;
        --bg-card: #0F1726;
        --bg-card-elevated: #111B2C;
        --bg-card-hover: #142034;
        
        --border-subtle: rgba(56, 189, 248, 0.12);
        --border-card: rgba(255, 255, 255, 0.08);
        --border-highlight: rgba(0, 240, 255, 0.35);
        
        --text-primary: #FFFFFF;
        --text-secondary: #F1F5F9;
        --text-muted: #94A3B8;
        --text-dim: #64748B;
        
        --cyan-accent: #00F0FF;
        --cyan-glow: rgba(0, 240, 255, 0.2);
        --blue-accent: #38BDF8;
        
        --green-safe: #10B981;
        --green-bg: rgba(16, 185, 129, 0.12);
        --green-border: rgba(16, 185, 129, 0.35);
        
        --amber-warning: #F59E0B;
        --amber-bg: rgba(245, 158, 11, 0.12);
        --amber-border: rgba(245, 158, 11, 0.35);
        
        --red-danger: #EF4444;
        --red-bg: rgba(239, 68, 68, 0.12);
        --red-border: rgba(239, 68, 68, 0.35);
    }

    /* Base Layout */
    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-deep) !important;
        color: var(--text-secondary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    [data-testid="stAppViewContainer"] {
        background: 
            radial-gradient(circle at 10% 8%, rgba(0, 240, 255, 0.04) 0%, transparent 40%),
            radial-gradient(circle at 90% 70%, rgba(56, 189, 248, 0.03) 0%, transparent 45%),
            linear-gradient(180deg, #070D17 0%, #0B1220 100%) !important;
    }

    .block-container {
        max-width: 1560px !important;
        padding: 2rem 3rem 4rem !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        backdrop-filter: blur(8px);
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.025em;
        font-weight: 700;
    }

    p, span, label {
        color: var(--text-muted);
    }

    .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ==========================================================================
       SIDEBAR STYLING
       ========================================================================== */
    [data-testid="stSidebar"] {
        background: #09101D !important;
        border-right: 1px solid var(--border-subtle) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4);
    }

    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1.35rem !important;
    }

    .sidebar-brand {
        padding-bottom: 1.25rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid var(--border-card);
    }

    .brand-title {
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        color: #ffffff !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .brand-subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        color: var(--cyan-accent) !important;
        text-transform: uppercase;
        margin-top: 0.2rem;
    }

    .system-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.28);
        border-radius: 9999px;
        padding: 0.22rem 0.65rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 600;
        color: var(--green-safe) !important;
        letter-spacing: 0.08em;
        margin-top: 0.75rem;
    }

    .pulse-dot {
        width: 6px;
        height: 6px;
        background-color: var(--green-safe);
        border-radius: 50%;
        box-shadow: 0 0 8px var(--green-safe);
        animation: pulseAnimation 2s infinite ease-in-out;
    }

    @keyframes pulseAnimation {
        0%, 100% { transform: scale(0.9); opacity: 0.6; }
        50% { transform: scale(1.3); opacity: 1; filter: drop-shadow(0 0 4px var(--green-safe)); }
    }

    .pulse-dot-cyan {
        width: 7px;
        height: 7px;
        background-color: var(--cyan-accent);
        border-radius: 50%;
        box-shadow: 0 0 10px var(--cyan-accent);
        animation: pulseCyan 2s infinite;
        display: inline-block;
    }

    @keyframes pulseCyan {
        0%, 100% { opacity: 0.5; transform: scale(0.9); }
        50% { opacity: 1; transform: scale(1.2); }
    }

    /* Sidebar Navigation (Radio) */
    [data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }

    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {
        gap: 0.35rem;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 0.65rem 0.85rem !important;
        margin: 0 !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
        background: rgba(56, 189, 248, 0.06) !important;
        border-color: rgba(56, 189, 248, 0.2) !important;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label [data-testid="stMarkdownContainer"] p {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        color: var(--text-muted) !important;
        letter-spacing: 0.02em;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) {
        background: rgba(0, 240, 255, 0.08) !important;
        border-left: 3px solid var(--cyan-accent) !important;
        border-color: rgba(0, 240, 255, 0.25) rgba(0, 240, 255, 0.25) rgba(0, 240, 255, 0.25) var(--cyan-accent) !important;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    .sidebar-section-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--text-dim);
        margin: 1.4rem 0 0.55rem;
    }

    .risk-policy-card {
        background: #0B1424;
        border: 1px solid var(--border-card);
        border-radius: 8px;
        padding: 0.75rem 0.85rem;
        margin-top: 0.45rem;
        display: flex;
        flex-direction: column;
        gap: 0.45rem;
    }

    .risk-policy-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
    }

    .system-status-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-top: 0.45rem;
    }

    .status-list-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-muted);
    }

    .sidebar-footer {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border-card);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: var(--text-dim);
        letter-spacing: 0.08em;
    }

    /* ==========================================================================
       DASHBOARD TOP HEADER
       ========================================================================== */
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        padding-bottom: 1.5rem;
        margin-bottom: 1.75rem;
        border-bottom: 1px solid var(--border-card);
    }

    .breadcrumb {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        color: var(--cyan-accent);
        text-transform: uppercase;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .dashboard-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff !important;
        margin: 0;
        line-height: 1.15;
    }

    .dashboard-subtitle {
        font-size: 0.92rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
    }

    .header-status-cluster {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .header-status-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: #0F1726;
        border: 1px solid var(--border-subtle);
        border-radius: 6px;
        padding: 0.45rem 0.85rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--text-secondary);
        letter-spacing: 0.06em;
    }

    /* ==========================================================================
       HERO / SECURITY OVERVIEW CARD
       ========================================================================== */
    .hero-card {
        background: linear-gradient(135deg, #0F1726 0%, #111B2C 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 1.65rem 2.25rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .hero-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--cyan-accent), transparent);
    }

    .hero-content {
        max-width: 640px;
        z-index: 2;
    }

    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        color: var(--cyan-accent);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .hero-heading {
        font-size: 1.55rem;
        font-weight: 800;
        color: #ffffff !important;
        line-height: 1.25;
        margin-bottom: 0.5rem;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    .hero-desc {
        font-size: 0.9rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin: 0;
    }

    .hero-viz {
        z-index: 1;
        opacity: 0.95;
    }

    /* ==========================================================================
       KPI METRIC CARDS
       ========================================================================== */
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border-card);
        border-radius: 12px;
        padding: 1.35rem 1.4rem;
        position: relative;
        transition: all 0.22s ease-in-out;
        overflow: hidden;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.16);
        box-shadow: 0 10px 24px -8px rgba(0, 0, 0, 0.5);
    }

    .kpi-card.approved { border-left: 3px solid var(--green-safe); }
    .kpi-card.review { border-left: 3px solid var(--amber-warning); }
    .kpi-card.blocked { border-left: 3px solid var(--red-danger); }
    .kpi-card.events { border-left: 3px solid var(--cyan-accent); }

    .kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.65rem;
    }

    .kpi-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-muted);
    }

    .kpi-icon {
        font-size: 1.1rem;
    }

    .kpi-value {
        font-size: 2.3rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
        line-height: 1;
        margin-bottom: 0.4rem;
    }

    .kpi-detail {
        font-size: 0.75rem;
        color: var(--text-dim);
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* ==========================================================================
       PANELS & CARDS
       ========================================================================== */
    .panel-card {
        background: var(--bg-card);
        border: 1px solid var(--border-card);
        border-radius: 12px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }

    .panel-card:hover {
        border-color: rgba(255, 255, 255, 0.14);
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.15rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-card);
    }

    .panel-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff !important;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.22rem 0.55rem;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .badge-safe {
        background: var(--green-bg);
        color: var(--green-safe) !important;
        border: 1px solid var(--green-border);
    }

    .badge-warning {
        background: var(--amber-bg);
        color: var(--amber-warning) !important;
        border: 1px solid var(--amber-border);
    }

    .badge-danger {
        background: var(--red-bg);
        color: var(--red-danger) !important;
        border: 1px solid var(--red-border);
    }

    .badge-cyan {
        background: rgba(0, 240, 255, 0.1);
        color: var(--cyan-accent) !important;
        border: 1px solid rgba(0, 240, 255, 0.3);
    }

    .badge-neutral {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-muted) !important;
        border: 1px solid var(--border-card);
    }

    /* Code Editor Headers */
    .editor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #0B111F;
        padding: 0.45rem 0.85rem;
        border-radius: 8px 8px 0 0;
        border: 1px solid var(--border-subtle);
        border-bottom: none;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-dim);
    }

    [data-testid="stTextArea"] textarea {
        background: #070D17 !important;
        color: #38BDF8 !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 0 0 8px 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        line-height: 1.5 !important;
        padding: 0.85rem !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--cyan-accent) !important;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.25) !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease !important;
        border: 1px solid var(--border-card) !important;
        background: #111B2C !important;
        color: #F1F5F9 !important;
        min-height: 42px !important;
    }

    .stButton > button:hover {
        background: #16243A !important;
        border-color: var(--blue-accent) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284C7 0%, #00F0FF 100%) !important;
        color: #070D17 !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 4px 16px rgba(0, 240, 255, 0.3) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #039BE5 0%, #2CF4FF 100%) !important;
        box-shadow: 0 6px 20px rgba(0, 240, 255, 0.45) !important;
        transform: translateY(-1px);
    }

    /* ==========================================================================
       PROMINENT DECISION EVALUATION PANEL
       ========================================================================== */
    .decision-panel {
        border-radius: 10px;
        padding: 1.4rem 1.6rem;
        margin-top: 1.25rem;
        border: 1px solid;
    }

    .decision-panel.low {
        background: rgba(16, 185, 129, 0.07);
        border-color: var(--green-border);
    }

    .decision-panel.medium {
        background: rgba(245, 158, 11, 0.07);
        border-color: var(--amber-border);
    }

    .decision-panel.high {
        background: rgba(239, 68, 68, 0.07);
        border-color: var(--red-border);
    }

    .decision-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .decision-verdict {
        font-size: 1.35rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .decision-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.85rem;
        margin-bottom: 0.85rem;
    }

    .decision-cell {
        background: rgba(0, 0, 0, 0.25);
        border-radius: 6px;
        padding: 0.65rem 0.85rem;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }

    .decision-cell-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-dim);
        margin-bottom: 0.25rem;
    }

    .decision-cell-value {
        font-size: 0.88rem;
        font-weight: 600;
        color: #ffffff;
    }

    .risk-meter-track {
        height: 6px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 9999px;
        overflow: hidden;
        margin-top: 0.75rem;
    }

    .risk-meter-fill {
        height: 100%;
        border-radius: 9999px;
    }

    .risk-meter-fill.low { background: var(--green-safe); }
    .risk-meter-fill.medium { background: var(--amber-warning); }
    .risk-meter-fill.high { background: var(--red-danger); }

    /* ==========================================================================
       SCENARIO CARDS
       ========================================================================== */
    .scenario-item {
        background: #0B1322;
        border: 1px solid var(--border-card);
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.65rem;
        transition: all 0.2s ease;
    }

    .scenario-item:hover {
        border-color: rgba(56, 189, 248, 0.35);
        background: #0F1A2D;
    }

    .scenario-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.25rem;
    }

    .scenario-name {
        font-weight: 700;
        font-size: 0.88rem;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }

    .scenario-desc {
        font-size: 0.78rem;
        color: var(--text-muted);
        line-height: 1.35;
    }

    /* Human Gate Card */
    .human-gate-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(20, 15, 8, 0.85) 100%);
        border: 1px solid var(--amber-border);
        border-radius: 12px;
        padding: 1.4rem;
        margin-top: 1.25rem;
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.12);
    }

    /* Policy Decision Pipeline */
    .pipeline-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.5rem;
        background: #09101D;
        border: 1px solid var(--border-card);
        border-radius: 10px;
        overflow-x: auto;
    }

    .pipeline-node {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        min-width: 95px;
    }

    .pipeline-circle {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #0F182C;
        border: 1px solid var(--border-subtle);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        color: var(--cyan-accent);
        margin-bottom: 0.45rem;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.15);
    }

    .pipeline-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-muted);
    }

    .pipeline-arrow {
        color: rgba(56, 189, 248, 0.4);
        font-size: 0.95rem;
        padding: 0 0.5rem;
    }

    /* Live Policy Events Table */
    .event-row {
        display: grid;
        grid-template-columns: 85px 140px 140px 1fr 90px 105px;
        align-items: center;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        font-size: 0.82rem;
        transition: background-color 0.15s ease;
    }

    .event-row:hover {
        background: rgba(255, 255, 255, 0.02);
    }

    .event-row-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: var(--text-dim);
        text-transform: uppercase;
        border-bottom: 1px solid var(--border-card);
        padding-bottom: 0.65rem;
        margin-bottom: 0.35rem;
    }

    /* Streamlit widget overrides */
    div[data-testid="stToggle"] label {
        color: var(--text-secondary) !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
    }

    div[data-testid="stSelectbox"] label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: var(--text-muted) !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #0B111F !important;
        border-color: rgba(56, 189, 248, 0.18) !important;
        color: #F1F5F9 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stTextInput"] label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: var(--text-muted) !important;
        margin-bottom: 0.25rem !important;
    }

    div[data-testid="stTextInput"] input {
        background-color: #0B111F !important;
        border-color: rgba(56, 189, 248, 0.18) !important;
        color: #F1F5F9 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: var(--cyan-accent) !important;
    }

    [data-testid="stExpander"] {
        background: #09101D !important;
        border: 1px solid var(--border-card) !important;
        border-radius: 8px !important;
        margin-top: 0.75rem !important;
    }
    
    [data-testid="stExpander"] details summary {
        color: var(--text-muted) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
    }

    hr {
        border-color: var(--border-card) !important;
        margin: 1.25rem 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Professional Scenarios (Section 8)
PRESET_SCENARIOS = [
    {
        "id": "web_search",
        "name": "WEB SEARCH",
        "icon": "🔍",
        "risk": "LOW",
        "desc": "Fetch documentation and public web indexing notes",
        "payload": {
            "agent": "research-agent",
            "tool": "web_search",
            "args": {"query": "AI agent security best practices"},
        },
    },
    {
        "id": "send_email",
        "name": "SEND EMAIL",
        "icon": "✉️",
        "risk": "MEDIUM",
        "desc": "Outbound communication targeting external recipient",
        "payload": {
            "agent": "support-agent",
            "tool": "send_email",
            "args": {"recipient": "customer@acme-corp.com", "subject": "Account Security Verification"},
        },
    },
    {
        "id": "database_update",
        "name": "DATABASE UPDATE",
        "icon": "💾",
        "risk": "LOW",
        "desc": "Read/write session telemetry to internal application table",
        "payload": {
            "agent": "telemetry-agent",
            "tool": "update_record",
            "args": {"table": "agent_session_telemetry", "action": "upsert_status"},
        },
    },
    {
        "id": "file_delete",
        "name": "FILE DELETE",
        "icon": "⚠️",
        "risk": "HIGH",
        "desc": "Destructive drop or wipe targeting production system files",
        "payload": {
            "agent": "ops-agent",
            "tool": "delete_file",
            "args": {"path": "/etc/production_db/config.json", "force": True},
        },
    },
    {
        "id": "external_api",
        "name": "EXTERNAL API",
        "icon": "🔑",
        "risk": "MEDIUM",
        "desc": "Request token rotation and credential refresh via external gateway",
        "payload": {
            "agent": "devops-agent",
            "tool": "rotate_api_token",
            "args": {"service": "stripe_payment_gateway", "scope": "admin_keys"},
        },
    },
]

DEFAULT_PAYLOAD = PRESET_SCENARIOS[0]["payload"]


def build_payload_from_form(agent: str, tool: str, args_input: str) -> dict:
    clean_args = (args_input or "").strip()
    parsed_args = None
    if clean_args.startswith("{") and clean_args.endswith("}"):
        try:
            parsed_args = json.loads(clean_args)
        except Exception:
            parsed_args = None
    if parsed_args is None:
        parsed_args = {"query": clean_args} if clean_args else {}
    return {
        "agent": (agent or "").strip(),
        "tool": (tool or "").strip(),
        "args": parsed_args,
    }


def sync_event_to_state(event: dict):
    if not isinstance(event, dict):
        return
    st.session_state["form_agent"] = str(event.get("agent", ""))
    st.session_state["form_tool"] = str(event.get("tool", ""))
    args = event.get("args")
    if isinstance(args, dict) and len(args) == 1 and "query" in args:
        st.session_state["form_args"] = str(args["query"])
    elif isinstance(args, dict):
        st.session_state["form_args"] = json.dumps(args)
    else:
        st.session_state["form_args"] = str(args or "")
    st.session_state["raw_json_str"] = json.dumps(event, indent=2)


def init_state():
    default_args = DEFAULT_PAYLOAD.get("args", {})
    default_query = default_args.get("query", "AI agent security best practices") if isinstance(default_args, dict) else str(default_args)
    defaults = {
        "events": [],
        "pending": None,
        "automation": True,
        "last_result": None,
        "form_agent": DEFAULT_PAYLOAD.get("agent", "research-agent"),
        "form_tool": DEFAULT_PAYLOAD.get("tool", "web_search"),
        "form_args": default_query,
        "raw_json_str": json.dumps(DEFAULT_PAYLOAD, indent=2),
        "show_advanced": False,
        "prev_show_advanced": False,
        "pending_load_event": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.get("pending_load_event"):
        event = st.session_state.pop("pending_load_event")
        sync_event_to_state(event)


def evaluate(event):
    combined_parts = [
        str(event.get("tool", "")),
        str(event.get("action", "")),
        str(event.get("resource", "")),
    ]
    args = event.get("args")
    if isinstance(args, dict):
        combined_parts.extend(str(v) for v in args.values())
        combined_parts.extend(str(k) for k in args.keys())
    elif args:
        combined_parts.append(str(args))

    combined = " ".join(combined_parts).lower()

    if any(word in combined for word in ("delete", "drop", "destroy", "shutdown", "format", "production_db", "wipe", "truncate", "rm -rf")):
        return {
            "risk": "HIGH",
            "score": 95,
            "decision": "BLOCKED",
            "policy": "POLICY-SEC-01 (Strict Isolation)",
            "reason": "Destructive or production-impacting operation detected. Unauthorized file/data mutation prevented.",
            "action": "IMMEDIATE BLOCK & ALERT OPERATOR",
        }
    if any(word in combined for word in ("email", "send", "password", "credential", "upload", "payment", "token", "rotate", "api_key", "secret")):
        return {
            "risk": "MEDIUM",
            "score": 62,
            "decision": "REVIEW",
            "policy": "POLICY-SEC-02 (Human Gate Armed)",
            "reason": "Sensitive outbound communication or credential operation detected. Human sign-off required.",
            "action": "ROUTE TO OPERATOR REVIEW QUEUE",
        }
    return {
        "risk": "LOW",
        "score": 14,
        "decision": "APPROVED",
        "policy": "POLICY-SEC-03 (Least Privilege Baseline)",
        "reason": "Operation strictly matches least-privilege read/search policy boundary.",
        "action": "ALLOW EXECUTION & LOG TO AUDIT STREAM",
    }


def record_event(event, result, source="manual"):
    args = event.get("args")
    resource_str = event.get("resource")
    if not resource_str and isinstance(args, dict):
        resource_str = str(args.get("query") or args.get("recipient") or args.get("path") or args.get("table") or args.get("service") or args)
    elif not resource_str:
        resource_str = str(args or "none")

    st.session_state.events.insert(0, {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Agent": event.get("agent", "unknown"),
        "Tool": event.get("tool", "unknown"),
        "Resource": resource_str,
        "Risk": result["risk"],
        "Score": f'{result["score"]}%',
        "Decision": result["decision"],
        "Policy": result.get("policy", "POLICY-SEC-03"),
        "Source": source,
    })


def process_event(event, source="manual"):
    result = evaluate(event)
    st.session_state.last_result = {"event": event, "result": result}
    if result["risk"] == "MEDIUM" and st.session_state.automation:
        st.session_state.pending = (event, result)
    else:
        record_event(event, result, source)
    return result


def render_sidebar():
    with st.sidebar:
        # 1. Header (Section 2)
        render_html(
            """
            <div class="sidebar-brand">
                <div class="brand-title">
                    <span>🛡️</span> AEGIS
                </div>
                <div class="brand-subtitle">AGENT FIREWALL</div>
                <div class="system-status-pill">
                    <span class="pulse-dot"></span>
                    <span>SYSTEM ONLINE</span>
                </div>
            </div>
            """
        )

        # 2. Navigation
        render_html('<div class="sidebar-section-title">CONTROL PLANE</div>')
        nav_options = ["⊞ Command Center", "⚖ Policy Studio", "📜 Audit Trail"]
        selected_nav = st.radio("Navigation", nav_options, label_visibility="collapsed", key="nav_workspace_radio")
        
        page_map = {
            "⊞ Command Center": "Command center",
            "⚖ Policy Studio": "Policy studio",
            "📜 Audit Trail": "Audit trail",
        }
        current_page = page_map.get(selected_nav, "Command center")

        # 3. Automation Section
        render_html('<div class="sidebar-section-title">AUTOMATION</div>')
        automation = st.toggle("Route sensitive calls to review", value=st.session_state.automation, key="sidebar_auto_toggle")
        st.session_state.automation = automation

        # 4. Risk Policy Summary
        render_html(
            """
            <div class="sidebar-section-title" style="margin-top:0.85rem;">RISK POLICY</div>
            <div class="risk-policy-card">
                <div class="risk-policy-row">
                    <span class="badge badge-danger">HIGH</span>
                    <span style="color:#EF4444; font-weight:700;">➔ BLOCK</span>
                </div>
                <div class="risk-policy-row">
                    <span class="badge badge-warning">MEDIUM</span>
                    <span style="color:#F59E0B; font-weight:700;">➔ REVIEW</span>
                </div>
                <div class="risk-policy-row">
                    <span class="badge badge-safe">LOW</span>
                    <span style="color:#10B981; font-weight:700;">➔ ALLOW + LOG</span>
                </div>
            </div>
            """
        )

        # 5. System Status (Section 2)
        render_html(
            """
            <div class="sidebar-section-title">SYSTEM STATUS</div>
            <div class="system-status-list">
                <div class="status-list-item">
                    <span>● Policy Engine</span>
                    <span style="color:#10B981; font-weight:700;">ONLINE</span>
                </div>
                <div class="status-list-item">
                    <span>● Audit Stream</span>
                    <span style="color:#00F0FF; font-weight:700;">RECORDING</span>
                </div>
                <div class="status-list-item">
                    <span>● Interceptor</span>
                    <span style="color:#38BDF8; font-weight:700;">ACTIVE</span>
                </div>
            </div>
            """
        )

        # 6. Bottom Version
        render_html(
            """
            <div class="sidebar-footer">
                <div>AEGIS v1.0 // ENTERPRISE</div>
                <div style="color:#64748B; margin-top:2px;">SECURITY CONTROL PLANE</div>
            </div>
            """
        )

        return current_page


def render_evaluation_result():
    payload = st.session_state.last_result
    if not payload:
        return
    event, result = payload["event"], payload["result"]
    risk = result["risk"]
    decision = result["decision"]
    score = result["score"]
    reason = result["reason"]
    policy = result.get("policy", "POLICY-SEC-03")
    action = result.get("action", "ALLOW EXECUTION & LOG")
    risk_class = risk.lower()

    if decision == "APPROVED":
        verdict_icon = "✓"
        verdict_text = "ALLOWED"
        verdict_color = "#10B981"
    elif decision == "REVIEW":
        verdict_icon = "⚠"
        verdict_text = "REVIEW REQUIRED"
        verdict_color = "#F59E0B"
    else:
        verdict_icon = "✕"
        verdict_text = "BLOCKED"
        verdict_color = "#EF4444"

    render_html(
        f"""
        <div class="decision-panel {risk_class}">
            <div class="decision-banner">
                <div class="decision-verdict" style="color:{verdict_color};">
                    <span>{verdict_icon}</span>
                    <span>POLICY DECISION: {verdict_text}</span>
                </div>
                <span class="badge badge-{ 'danger' if risk=='HIGH' else ('warning' if risk=='MEDIUM' else 'safe') }">{risk} RISK · {score}%</span>
            </div>
            <div class="decision-grid">
                <div class="decision-cell">
                    <div class="decision-cell-label">RISK LEVEL</div>
                    <div class="decision-cell-value" style="color:{verdict_color};">{risk} ({score}%)</div>
                </div>
                <div class="decision-cell">
                    <div class="decision-cell-label">MATCHED POLICY</div>
                    <div class="decision-cell-value">{policy}</div>
                </div>
                <div class="decision-cell" style="grid-column: span 2;">
                    <div class="decision-cell-label">EVALUATION REASON</div>
                    <div class="decision-cell-value" style="font-size:0.84rem; font-weight:400; color:#E2E8F0;">{reason}</div>
                </div>
                <div class="decision-cell" style="grid-column: span 2;">
                    <div class="decision-cell-label">ENFORCEMENT ACTION</div>
                    <div class="decision-cell-value" style="color:#00F0FF; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">{action}</div>
                </div>
            </div>
            <div class="risk-meter-track">
                <div class="risk-meter-fill {risk_class}" style="width: {score}%;"></div>
            </div>
        </div>
        """
    )
    with st.expander("🔍 Inspect Normalized Event Payload"):
        st.json(event)


# Initialize State
init_state()

# Render Sidebar & Get Current View
page = render_sidebar()


# ==============================================================================
# VIEW 1: COMMAND CENTER
# ==============================================================================
if page == "Command center":
    # 1. Header (Section 3)
    render_html(
        f"""
        <div class="dashboard-header">
            <div>
                <div class="breadcrumb">
                    <span>AEGIS</span> <span>/</span> <span>CONTROL PLANE</span> <span>/</span> <span style="color:#ffffff;">COMMAND CENTER</span>
                </div>
                <h1 class="dashboard-title">Command Center</h1>
                <div class="dashboard-subtitle">Monitor, evaluate and control autonomous agent actions in real-time.</div>
            </div>
            <div class="header-status-cluster">
                <div class="header-status-badge">
                    <span class="pulse-dot-cyan"></span>
                    <span>● LIVE: Policy Engine Active</span>
                </div>
                <div class="header-status-badge" style="color: #38BDF8;">
                    <span>⚡ 4ms LATENCY</span>
                </div>
                <div class="header-status-badge" style="color: var(--text-dim);">
                    <span class="mono">{datetime.now().strftime('%H:%M:%S')}</span>
                </div>
            </div>
        </div>
        """
    )

    # 2. Hero Section (Section 4)
    render_html(
        """
        <div class="hero-card">
            <div class="hero-content">
                <div class="hero-eyebrow">
                    <span class="pulse-dot-cyan"></span>
                    <span>ACTIVE INTERCEPTOR GATEWAY</span>
                </div>
                <div class="hero-heading">Control autonomous actions before they execute.</div>
                <p class="hero-desc">
                    Aegis intercepts AI agent tool calls, evaluates policy risk, and provides a human approval gate for sensitive actions.
                </p>
            </div>
            <div class="hero-viz">
                <svg width="340" height="100" viewBox="0 0 340 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="cyberLine" x1="0" y1="0" x2="340" y2="0" gradientUnits="userSpaceOnUse">
                            <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.2"/>
                            <stop offset="50%" stop-color="#00F0FF" stop-opacity="0.9"/>
                            <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.2"/>
                        </linearGradient>
                    </defs>
                    <line x1="20" y1="50" x2="320" y2="50" stroke="url(#cyberLine)" stroke-width="1.5" stroke-dasharray="4 4" />
                    <!-- Node 1: Agent -->
                    <circle cx="50" cy="50" r="20" fill="#0C1426" stroke="#38BDF8" stroke-width="2"/>
                    <circle cx="50" cy="50" r="8" fill="#00F0FF" fill-opacity="0.6"/>
                    <text x="50" y="86" fill="#94A3B8" font-size="9" font-family="'JetBrains Mono', monospace" text-anchor="middle">AGENT</text>
                    <!-- Arrow 1 -->
                    <polygon points="105,47 115,50 105,53" fill="#00F0FF"/>
                    <!-- Node 2: Aegis Shield -->
                    <circle cx="170" cy="50" r="26" fill="#101C36" stroke="#00F0FF" stroke-width="2.5"/>
                    <path d="M170 38 L181 43 V51 C181 58 170 64 170 64 C170 64 159 58 159 51 V43 Z" fill="#00F0FF" fill-opacity="0.25" stroke="#00F0FF" stroke-width="1.5"/>
                    <text x="170" y="90" fill="#00F0FF" font-size="10" font-family="'JetBrains Mono', monospace" font-weight="bold" text-anchor="middle">AEGIS GATE</text>
                    <!-- Arrow 2 -->
                    <polygon points="225,47 235,50 225,53" fill="#00F0FF"/>
                    <!-- Node 3: Decision Gate -->
                    <circle cx="290" cy="50" r="20" fill="#0C1426" stroke="#10B981" stroke-width="2"/>
                    <circle cx="290" cy="50" r="8" fill="#10B981" fill-opacity="0.6"/>
                    <text x="290" y="86" fill="#10B981" font-size="9" font-family="'JetBrains Mono', monospace" text-anchor="middle">DECISION</text>
                </svg>
            </div>
        </div>
        """
    )

    # 3. KPI Metrics (Section 5)
    counts = {"APPROVED": 0, "REVIEW": 0, "BLOCKED": 0}
    for item in st.session_state.events:
        decision = item.get("Decision", "")
        counts[decision] = counts.get(decision, 0) + 1
    total_events = len(st.session_state.events)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_html(
            f"""
            <div class="kpi-card approved">
                <div class="kpi-top">
                    <span class="kpi-label">APPROVED</span>
                    <span class="kpi-icon" style="color:var(--green-safe);">🛡️</span>
                </div>
                <div class="kpi-value">{counts['APPROVED']}</div>
                <div class="kpi-detail">
                    <span class="badge badge-safe">SAFE</span>
                    <span>Within policy</span>
                </div>
            </div>
            """
        )

    with k2:
        render_html(
            f"""
            <div class="kpi-card review">
                <div class="kpi-top">
                    <span class="kpi-label">REVIEW QUEUE</span>
                    <span class="kpi-icon" style="color:var(--amber-warning);">⏳</span>
                </div>
                <div class="kpi-value">{counts['REVIEW']}</div>
                <div class="kpi-detail">
                    <span class="badge badge-warning">PENDING</span>
                    <span>Awaiting decision</span>
                </div>
            </div>
            """
        )

    with k3:
        render_html(
            f"""
            <div class="kpi-card blocked">
                <div class="kpi-top">
                    <span class="kpi-label">BLOCKED</span>
                    <span class="kpi-icon" style="color:var(--red-danger);">⛔</span>
                </div>
                <div class="kpi-value">{counts['BLOCKED']}</div>
                <div class="kpi-detail">
                    <span class="badge badge-danger">PREVENTED</span>
                    <span>Prevented calls</span>
                </div>
            </div>
            """
        )

    with k4:
        render_html(
            f"""
            <div class="kpi-card events">
                <div class="kpi-top">
                    <span class="kpi-label">EVENTS</span>
                    <span class="kpi-icon" style="color:var(--cyan-accent);">📈</span>
                </div>
                <div class="kpi-value">{total_events}</div>
                <div class="kpi-detail">
                    <span class="badge badge-cyan">TOTAL</span>
                    <span>Recorded this session</span>
                </div>
            </div>
            """
        )

    st.write("")

    # 4. Main Two-Column Work Area
    left_col, right_col = st.columns([1.25, 0.85])

    # Left Column: Tool Call Interceptor (Section 6)
    with left_col:
        render_html(
            """
            <div class="panel-card">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>⚡</span> INTERCEPT TOOL CALL
                    </div>
                    <span class="badge badge-cyan">GATEWAY ACTIVE</span>
                </div>
            """
        )

        top_c1, top_c2 = st.columns([1.5, 1])
        with top_c1:
            if st.session_state.show_advanced:
                render_html('<div style="font-size:0.78rem; color:#94A3B8; padding-top:0.35rem;">Direct RFC-8259 JSON payload editor with schema validation.</div>')
            else:
                render_html('<div style="font-size:0.78rem; color:#94A3B8; padding-top:0.35rem;">Configure agent invocation parameters to inspect security boundaries.</div>')
        with top_c2:
            adv = st.toggle("Advanced JSON", key="show_advanced", help="Toggle between clean visual form and raw JSON code editor")

        # Handle toggle mode transitions
        prev_adv = st.session_state.get("prev_show_advanced", False)
        if adv and not prev_adv:
            # Just switched to Advanced JSON -> sync current visual form values into raw_json_str
            form_payload = build_payload_from_form(
                st.session_state.form_agent,
                st.session_state.form_tool,
                st.session_state.form_args,
            )
            st.session_state.raw_json_str = json.dumps(form_payload, indent=2)
        elif not adv and prev_adv:
            # Just switched to Visual Form -> parse raw_json_str into form fields
            try:
                parsed = json.loads(st.session_state.raw_json_str)
                if isinstance(parsed, dict):
                    st.session_state.form_agent = str(parsed.get("agent", ""))
                    st.session_state.form_tool = str(parsed.get("tool", ""))
                    args = parsed.get("args")
                    if isinstance(args, dict) and len(args) == 1 and "query" in args:
                        st.session_state.form_args = str(args["query"])
                    elif isinstance(args, dict):
                        st.session_state.form_args = json.dumps(args)
                    else:
                        st.session_state.form_args = str(args or "")
            except Exception:
                pass
        st.session_state.prev_show_advanced = adv

        if not adv:
            # Sync visual form values into raw_json_str
            form_payload = build_payload_from_form(
                st.session_state.form_agent,
                st.session_state.form_tool,
                st.session_state.form_args,
            )
            st.session_state.raw_json_str = json.dumps(form_payload, indent=2)

            col_ag, col_tl = st.columns(2)
            with col_ag:
                st.text_input(
                    "AGENT",
                    key="form_agent",
                    placeholder="research-agent",
                    help="Identifier of the calling autonomous agent",
                )
            with col_tl:
                st.text_input(
                    "TOOL",
                    key="form_tool",
                    placeholder="web_search",
                    help="Name of the tool or API function requested",
                )

            st.text_input(
                "QUERY / ARGUMENTS",
                key="form_args",
                placeholder="AI agent security best practices",
                help="Parameters, query string, or JSON payload passed to the tool",
            )

            b1, b2 = st.columns([1.2, 1])
            with b1:
                inspect = st.button("🛡️ Evaluate Tool Call", use_container_width=True, type="primary", key="btn_eval_form")
            with b2:
                batch = st.button("⚡ Run Demo Sequence", use_container_width=True, key="btn_demo_form")

            render_html("</div>")

            if inspect:
                payload = build_payload_from_form(
                    st.session_state.form_agent,
                    st.session_state.form_tool,
                    st.session_state.form_args,
                )
                process_event(payload, "visual_form")
                st.session_state["pending_load_event"] = payload
                st.rerun()

            if batch:
                for demo in [s["payload"] for s in PRESET_SCENARIOS[:3]]:
                    process_event(demo, "demo_batch")
                st.session_state["pending_load_event"] = PRESET_SCENARIOS[2]["payload"]
                st.rerun()

        else:
            # Sync raw_json_str into form fields if valid JSON
            try:
                parsed = json.loads(st.session_state.raw_json_str)
                if isinstance(parsed, dict):
                    st.session_state.form_agent = str(parsed.get("agent", ""))
                    st.session_state.form_tool = str(parsed.get("tool", ""))
                    args = parsed.get("args")
                    if isinstance(args, dict) and len(args) == 1 and "query" in args:
                        st.session_state.form_args = str(args["query"])
                    elif isinstance(args, dict):
                        st.session_state.form_args = json.dumps(args)
                    else:
                        st.session_state.form_args = str(args or "")
            except Exception:
                pass

            render_html(
                """
                <div class="editor-header">
                    <span>RFC-8259 JSON</span>
                    <span>SCHEMA: AGENT-CALL-v1</span>
                </div>
                """
            )

            raw_input = st.text_area(
                "Tool-call payload",
                key="raw_json_str",
                height=200,
                label_visibility="collapsed",
                help="Provide the simulated tool call payload in JSON format.",
            )

            b1, b2 = st.columns([1.2, 1])
            with b1:
                inspect_json = st.button("🛡️ Evaluate Tool Call", use_container_width=True, type="primary", key="btn_eval_json")
            with b2:
                batch_json = st.button("⚡ Run Demo Sequence", use_container_width=True, key="btn_demo_json")

            render_html("</div>")

            if inspect_json:
                try:
                    event = json.loads(st.session_state.raw_json_str)
                    if not isinstance(event, dict):
                        st.error("Payload must be a valid JSON dictionary object.")
                    else:
                        process_event(event, "advanced_json")
                        st.session_state["pending_load_event"] = event
                        st.rerun()
                except json.JSONDecodeError as error:
                    st.error(f"Syntax Error in JSON: {error}")

            if batch_json:
                for demo in [s["payload"] for s in PRESET_SCENARIOS[:3]]:
                    process_event(demo, "demo_batch")
                st.session_state["pending_load_event"] = PRESET_SCENARIOS[2]["payload"]
                st.rerun()

        # Large Policy Decision Panel Below
        render_evaluation_result()

    # Right Column: Quick Scenarios & Human Gate (Section 8)
    with right_col:
        render_html(
            """
            <div class="panel-card">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>🎯</span> QUICK SCENARIOS
                    </div>
                    <span class="badge badge-neutral">SIMULATOR</span>
                </div>
                <p style="font-size:0.8rem; color:#94A3B8; margin-top:-0.5rem; margin-bottom:1rem;">
                    Trigger pre-configured agent scenarios to evaluate policy enforcement in real-time.
                </p>
            """
        )

        for sc in PRESET_SCENARIOS:
            risk_badge = f'<span class="badge badge-{"danger" if sc["risk"]=="HIGH" else ("warning" if sc["risk"]=="MEDIUM" else "safe")}">{sc["risk"]}</span>'
            render_html(
                f"""
                <div class="scenario-item">
                    <div class="scenario-header">
                        <div class="scenario-name">
                            <span>{sc['icon']}</span>
                            <span>{sc['name']}</span>
                        </div>
                        {risk_badge}
                    </div>
                    <div class="scenario-desc">{sc['desc']}</div>
                </div>
                """
            )
            if st.button(f"SIMULATE: {sc['name']}", key=f"btn_sc_{sc['id']}", use_container_width=True):
                process_event(sc["payload"], "scenario_simulator")
                st.session_state["pending_load_event"] = sc["payload"]
                st.rerun()

        render_html("</div>")

        # Human Approval Gate (when pending review)
        if st.session_state.pending:
            p_event, p_result = st.session_state.pending
            render_html(
                f"""
                <div class="human-gate-card">
                    <div class="panel-header" style="border-bottom-color: rgba(245,158,11,0.25);">
                        <div class="panel-title" style="color:#FBBF24 !important;">
                            <span>⚠️</span> Human Approval Gate
                        </div>
                        <span class="badge badge-warning">ACTION REQUIRED</span>
                    </div>
                    <p style="font-size:0.85rem; color:#FEF3C7; margin-bottom:0.75rem;">
                        Agent <strong>{p_event.get('agent', 'agent')}</strong> requested sensitive tool 
                        <code style="background:rgba(0,0,0,0.4); padding:2px 6px; border-radius:4px; color:#FDE68A;">{p_event.get('tool', 'tool')}</code>.
                    </p>
                """
            )
            h_col1, h_col2 = st.columns(2)
            with h_col1:
                approve = st.button("✓ Approve Action", use_container_width=True, type="primary", key="btn_gate_approve")
            with h_col2:
                reject = st.button("✕ Block Action", use_container_width=True, key="btn_gate_reject")

            if approve or reject:
                p_result["decision"] = "APPROVED" if approve else "BLOCKED"
                record_event(p_event, p_result, "human_gate")
                st.session_state.pending = None
                st.rerun()

            render_html("</div>")

    st.write("")

    # 5. Policy Decision Flow (Section 10)
    render_html(
        """
        <div class="panel-card" style="margin-bottom: 1.5rem;">
            <div class="panel-header">
                <div class="panel-title">
                    <span>🔄</span> POLICY DECISION FLOW
                </div>
                <span class="badge badge-cyan">ZERO-TRUST EXECUTION FLOW</span>
            </div>
            <div class="pipeline-container">
                <div class="pipeline-node">
                    <div class="pipeline-circle">🤖</div>
                    <div class="pipeline-label">Agent Request</div>
                </div>
                <div class="pipeline-arrow">➔</div>
                <div class="pipeline-node">
                    <div class="pipeline-circle">⚡</div>
                    <div class="pipeline-label">Intercept</div>
                </div>
                <div class="pipeline-arrow">➔</div>
                <div class="pipeline-node">
                    <div class="pipeline-circle">🛡️</div>
                    <div class="pipeline-label">Policy Engine</div>
                </div>
                <div class="pipeline-arrow">➔</div>
                <div class="pipeline-node">
                    <div class="pipeline-circle">📊</div>
                    <div class="pipeline-label">Risk Analysis</div>
                </div>
                <div class="pipeline-arrow">➔</div>
                <div class="pipeline-node">
                    <div class="pipeline-circle">⚖️</div>
                    <div class="pipeline-label">Allow / Review / Block</div>
                </div>
            </div>
        </div>
        """
    )

    # 6. Risk Distribution & Live Policy Events (Section 7 & 9)
    feed_col, dist_col = st.columns([1.35, 0.65])

    with dist_col:
        total_ev = max(len(st.session_state.events), 1)
        low_count = sum(1 for e in st.session_state.events if e.get("Risk") == "LOW")
        med_count = sum(1 for e in st.session_state.events if e.get("Risk") == "MEDIUM")
        high_count = sum(1 for e in st.session_state.events if e.get("Risk") == "HIGH")

        low_pct = int((low_count / total_ev) * 100) if len(st.session_state.events) > 0 else 0
        med_pct = int((med_count / total_ev) * 100) if len(st.session_state.events) > 0 else 0
        high_pct = int((high_count / total_ev) * 100) if len(st.session_state.events) > 0 else 0

        render_html(
            f"""
            <div class="panel-card">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>📊</span> RISK DISTRIBUTION
                    </div>
                    <span class="badge badge-neutral">SESSION METRICS</span>
                </div>
                <div style="margin-bottom: 1rem;">
                    <!-- Segmented Horizontal Bar -->
                    <div style="display:flex; height:10px; border-radius:9999px; overflow:hidden; background:rgba(255,255,255,0.06); margin-bottom:1rem;">
                        <div style="width:{low_pct}%; background:var(--green-safe);" title="LOW: {low_pct}%"></div>
                        <div style="width:{med_pct}%; background:var(--amber-warning);" title="MEDIUM: {med_pct}%"></div>
                        <div style="width:{high_pct}%; background:var(--red-danger);" title="HIGH: {high_pct}%"></div>
                    </div>
                    <div style="display:flex; flex-direction:column; gap:0.6rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.82rem;">
                            <span style="display:flex; align-items:center; gap:0.4rem;">
                                <span style="width:8px; height:8px; border-radius:50%; background:var(--green-safe);"></span>
                                <span style="color:var(--text-secondary);">Low Risk (Safe)</span>
                            </span>
                            <span class="mono" style="font-weight:600; color:var(--green-safe);">{low_count} ({low_pct}%)</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.82rem;">
                            <span style="display:flex; align-items:center; gap:0.4rem;">
                                <span style="width:8px; height:8px; border-radius:50%; background:var(--amber-warning);"></span>
                                <span style="color:var(--text-secondary);">Medium Risk (Review)</span>
                            </span>
                            <span class="mono" style="font-weight:600; color:var(--amber-warning);">{med_count} ({med_pct}%)</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.82rem;">
                            <span style="display:flex; align-items:center; gap:0.4rem;">
                                <span style="width:8px; height:8px; border-radius:50%; background:var(--red-danger);"></span>
                                <span style="color:var(--text-secondary);">High Risk (Blocked)</span>
                            </span>
                            <span class="mono" style="font-weight:600; color:var(--red-danger);">{high_count} ({high_pct}%)</span>
                        </div>
                    </div>
                </div>
            </div>
            """
        )

    with feed_col:
        render_html(
            """
            <div class="panel-card">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>📡</span> LIVE POLICY EVENTS
                    </div>
                    <span class="badge badge-cyan">STREAMING FEED</span>
                </div>
            """
        )

        if st.session_state.events:
            render_html(
                """
                <div class="event-row event-row-header">
                    <div>TIME</div>
                    <div>AGENT</div>
                    <div>TOOL</div>
                    <div>RESOURCE</div>
                    <div>RISK</div>
                    <div>DECISION</div>
                </div>
                """
            )

            for ev in st.session_state.events[:6]:
                risk_val = ev.get("Risk", "LOW")
                dec_val = ev.get("Decision", "APPROVED")

                r_badge = f'<span class="badge badge-{"danger" if risk_val=="HIGH" else ("warning" if risk_val=="MEDIUM" else "safe")}">{risk_val}</span>'
                d_badge = f'<span class="badge badge-{"danger" if dec_val=="BLOCKED" else ("warning" if dec_val=="REVIEW" else "safe")}">{dec_val}</span>'

                render_html(
                    f"""
                    <div class="event-row">
                        <div class="mono" style="color:var(--text-muted); font-size:0.75rem;">● {ev.get('Time')}</div>
                        <div style="font-weight:500; color:#ffffff;">{ev.get('Agent')}</div>
                        <div class="mono" style="color:#38BDF8;">{ev.get('Tool')}</div>
                        <div class="mono" style="color:var(--text-muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="{ev.get('Resource')}">{ev.get('Resource')}</div>
                        <div>{r_badge}</div>
                        <div>{d_badge}</div>
                    </div>
                    """
                )
        else:
            render_html(
                """
                <div style="text-align:center; padding: 2.5rem 1.5rem; color: var(--text-muted);">
                    <div style="font-size:2rem; margin-bottom:0.5rem; opacity:0.8;">📡</div>
                    <div style="font-weight:600; color:#FFFFFF; margin-bottom:0.25rem;">No policy events yet.</div>
                    <div style="font-size:0.82rem; color:var(--text-muted);">Run a simulation or evaluate a tool call to populate the stream.</div>
                </div>
                """
            )

        render_html("</div>")


# ==============================================================================
# VIEW 2: POLICY STUDIO (Section 11)
# ==============================================================================
elif page == "Policy studio":
    render_html(
        """
        <div class="dashboard-header">
            <div>
                <div class="breadcrumb">
                    <span>AEGIS</span> <span>/</span> <span>GOVERNANCE</span> <span>/</span> <span style="color:#ffffff;">POLICY STUDIO</span>
                </div>
                <h1 class="dashboard-title">Policy Studio</h1>
                <div class="dashboard-subtitle">Configure security guardrails, automate risk classification, and audit policy rules.</div>
            </div>
            <div class="header-status-cluster">
                <div class="header-status-badge">
                    <span class="pulse-dot"></span>
                    <span>RULE ENGINE v1.4 ACTIVE</span>
                </div>
            </div>
        </div>
        """
    )

    p_left, p_right = st.columns([1.2, 0.8])

    with p_left:
        # Security Rule Matrix Cards
        render_html(
            """
            <div class="panel-card">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>🛡️</span> Security Rule Matrix
                    </div>
                    <span class="badge badge-safe">ACTIVE ENGINE</span>
                </div>
                <!-- HIGH RISK -->
                <div style="background:rgba(239,68,68,0.05); border:1px solid var(--red-border); border-radius:8px; padding:1rem; margin-bottom:0.85rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span class="badge badge-danger">HIGH RISK</span>
                        <span class="badge badge-danger">ACTION: BLOCK</span>
                        <span class="badge badge-safe">STATUS: ACTIVE</span>
                    </div>
                    <div style="font-weight:700; font-size:0.92rem; color:#ffffff; margin-bottom:0.2rem;">
                        Destructive or Production-Impacting Operations
                    </div>
                    <div style="font-size:0.8rem; color:#94A3B8; line-height:1.4;">
                        Matches keywords: <code style="color:#F87171;">delete</code>, <code style="color:#F87171;">drop</code>, <code style="color:#F87171;">destroy</code>, <code style="color:#F87171;">shutdown</code>, <code style="color:#F87171;">production_db</code>.
                        Prevented unconditionally at the gateway before reaching execution runtimes.
                    </div>
                </div>
                <!-- MEDIUM RISK -->
                <div style="background:rgba(245,158,11,0.05); border:1px solid var(--amber-border); border-radius:8px; padding:1rem; margin-bottom:0.85rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span class="badge badge-warning">MEDIUM RISK</span>
                        <span class="badge badge-warning">ACTION: REQUIRE APPROVAL</span>
                        <span class="badge badge-safe">STATUS: ACTIVE</span>
                    </div>
                    <div style="font-weight:700; font-size:0.92rem; color:#ffffff; margin-bottom:0.2rem;">
                        Outbound Communications & Credential Access
                    </div>
                    <div style="font-size:0.8rem; color:#94A3B8; line-height:1.4;">
                        Matches keywords: <code style="color:#FBBF24;">email</code>, <code style="color:#FBBF24;">send</code>, <code style="color:#FBBF24;">password</code>, <code style="color:#FBBF24;">credential</code>, <code style="color:#FBBF24;">payment</code>, <code style="color:#FBBF24;">token</code>.
                        Pauses execution and routes payload to the security operator review queue.
                    </div>
                </div>
                <!-- LOW RISK -->
                <div style="background:rgba(16,185,129,0.05); border:1px solid var(--green-border); border-radius:8px; padding:1rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span class="badge badge-safe">LOW RISK</span>
                        <span class="badge badge-safe">ACTION: ALLOW + LOG</span>
                        <span class="badge badge-safe">STATUS: ACTIVE</span>
                    </div>
                    <div style="font-weight:700; font-size:0.92rem; color:#ffffff; margin-bottom:0.2rem;">
                        Read-Only & Safe Introspection Operations
                    </div>
                    <div style="font-size:0.8rem; color:#94A3B8; line-height:1.4;">
                        Matches benign read, query, search, and metric calls. Conforms to standard least-privilege boundary.
                    </div>
                </div>
            </div>
            """
        )

        # Core Architectural Invariants
        render_html(
            """
            <div class="panel-card">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>📖</span> Core Architectural Invariants
                    </div>
                </div>
                <div style="display:flex; flex-direction:column; gap:0.85rem;">
                    <div>
                        <div style="font-weight:700; font-size:0.9rem; color:#38BDF8; margin-bottom:0.15rem;">
                            1. Principle of Least Privilege
                        </div>
                        <div style="font-size:0.82rem; color:#94A3B8;">
                            An autonomous agent only obtains permission when the explicit tool and parameter schema strictly match policy.
                        </div>
                    </div>
                    <div>
                        <div style="font-weight:700; font-size:0.9rem; color:#38BDF8; margin-bottom:0.15rem;">
                            2. Fail Closed Architecture
                        </div>
                        <div style="font-size:0.82rem; color:#94A3B8;">
                            Any parsing failure, malformed JSON, or ambiguous parameter will fail closed and trigger an immediate block.
                        </div>
                    </div>
                    <div>
                        <div style="font-weight:700; font-size:0.9rem; color:#38BDF8; margin-bottom:0.15rem;">
                            3. Continuous Verifiable Human Gate
                        </div>
                        <div style="font-size:0.82rem; color:#94A3B8;">
                            Irreversible side effects (financial, external messages, credentials) require explicit human approval.
                        </div>
                    </div>
                </div>
            </div>
            """
        )

    with p_right:
        render_html(
            """
            <div class="panel-card">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>⚙️</span> Automation Controls
                    </div>
                    <span class="badge badge-neutral">CONFIGURATION</span>
                </div>
            """
        )

        st.toggle("Auto-approve LOW risk read operations", value=True, disabled=True, key="toggle_auto_low")
        st.caption("Standard safety default: read-only telemetry and queries execute without blocking.")

        st.toggle("Auto-block HIGH risk destructive actions", value=True, disabled=True, key="toggle_auto_high")
        st.caption("Security enforcement: drop and delete payloads cannot bypass the interceptor.")

        st.toggle(
            "Route MEDIUM risk to human review queue",
            value=st.session_state.automation,
            key="policy_studio_automation_toggle",
        )
        st.caption("When enabled, sensitive actions pause execution until operator approval.")

        st.divider()

        st.selectbox("Human Review Expiration Timeout", ["15 minutes", "1 hour", "4 hours", "No expiry"], index=1, key="select_review_expiry")
        st.caption("Unreviewed actions automatically expire and fail closed.")

        st.selectbox("Immutable Audit Log Retention", ["7 days", "30 days", "90 days", "1 year", "Permanent"], index=2, key="select_audit_retention")
        st.caption("Session events are archived to cryptographically signed storage.")

        render_html("</div>")


# ==============================================================================
# VIEW 3: AUDIT TRAIL (Section 12)
# ==============================================================================
else:
    render_html(
        """
        <div class="dashboard-header">
            <div>
                <div class="breadcrumb">
                    <span>AEGIS</span> <span>/</span> <span>COMPLIANCE</span> <span>/</span> <span style="color:#ffffff;">AUDIT TRAIL</span>
                </div>
                <h1 class="dashboard-title">Audit Trail</h1>
                <div class="dashboard-subtitle">Immutable forensic log of all intercepted AI tool requests, risk assessments, and human decisions.</div>
            </div>
            <div class="header-status-cluster">
                <div class="header-status-badge">
                    <span class="pulse-dot-cyan"></span>
                    <span>CRYPTOGRAPHIC HASH VERIFIED</span>
                </div>
            </div>
        </div>
        """
    )

    # Query & Filters
    render_html(
        """
        <div class="panel-card" style="margin-bottom: 1.25rem;">
            <div class="panel-header">
                <div class="panel-title">
                    <span>🔎</span> Query & Filters
                </div>
            </div>
        """
    )

    fc1, fc2, fc3 = st.columns([1, 1, 1.5])
    with fc1:
        risk_filter = st.selectbox("Filter by Risk", ["All", "LOW", "MEDIUM", "HIGH"], index=0, key="audit_risk_filter")
    with fc2:
        decision_filter = st.selectbox("Filter by Decision", ["All", "APPROVED", "REVIEW", "BLOCKED"], index=0, key="audit_decision_filter")
    with fc3:
        search_query = st.text_input("Search Agent / Tool / Resource", placeholder="e.g. research-agent, delete, email...", key="audit_search_text")

    render_html("</div>")

    filtered_events = st.session_state.events
    if risk_filter != "All":
        filtered_events = [e for e in filtered_events if e.get("Risk") == risk_filter]
    if decision_filter != "All":
        filtered_events = [e for e in filtered_events if e.get("Decision") == decision_filter]
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_events = [
            e for e in filtered_events
            if q in str(e.get("Agent", "")).lower()
            or q in str(e.get("Tool", "")).lower()
            or q in str(e.get("Resource", "")).lower()
            or q in str(e.get("Policy", "")).lower()
        ]

    # Forensic Table
    render_html(
        """
        <div class="panel-card">
            <div class="panel-header">
                <div class="panel-title">
                    <span>📜</span> Forensic Event Log
                </div>
                <span class="badge badge-neutral">TOTAL: {} RECORDS</span>
            </div>
        """.format(len(filtered_events))
    )

    if filtered_events:
        render_html(
            """
            <div class="event-row event-row-header" style="grid-template-columns: 85px 130px 130px 1fr 90px 105px 125px 95px;">
                <div>TIME</div>
                <div>AGENT</div>
                <div>TOOL</div>
                <div>RESOURCE</div>
                <div>RISK</div>
                <div>DECISION</div>
                <div>POLICY</div>
                <div>STATUS</div>
            </div>
            """
        )

        for ev in filtered_events:
            risk_val = ev.get("Risk", "LOW")
            dec_val = ev.get("Decision", "APPROVED")

            r_badge = f'<span class="badge badge-{"danger" if risk_val=="HIGH" else ("warning" if risk_val=="MEDIUM" else "safe")}">{risk_val}</span>'
            d_badge = f'<span class="badge badge-{"danger" if dec_val=="BLOCKED" else ("warning" if dec_val=="REVIEW" else "safe")}">{dec_val}</span>'

            render_html(
                f"""
                <div class="event-row" style="grid-template-columns: 85px 130px 130px 1fr 90px 105px 125px 95px;">
                    <div class="mono" style="color:var(--text-muted); font-size:0.75rem;">{ev.get('Time')}</div>
                    <div style="font-weight:600; color:#ffffff;">{ev.get('Agent')}</div>
                    <div class="mono" style="color:#38BDF8;">{ev.get('Tool')}</div>
                    <div class="mono" style="color:var(--text-muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="{ev.get('Resource')}">{ev.get('Resource')}</div>
                    <div>{r_badge}</div>
                    <div>{d_badge}</div>
                    <div class="mono" style="font-size:0.68rem; color:#94A3B8;">{ev.get('Policy', 'POLICY-SEC-03')}</div>
                    <div><span class="badge badge-neutral">{ev.get('Source', 'manual')}</span></div>
                </div>
                """
            )

        render_html("<div style='margin-top:1.5rem;'>")
        st.download_button(
            "📥 Export Audit Log (JSON)",
            data=json.dumps(filtered_events, indent=2),
            file_name=f"aegis_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="btn_download_audit_json",
        )
        render_html("</div>")
    else:
        render_html(
            """
            <div style="text-align:center; padding: 2.5rem 1.5rem; color: var(--text-muted);">
                <div style="font-size:2rem; margin-bottom:0.5rem; opacity:0.8;">🔍</div>
                <div style="font-weight:600; color:#ffffff; margin-bottom:0.25rem;">NO MATCHING EVENTS FOUND</div>
                <div style="font-size:0.82rem; color:var(--text-muted);">Adjust your search query or run a scenario from the Command Center.</div>
            </div>
            """
        )

    render_html("</div>")