import os
import json
from datetime import datetime

LOG_FILE = "logs/inputs.json"

def log_input(text, engine, voice):
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "text": text,
        "engine": engine,
        "voice": voice
    }
    
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
            
    logs.append(log_entry)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)
