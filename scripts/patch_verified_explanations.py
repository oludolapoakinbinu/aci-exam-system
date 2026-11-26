"""Overwrite explanations for calculation items we have explicitly verified."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

PATCHES = {
    "PE1-001": (
        "In London money-market convention, GBP, AUD, CAD (sometimes), NZD, HKD, SGD and ZAR "
        "use a 365-day year; USD/EUR/CHF/JPY use 360. Of the listed currencies, HKD is the "
        "365-day answer expected by this paper (AUD is also 365 — if both appear, prefer the key's "
        "choice after checking the latest syllabus wording)."
    ),
    "PE1-003": (
        "Straight-line interpolation: 3.10% + (120−90)/(180−90)×(3.50−3.10)% "
        "= 3.10% + (1/3)×0.40% = 3.233%."
    ),
    "PE1-004": (
        "Convert annual effective 5% to semi-annual bond basis: (1+y/2)² = 1.05 ⇒ "
        "y = 2(√1.05 − 1) ≈ 4.939%."
    ),
    "PE1-005": (
        "Rate = (interest/principal)×(basis/days) = (100,000/15,500,000)×(360/182) ≈ 1.276% → 1.28%. "
        "CHF uses ACT/360."
    ),
    "PE1-008": (
        "EONIA was the euro overnight index average: a volume-weighted average of overnight "
        "unsecured euro transactions. (It has since been superseded by €STR for new business.)"
    ),
    "PE1-009": (
        "In a classic repo legal title passes to the buyer, so the issuer pays the coupon to the buyer; "
        "the buyer must immediately make an equivalent 'manufactured' payment to the seller."
    ),
    "PE5-036": (
        "Points 205/195 are descending ⇒ discount −205/−195. Client sells USD / buys GBP ⇒ deals on "
        "the GBP/USD offer. Outright offer = 1.4540 − 0.0195 = 1.4345."
    ),
    "PE5-039": (
        "FRA buyer settlement = N×(L−F)×d/360 / [1+L×d/360]. "
        "500m×0.0025×334/360 = 1,159,722.22; ÷ (1+0.0075×334/360) ≈ 1,151,708 received."
    ),
    "PE5-041": (
        "Eurodollar future: 1 bp = USD 25/contract. Short 20 lots, price falls 10 bp (95.30→95.20) "
        "⇒ rates up ⇒ short profits 20×10×25 = USD 5,000."
    ),
}

# Also set answers we verified if needed
ANSWER_FIXES = {
    # id: (answer_index, source_key, key_corrected, note)
}


def main():
    for path in RAW.glob("PE*.questions.json"):
        items = json.loads(path.read_text())
        changed = 0
        for q in items:
            if q["id"] in PATCHES:
                q["explanation"] = PATCHES[q["id"]]
                changed += 1
            if q["id"] in ANSWER_FIXES:
                ans, key, corr, note = ANSWER_FIXES[q["id"]]
                q["answer"] = ans
                q["source_key"] = key
                q["key_corrected"] = corr
                q["correction_note"] = note
                changed += 1
        if changed:
            path.write_text(json.dumps(items, indent=2, ensure_ascii=False))
            print(path.name, changed)


if __name__ == "__main__":
    main()
