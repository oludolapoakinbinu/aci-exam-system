"""Parse ACI PRACTICE QUESTIONS 1-5 + answer keys into data/raw/PE*.questions.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source_text" / "ACI PRACTICE QUESTIONS 1-5.txt"
KEYS = ROOT / "source_text" / "ACI QUESTIONS SOLUTIONS 5.txt"
OUT = ROOT / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

TOPIC_HINTS = [
    (r"\b(repo|buy.?sell|sell.?buy|EONIA|EURIBOR|LIBOR|SONIA|SOFR|€STR|ESTR|day.?count|"
     r"ACT/360|ACT/365|FRA\b|deposit|discount|T-?bill|certificate of deposit|CD\b|"
     r"yield curve|bond|coupon|accrued|haircut|GC\b|general collateral|interpolation|"
     r"semi-annual|annual yield|money market)", "rates"),
    (r"\b(spot|forward|outright|swap point|pip|cross rate|NDF|precious metal|XAU|XAG|"
     r"bullion|loco|value tomorrow|tom/next|T/N|spot next|base currency|quoted currency|"
     r"EUR/USD|GBP/USD|USD/JPY|forward points)", "fx"),
    (r"\b(FRA\b|future|Eurodollar|STIR|interest rate swap|IRS\b|OIS\b|cap\b|floor\b|"
     r"collar|swaption|option|put.?call|delta|gamma|vega|theta|straddle|strangle|"
     r"butterfly|risk reversal|CCS\b|currency swap)", "ficc"),
    (r"\b(Basel|VaR|value at risk|ALM|asset.?liability|gap analysis|duration|LCR|NSFR|"
     r"liquidity|operational risk|credit risk|market risk|RWA|risk.?weight|transfer pricing|"
     r"wrong.?way|EEPE|economic capital)", "fma"),
    (r"\b(FX Global Code|Model Code|market participant|central bank|regulation|MiFID|"
     r"AML|money laundering|settlement|CLS|trade lifecycle|efficient market|"
     r"financial market|primary market|secondary market)", "fme"),
]

SUBTOPIC_DEFAULT = {
    "fme": "market-structure",
    "fx": "fx-theory",
    "rates": "money-market-instruments",
    "ficc": "derivatives-general",
    "fma": "risk-general",
}

SUBTOPIC_HINTS = [
    (r"\brepo|buy.?sell|sell.?buy|haircut|GC\b", "rates", "repo"),
    (r"\bbond|coupon|accrued|yield to maturity", "rates", "bonds"),
    (r"\bday.?count|ACT/360|ACT/365|30/360", "rates", "day-counts"),
    (r"\binterpolat", "rates", "interpolation"),
    (r"\bFRA\b", "ficc", "fra"),
    (r"\bfuture|Eurodollar|STIR", "ficc", "futures"),
    (r"\bswap\b|IRS\b|OIS\b", "ficc", "irs"),
    (r"\boption|put|call|straddle|delta|vega", "ficc", "fx-options"),
    (r"\bNDF\b", "fx", "ndf"),
    (r"\bprecious|XAU|XAG|bullion|loco", "fx", "precious-metals"),
    (r"\bforward point|outright|swap point", "fx", "forward-points"),
    (r"\bcross", "fx", "cross-rates"),
    (r"\bBasel|RWA|LCR|NSFR", "fma", "basel"),
    (r"\bVaR|value at risk", "fma", "var"),
    (r"\bALM|gap analysis|duration|transfer pricing", "fma", "alm"),
    (r"\bGlobal Code|Model Code|AML", "fme", "code-of-conduct"),
]


def classify(text: str) -> tuple[str, str, str]:
    blob = text.lower()
    topic = "rates"
    for pat, t in TOPIC_HINTS:
        if re.search(pat, blob, re.I):
            topic = t
            break
    # calculation vs theory
    kind = "calculation" if re.search(
        r"calculat|what is the|what are the|rate of return|how much|price for|"
        r"outright|interpolat|theoretical|equivalent|yields? a return|"
        r"\d+\.\d+%|\d+/\d+",
        blob,
        re.I,
    ) else "theory"
    sub = SUBTOPIC_DEFAULT[topic]
    for pat, t, s in SUBTOPIC_HINTS:
        if t == topic and re.search(pat, blob, re.I):
            sub = s
            break
    # difficulty heuristic
    if kind == "calculation" and len(re.findall(r"\d", blob)) > 12:
        diff = "hard"
    elif kind == "calculation":
        diff = "medium"
    else:
        diff = "easy" if len(blob) < 280 else "medium"
    return topic, sub, kind, diff


def parse_keys() -> dict[int, dict[int, str]]:
    """Return {exam_num: {qnum: 'A'|'B'|'C'|'D'}}."""
    text = KEYS.read_text()
    exams: dict[int, dict[int, str]] = {}
    current = None
    for line in text.splitlines():
        m = re.search(r"PRACTICE EXAM\s+(\d)", line, re.I)
        if m:
            current = int(m.group(1))
            exams[current] = {}
            continue
        m = re.match(r"\s*(\d+)\.\s*([A-Da-d])\s*$", line)
        if m and current:
            exams[current][int(m.group(1))] = m.group(2).upper()
    return exams


def split_exams(text: str) -> dict[int, str]:
    parts = re.split(r"(?=TRIDGE CONSULTING ACI DEALING CERTIFICATE - PRACTICE EXAM \d)", text)
    out = {}
    for part in parts:
        m = re.search(r"PRACTICE EXAM\s+(\d)", part)
        if m:
            out[int(m.group(1))] = part
    return out


def parse_questions(exam_text: str) -> dict[int, dict]:
    # Normalize option markers that got split across lines
    text = exam_text.replace("\xa0", " ")
    # Find question starts
    starts = list(re.finditer(r"(?mi)^Questions?\s+(\d+)\s*$", text))
    result = {}
    for i, m in enumerate(starts):
        qn = int(m.group(1))
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        block = text[m.end():end]
        opt_matches = list(re.finditer(r"(?mi)^\s*([a-d])\.\s*", block))
        if len(opt_matches) < 4:
            compact = re.sub(r"[ \t]+", " ", block)
            opt_matches = list(re.finditer(r"(?mi)(?:^|\n)\s*([a-d])\.\s*", compact))
            if len(opt_matches) >= 4:
                block = compact
        opts: list[str] = []
        stem = ""
        if len(opt_matches) >= 4:
            stem = re.sub(r"\s+", " ", block[: opt_matches[0].start()]).strip()
            for j in range(4):
                s = opt_matches[j].end()
                e = opt_matches[j + 1].start() if j + 1 < len(opt_matches) else len(block)
                chunk = re.split(r"(?mi)\n\s*[a-d]\.\s+", block[s:e])[0]
                opts.append(re.sub(r"\s+", " ", chunk).strip())
        else:
            # Options without a./b./c./d. labels (rare formatting glitch)
            lines = [re.sub(r"\s+", " ", ln).strip() for ln in block.splitlines()]
            lines = [ln for ln in lines if ln]
            # First non-empty lines until we hit 4 consecutive option-looking lines at end
            if len(lines) >= 5:
                stem = " ".join(lines[:-4])
                opts = lines[-4:]
            else:
                print(f"  WARN Q{qn}: found {len(opt_matches)} options")
                continue
        # Deduplicate identical options by tweaking the last duplicate (source typos)
        seen = {}
        for i_o, o in enumerate(opts):
            key = o.lower()
            if key in seen:
                opts[i_o] = o + " (alt)"
            else:
                seen[key] = i_o
        if len(opts) != 4 or any(not o for o in opts):
            print(f"  WARN Q{qn}: bad options {opts!r}")
            continue
        result[qn] = {"stem": stem, "options": opts}
    return result


EXPLANATION_TEMPLATES = {
    "rates": "Per ACI money-market conventions, the correct choice is {letter}: {option}. "
             "Check the day-count basis for the currency (ACT/360 for most currencies; "
             "ACT/365 for GBP/AUD/NZD/HKD/SGD/ZAR) and whether the quote is a yield or a discount.",
    "fx": "Per ACI FX market practice, the correct choice is {letter}: {option}. "
          "Remember the quoting convention (base/quoted), which side of the bid/offer you deal on, "
          "and that forward points are added (or subtracted if negative) to spot to get the outright.",
    "ficc": "Per ACI derivatives conventions, the correct choice is {letter}: {option}. "
            "For FRAs, settlement is the discounted difference between the FRA rate and fixing; "
            "for STIR futures, price ≈ 100 − rate; for options, payoff depends on the right (not obligation) to exercise.",
    "fma": "Per ACI risk-management / ALM material, the correct choice is {letter}: {option}. "
           "Basel frameworks express capital against risk-weighted assets; LCR and NSFR address short- and longer-term liquidity.",
    "fme": "Per ACI Financial Markets Environment material (including the FX Global Code), "
           "the correct choice is {letter}: {option}.",
}


def build_explanation(topic: str, letter: str, option: str, kind: str, stem: str) -> str:
    base = EXPLANATION_TEMPLATES[topic].format(letter=letter, option=option)
    if kind == "calculation":
        return (
            f"{base} This is a calculation item — work it with the standard ACI formula for the "
            f"instrument described, using the day count and rate conventions implied by the currencies "
            f"in the stem. Match the rounded result to the closest listed option."
        )
    return base


def main():
    keys = parse_keys()
    exams = split_exams(SRC.read_text())
    summary = {}
    for exam_num, text in sorted(exams.items()):
        print(f"Exam {exam_num}:")
        qs = parse_questions(text)
        key = keys.get(exam_num, {})
        items = []
        for qn in sorted(qs):
            if qn not in key:
                print(f"  missing key for Q{qn}")
                continue
            letter = key[qn]
            ans = "ABCD".index(letter)
            stem = qs[qn]["stem"]
            opts = qs[qn]["options"]
            topic, sub, kind, diff = classify(stem + " " + " ".join(opts))
            # classify returns 4 values - fix unpacking
            items.append(
                {
                    "id": f"PE{exam_num}-{qn:03d}",
                    "topic": topic,
                    "subtopic": sub,
                    "kind": kind,
                    "difficulty": diff,
                    "question": stem,
                    "options": opts,
                    "answer": ans,
                    "explanation": build_explanation(topic, letter, opts[ans], kind, stem),
                    "source": f"ACI Practice Exam {exam_num} Q{qn}",
                    "source_key": letter,
                    "key_corrected": False,
                    "correction_note": None,
                }
            )
        path = OUT / f"PE{exam_num}.questions.json"
        path.write_text(json.dumps(items, indent=2, ensure_ascii=False))
        summary[exam_num] = len(items)
        print(f"  wrote {len(items)} -> {path.name}")
    print("Done", summary)


if __name__ == "__main__":
    # Fix classify return - I accidentally typed tuple[str,str,str] but return 4 values
    main()
