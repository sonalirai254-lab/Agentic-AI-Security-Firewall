# Aegis // Agent Firewall
> A real-time security policy cockpit and governance proxy for autonomous AI agent tool calls.

---

## Overview

Aegis intercepts simulated or live AI agent tool-call JSON payloads before execution, evaluates cryptographic and behavioral policy risk, and provides human-in-the-loop approval gates for sensitive or irreversible operations.

### Key Capabilities
- **Command Center**:
  - **Tool-Call Interception**: Real-time evaluation of RFC-8259 JSON payloads with rule matching and risk scoring.
  - **KPI Telemetry**: Real-time metrics tracking Approved, Review Queue, Blocked, and Total Session Events.
  - **Interactive Simulator**: Pre-configured quick scenarios (Research Search, Send Customer Email, Delete Production DB, Query Analytics, Rotate API Credentials).
  - **Human Approval Gate**: Dynamic review card for sensitive medium-risk actions with instant Approve/Block resolution.
  - **Policy Decision Pipeline**: Visual zero-trust execution flow (`Agent ➔ Interceptor ➔ Policy Engine ➔ Risk Scoring ➔ Decision Gate`).
  - **Risk Distribution & Live Events**: Segmented session risk distribution meter and real-time streaming forensic feed.
- **Policy Studio**:
  - **Security Rule Matrix**: Configurable risk rules for High (Immediate Block), Medium (Human Gate), and Low (Allow + Audit Log).
  - **Architectural Invariants**: Explicit enforcement of Least Privilege, Fail-Closed Architecture, and Verifiable Human Gates.
  - **Automation Controls**: Configurable review expiration timeouts and immutable audit log retention.
- **Audit Trail**:
  - **Forensic Event Log**: Searchable and filterable table (by Risk, Decision, or keyword search across Agent/Tool/Resource).
  - **JSON Export**: One-click download of the complete session audit log (`aegis_audit_<timestamp>.json`).

---

## Local Development

### 1. Clone the repository & navigate to project directory
```bash
git clone <your-repo-url>
cd Agentic_AI_Security_Firewall
```

### 2. Create and activate a virtual environment (optional but recommended)
- **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run app.py
```
The application will open at `http://localhost:8501`.

---

## Streamlit Community Cloud Deployment

This repository is pre-configured and optimized for direct 1-click deployment on [Streamlit Community Cloud](https://share.streamlit.io/).

### Deployment Settings
- **Repository**: Your GitHub repository
- **Branch**: `main`
- **Main file path**: `app.py`
- **Python Version**: `3.10` / `3.11` / `3.12` (recommended)

### Dependencies
All required dependencies are defined in `requirements.txt`:
```
streamlit>=1.30.0
```
- **Zero system packages required**: No external C-libraries, binaries, or Nmap installations are required.
- **Zero standard library packages in requirements**: Uses only built-in `json` and `datetime`.

### Secrets & Environment Variables
- **Required Secrets**: **None**. The application runs completely standalone with its embedded policy rule engine.
- **Optional Secrets**: If integrating with custom webhook endpoints or logging services in the future, configure them under **App Settings ➔ Secrets** in Streamlit Cloud using standard TOML format (`st.secrets`).

---

## License
MIT License.
