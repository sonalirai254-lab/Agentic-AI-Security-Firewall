# Agentic AI Security Firewall

A simple hackathon MVP that intercepts simulated AI agent tool-call JSON payloads and classifies them as:

- GREEN: Safe action → Approved
- AMBER: Sensitive action → Logged/Monitored
- RED: Destructive action → Blocked and sent for human approval

## Run in VS Code

### 1. Extract the ZIP
Open the extracted folder in VS Code.

### 2. Open Terminal
Use **Terminal → New Terminal**.

### 3. Create virtual environment
```bash
python -m venv venv
```

### 4. Activate it (Windows)
```bash
venv\Scripts\activate
```

### 5. Install requirements
```bash
pip install -r requirements.txt
```

### 6. Run the live project
```bash
streamlit run app.py
```

Then open:
http://localhost:8501

## Demo
Try these actions:
- read_file → GREEN
- send_email → AMBER
- delete_database → RED
