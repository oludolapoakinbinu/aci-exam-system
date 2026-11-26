"""Merge data/raw/*.json into data/question_bank.json and data/flashcards.json."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT_Q = ROOT / "data" / "question_bank.json"
OUT_F = ROOT / "data" / "flashcards.json"


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def q_fingerprint(q: dict) -> str:
    opts = "|".join(norm(o) for o in q["options"])
    return hashlib.md5(f"{norm(q['question'])}::{opts}".encode()).hexdigest()


def main():
    questions = []
    seen = set()
    for path in sorted(RAW.glob("*.questions.json")):
        for q in json.loads(path.read_text()):
            fp = q_fingerprint(q)
            if fp in seen:
                continue
            seen.add(fp)
            questions.append(q)

    cards = []
    seen_c = set()
    for path in sorted(RAW.glob("*.flashcards.json")):
        for c in json.loads(path.read_text()):
            fp = hashlib.md5(norm(c["front"]).encode()).hexdigest()
            if fp in seen_c:
                continue
            seen_c.add(fp)
            cards.append(c)

    OUT_Q.write_text(json.dumps(questions, indent=2, ensure_ascii=False))
    OUT_F.write_text(json.dumps(cards, indent=2, ensure_ascii=False))

    by_topic: dict[str, int] = {}
    for q in questions:
        by_topic[q["topic"]] = by_topic.get(q["topic"], 0) + 1
    print(f"questions={len(questions)} flashcards={len(cards)} by_topic={by_topic}")


if __name__ == "__main__":
    main()
