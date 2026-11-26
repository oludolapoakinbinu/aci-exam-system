from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "aci.db"
RAW_DIR = DATA_DIR / "raw"
BANK_PATH = DATA_DIR / "question_bank.json"
FLASH_PATH = DATA_DIR / "flashcards.json"
SOURCE_TEXT = ROOT / "source_text"

TOPICS = {
    "fme": {
        "code": "fme",
        "name": "Financial Markets Environment",
        "exam_count": 10,
        "min_pass": 5,
        "color": "#0ea5e9",
    },
    "fx": {
        "code": "fx",
        "name": "Foreign Exchange",
        "exam_count": 18,
        "min_pass": 9,
        "color": "#8b5cf6",
    },
    "rates": {
        "code": "rates",
        "name": "Rates",
        "exam_count": 18,
        "min_pass": 9,
        "color": "#10b981",
    },
    "ficc": {
        "code": "ficc",
        "name": "FICC Derivatives",
        "exam_count": 14,
        "min_pass": 7,
        "color": "#f59e0b",
    },
    "fma": {
        "code": "fma",
        "name": "Financial Markets Applications",
        "exam_count": 10,
        "min_pass": 5,
        "color": "#ef4444",
    },
}

EXAM_TOTAL = 70
EXAM_PASS = 42  # 60%
EXAM_MINUTES = 120
GRADES = [
    (80, "Distinction"),
    (70, "Merit"),
    (60, "Pass"),
    (0, "Fail"),
]
