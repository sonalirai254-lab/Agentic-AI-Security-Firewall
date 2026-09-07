import json
from datetime import datetime

import streamlit as st


st.set_page_config(
    page_title="Aegis Control Room",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root { --ink:#101820; --paper:#f4f6f2; --muted:#65727a; --line:#d8dfdc; --lime:#c6f36b; --cyan:#8de4de; --orange:#ffb86b; --red:#ff7d76; }
    .stApp { background:var(--paper); color:var(--ink); font-family:'Space Grotesk', sans-serif; }
    [data-testid="stSidebar"] { background:#10242a; border-right:0; }
    [data-testid="stSidebar"] * { color:#dce8e1 !important; }
    [data-testid="stSidebar"] .stRadio label { padding:8px 4px; }
    .block-container { max-width:1500px; padding:2.5rem 3.5rem 4rem; }
    h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif !important; color:var(--ink) !important; letter-spacing:-.03em; }
    h1 { font-size:2.8rem !important; margin-bottom:.25rem !important; }
    h2 { font-size:1.45rem !important; }
    p, label, .stCaption { color:var(--muted) !important; }
    .eyebrow { color:#4e7d52; font:500 12px 'DM Mono',monospace; letter-spacing:.13em; text-transform:uppercase; }
    .topline { display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; margin-bottom:2.3rem; }
    .live { background:var(--ink); color:var(--lime); border-radius:99px; padding:9px 15px; font:500 12px 'DM Mono',monospace; letter-spacing:.08em; white-space:nowrap; }
    .hero { background:var(--ink); border-radius:18px; padding:26px 30px; color:#e9f5ea; min-height:170px; position:relative; overflow:hidden; }
    .hero:after { content:'◈'; position:absolute; right:36px; top:10px; font-size:130px; color:#244148; transform:rotate(18deg); }
    .hero h2 { color:#f4f8ee !important; margin:0 0 10px; font-size:1.8rem !important; position:relative; z-index:1; }
    .hero p { color:#aec0ba !important; max-width:650px; position:relative; z-index:1; }
    .metric { background:#fff; border:1px solid var(--line); border-radius:14px; padding:18px 20px; min-height:112px; }
    .metric .label { color:var(--muted); font:500 11px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.08em; }
    .metric .value { color:var(--ink); font-size:2.3rem; font-weight:700; margin-top:8px; }
    .metric .detail { color:#4e7d52; font-size:12px; }
    .panel { background:#fff; border:1px solid var(--line); border-radius:14px; padding:22px; }
    .panel-title { display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; }
    .panel-title h3 { margin:0; font-size:1.08rem; }
    .mono { font:13px 'DM Mono',monospace; }
    .signal { border-radius:12px; padding:18px; border-left:5px solid; margin:8px 0 16px; }
    .signal.low { background:#edf9d9; border-color:#78ad38; }
    .signal.medium { background:#fff2dc; border-color:#dc912d; }
    .signal.high { background:#ffe4e2; border-color:#df5c57; }
    .signal strong { color:var(--ink); font-size:1.15rem; }
    .tag { display:inline-block; border-radius:99px; padding:4px 9px; font:500 11px 'DM Mono',monospace; }
    .tag.low { background:#dff4ad; color:#3e661a; } .tag.medium { background:#ffe1ae; color:#8c5a16; } .tag.high { background:#ffd0cd; color:#943c38; }
    .small-note { color:var(--muted); font-size:12px; }
    div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
    .stButton > button { border-radius:9px; border:1px solid #bdc9c5; min-height:42px; font-weight:600; color:var(--ink); background:#fff; }
    .stButton > button:hover { border-color:#4e7d52; color:#315536; }
    .stTextArea textarea, .stTextInput input { background:#fbfcfa !important; color:var(--ink) !important; border:1px solid #cbd5d0 !important; border-radius:9px !important; font-family:'DM Mono',monospace !important; }
    .stSelectbox div[data-baseweb="select"] > div { background:#fff; border-color:#cbd5d0; }
    .stProgress > div > div { background:#78ad38; }
    hr { border-color:var(--line); }
    </style>
    """,
    unsafe_allow_html=True,
)


DEFAULT_EVENTS = [
    {"agent": "research-agent", "tool": "read_file", "action": "read", "resource": "briefing.md"},
    {"agent": "support-agent", "tool": "send_email", "action": "send", "resource": "customer@example.com"},
    {"agent": "ops-agent", "tool": "delete_database", "action": "delete", "resource": "production_db"},
]


def init_state():
    defaults = {"events": [], "pending": None, "automation": True, "last_result": None}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def evaluate(event):
    combined = " ".join(str(event.get(key, "")).lower() for key in ("tool", "action", "resource"))
    if any(word in combined for word in ("delete", "drop", "destroy", "shutdown", "format", "production_db")):
        return {"risk": "HIGH", "score": 95, "decision": "BLOCKED", "reason": "Destructive or production-impacting operation detected."}
    if any(word in combined for word in ("email", "send", "password", "credential", "upload", "payment", "token")):
        return {"risk": "MEDIUM", "score": 60, "decision": "REVIEW", "reason": "Sensitive data or outbound communication requires an operator decision."}
    return {"risk": "LOW", "score": 15, "decision": "APPROVED", "reason": "Operation matches the current least-privilege policy."}


def record_event(event, result, source="manual"):
    st.session_state.events.insert(0, {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Agent": event.get("agent", "unknown"),
        "Tool": event.get("tool", "unknown"),
        "Resource": event.get("resource", "unknown"),
        "Risk": result["risk"],
        "Score": f'{result["score"]}%',
        "Decision": result["decision"],
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


def render_result():
    payload = st.session_state.last_result
    if not payload:
        return
    event, result = payload["event"], payload["result"]
    risk_class = result["risk"].lower()
    st.markdown(f'<div class="signal {risk_class}"><span class="tag {risk_class}">{result["risk"]} RISK · {result["score"]}%</span><br><strong>{result["decision"]}</strong><br><span class="small-note">{result["reason"]}</span></div>', unsafe_allow_html=True)
    with st.expander("View normalized event payload"):
        st.json(event)


def render_sidebar():
    with st.sidebar:
        st.markdown("<div class='eyebrow'>AEGIS // CONTROL ROOM</div>", unsafe_allow_html=True)
        st.markdown("## Agent firewall")
        st.caption("A policy cockpit for autonomous tool calls.")
        page = st.radio("Workspace", ["Command center", "Policy studio", "Audit trail"], label_visibility="collapsed")
        st.divider()
        st.markdown("**Automation layer**")
        automation = st.toggle("Route sensitive calls to review", value=st.session_state.automation)
        st.session_state.automation = automation
        st.caption("HIGH risk is always blocked. LOW risk is always logged. MEDIUM risk can pause for approval.")
        st.divider()
        st.markdown("**System status**")
        st.markdown("`●` Policy engine online")
        st.markdown("`●` Audit stream recording")
        st.markdown("`●` Human gate armed")
        return page


init_state()
page = render_sidebar()

if page == "Command center":
    st.markdown('<div class="topline"><div><div class="eyebrow">REAL-TIME AGENT GOVERNANCE</div><h1>Command center</h1><p>See what your agents are trying to do, decide what happens next.</p></div><div class="live">● LIVE POLICY ENGINE</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero"><h2>Make autonomy observable.</h2><p>Aegis intercepts tool calls before execution, scores the intent, and gives your team a clean human gate for anything sensitive.</p></div>', unsafe_allow_html=True)
    st.write("")
    counts = {"APPROVED": 0, "REVIEW": 0, "BLOCKED": 0}
    for item in st.session_state.events:
        counts[item["Decision"]] = counts.get(item["Decision"], 0) + 1
    m1, m2, m3, m4 = st.columns(4)
    for column, label, value, detail in [(m1, "APPROVED", counts["APPROVED"], "within policy"), (m2, "REVIEW QUEUE", counts["REVIEW"], "awaiting decision"), (m3, "BLOCKED", counts["BLOCKED"], "prevented calls"), (m4, "EVENTS", len(st.session_state.events), "recorded this session")]:
        with column:
            st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div><div class="detail">{detail}</div></div>', unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.25, .75])
    with left:
        st.markdown('<div class="panel"><div class="panel-title"><h3>Intercept a tool call</h3><span class="tag low">JSON INPUT</span></div>', unsafe_allow_html=True)
        raw = st.text_area("Tool-call payload", value=json.dumps(DEFAULT_EVENTS[0], indent=2), height=210, label_visibility="collapsed")
        c1, c2 = st.columns([1, 1])
        with c1:
            inspect = st.button("Analyze payload", use_container_width=True, type="primary")
        with c2:
            batch = st.button("Run demo sequence", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if inspect:
            try:
                event = json.loads(raw)
                if not isinstance(event, dict):
                    st.error("Payload must be a JSON object.")
                else:
                    process_event(event)
                    st.rerun()
            except json.JSONDecodeError as error:
                st.error(f"Invalid JSON: {error}")
        if batch:
            for demo in DEFAULT_EVENTS:
                process_event(demo, "demo")
            st.rerun()
        render_result()
    with right:
        st.markdown('<div class="panel"><div class="panel-title"><h3>Quick scenarios</h3><span class="tag medium">SIMULATOR</span></div>', unsafe_allow_html=True)
        st.caption("Use these to demonstrate the policy engine without writing JSON.")
        for label, event in [("Read a briefing", DEFAULT_EVENTS[0]), ("Send customer email", DEFAULT_EVENTS[1]), ("Delete production database", DEFAULT_EVENTS[2])]:
            if st.button(label, key=f"scenario_{label}", use_container_width=True):
                process_event(event, "scenario")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if st.session_state.pending:
            event, result = st.session_state.pending
            st.markdown('<div class="panel" style="margin-top:16px"><div class="panel-title"><h3>Human gate</h3><span class="tag medium">ACTION NEEDED</span></div>', unsafe_allow_html=True)
            st.write(f'`{event.get("tool", "tool")}` wants to access `{event.get("resource", "resource")}`.')
            a1, a2 = st.columns(2)
            with a1:
                approve = st.button("Approve", use_container_width=True)
            with a2:
                reject = st.button("Block", use_container_width=True)
            if approve or reject:
                result["decision"] = "APPROVED" if approve else "BLOCKED"
                record_event(event, result, "human gate")
                st.session_state.pending = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "Policy studio":
    st.markdown('<div class="topline"><div><div class="eyebrow">GUARDRAILS // CONFIGURATION</div><h1>Policy studio</h1><p>Make the firewall legible to the whole team, then tune the automation gate.</p></div><div class="live">● POLICY v1.0</div></div>', unsafe_allow_html=True)
    left, right = st.columns([1.1, .9])
    with left:
        st.markdown('<div class="panel"><div class="panel-title"><h3>Decision matrix</h3><span class="tag low">ACTIVE</span></div>', unsafe_allow_html=True)
        st.markdown("| Signal | Risk | Default action |\n|---|---:|---|\n| Read-only internal resource | LOW | Approve + log |\n| Email, upload, token, payment | MEDIUM | Human review |\n| Delete, drop, shutdown, production | HIGH | Block immediately |")
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div class="panel"><div class="panel-title"><h3>Policy principles</h3></div><p><b>Least privilege.</b> A tool call earns access only when its intent is clear.</p><p><b>Fail closed.</b> Destructive operations never bypass the firewall.</p><p><b>Human accountability.</b> Sensitive outbound actions pause with a visible owner.</p></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="panel-title"><h3>Automation controls</h3></div>', unsafe_allow_html=True)
        st.toggle("Auto-approve LOW risk", value=True, disabled=True)
        st.toggle("Auto-block HIGH risk", value=True, disabled=True)
        st.toggle("Pause MEDIUM risk for human review", value=st.session_state.automation, key="policy_automation")
        st.selectbox("Review expiry", ["15 minutes", "1 hour", "4 hours", "No expiry"], index=1)
        st.selectbox("Audit retention", ["7 days", "30 days", "90 days", "1 year"], index=2)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="topline"><div><div class="eyebrow">EVIDENCE // AUDIT STREAM</div><h1>Audit trail</h1><p>A readable record of every decision made by the firewall.</p></div><div class="live">● RECORDING</div></div>', unsafe_allow_html=True)
    if st.session_state.events:
        st.dataframe(st.session_state.events, use_container_width=True, hide_index=True)
        if st.button("Export audit JSON", use_container_width=False):
            st.download_button("Download audit.json", json.dumps(st.session_state.events, indent=2), "audit.json", "application/json")
    else:
        st.info("No events yet. Run a scenario from the Command center to start the audit stream.")