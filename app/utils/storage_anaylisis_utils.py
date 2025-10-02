import json
from pathlib import Path


ANALYSIS_FILE = Path("app/test/death_analysis.json")

def load_analysis():
    if ANALYSIS_FILE.exists():
        with open(ANALYSIS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_analysis(data):
    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)