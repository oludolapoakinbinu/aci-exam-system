"""Validate raw question/flashcard batch files against scripts/authoring_spec.txt."""
import json
import sys

SUBTOPICS = {
    "fme": {"market-functions", "market-structure", "participants", "efficient-markets", "regulation",
            "trade-lifecycle", "settlement", "code-of-conduct", "economic-indicators", "central-banks",
            "aml-ethics"},
    "fx": {"fx-quotes", "cross-rates", "value-dates", "forward-points", "outright-forwards", "fx-swaps",
           "forward-forwards", "ndf", "precious-metals", "fx-theory", "fx-risk"},
    "rates": {"day-counts", "simple-compound", "yield-conversion", "money-market-instruments",
              "discount-instruments", "benchmarks", "interpolation", "forward-rates", "yield-curve", "bonds",
              "repo", "central-bank-ops"},
    "ficc": {"fra", "futures", "irs", "ois", "ccs", "fx-options", "ir-options", "option-pricing",
             "option-strategies", "derivatives-general"},
    "fma": {"alm", "gap-analysis", "duration", "transfer-pricing", "market-risk", "var", "credit-risk",
            "liquidity-risk", "operational-risk", "basel", "risk-general"},
}


def check_question(q, errors):
    qid = q.get("id", "?")
    for k in ("id", "topic", "subtopic", "kind", "difficulty", "question", "options", "answer", "explanation",
              "source"):
        if k not in q:
            errors.append(f"{qid}: missing {k}")
    if q.get("topic") not in SUBTOPICS:
        errors.append(f"{qid}: bad topic {q.get('topic')}")
    elif q.get("subtopic") not in SUBTOPICS[q["topic"]]:
        errors.append(f"{qid}: bad subtopic {q.get('subtopic')} for {q['topic']}")
    if q.get("kind") not in ("theory", "calculation"):
        errors.append(f"{qid}: bad kind")
    if q.get("difficulty") not in ("easy", "medium", "hard"):
        errors.append(f"{qid}: bad difficulty")
    opts = q.get("options", [])
    if not isinstance(opts, list) or len(opts) != 4:
        errors.append(f"{qid}: needs exactly 4 options")
    elif len({str(o).strip().lower() for o in opts}) != 4:
        errors.append(f"{qid}: duplicate options")
    elif any(not str(o).strip() for o in opts):
        errors.append(f"{qid}: empty option")
    if q.get("answer") not in (0, 1, 2, 3):
        errors.append(f"{qid}: answer must be 0-3")
    if len(str(q.get("explanation", ""))) < 30:
        errors.append(f"{qid}: explanation too short")
    if q.get("key_corrected") and not q.get("correction_note"):
        errors.append(f"{qid}: key_corrected without correction_note")


def check_card(c, errors):
    cid = c.get("id", "?")
    for k in ("id", "topic", "subtopic", "front", "back"):
        if not c.get(k):
            errors.append(f"{cid}: missing {k}")
    if c.get("topic") not in SUBTOPICS:
        errors.append(f"{cid}: bad topic")
    elif c.get("subtopic") not in SUBTOPICS[c["topic"]]:
        errors.append(f"{cid}: bad subtopic {c.get('subtopic')}")


def main(paths):
    total_err = 0
    for p in paths:
        data = json.load(open(p))
        errors = []
        ids = [d.get("id") for d in data]
        if len(ids) != len(set(ids)):
            errors.append("duplicate ids")
        for d in data:
            (check_card if "front" in d else check_question)(d, errors)
        print(f"{p}: {len(data)} items, {len(errors)} errors")
        for e in errors:
            print("  ", e)
        total_err += len(errors)
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
