"""Rewrite every question explanation into a detailed, exam-style solution note."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "data" / "question_bank.json"
RAW = ROOT / "data" / "raw"

LETTERS = "ABCD"

TOPIC_CONTEXT = {
    "fme": (
        "This sits in Financial Markets Environment: market structure, regulation, codes of conduct "
        "(FX Global Code / Model Code), settlement and ethics."
    ),
    "fx": (
        "This is an FX item. Remember BASE/QUOTE quoting, which side of the bid/offer the customer "
        "deals on, and whether forward points are a premium (ascending) or discount (descending)."
    ),
    "rates": (
        "This is a Rates / money-markets item. Check the day-count basis (ACT/360 vs ACT/365) and "
        "whether the quote is a yield, discount rate, or bond/repo figure."
    ),
    "ficc": (
        "This is a FICC derivatives item (FRA, futures, IRS/OIS or options). Identify the instrument "
        "payoff and whether you are hedging a borrower or a lender/investor."
    ),
    "fma": (
        "This is Financial Markets Applications: ALM, market/credit/liquidity/operational risk, VaR "
        "and Basel (RWA, LCR, NSFR)."
    ),
}

SUBTOPIC_DETAIL = {
    "day-counts": (
        "ACT/360 is standard for USD, EUR, CHF and JPY money markets. ACT/365 is used for GBP, AUD, "
        "NZD, HKD, SGD and ZAR (among others). Interest = P × r × d/B."
    ),
    "interpolation": (
        "Straight-line interpolation: r = r1 + (t−t1)/(t2−t1)×(r2−r1). Same idea applies to FX forward "
        "points between two tenors."
    ),
    "forward-points": (
        "Ascending points (bid < offer) are a premium — add to spot. Descending points are a discount "
        "— subtract. Outright = spot + points on the matching bid or offer side."
    ),
    "outright-forwards": (
        "Build the outright from spot and points with the correct sign. Customer buys base on the "
        "offer; sells base on the bid."
    ),
    "cross-rates": (
        "When USD is the common currency in the middle, multiply same-side rates for the cross. "
        "When you must divide, invert carefully and keep bid/offer sides consistent with the dealing side."
    ),
    "fra": (
        "FRA settlement = N×(L−F)×d/B / [1+L×d/B]. The buyer receives when the fixing exceeds the "
        "FRA rate (typical hedge for a future borrower). Notation A×B starts in A months and ends in B."
    ),
    "futures": (
        "STIR futures price ≈ 100 − rate. For Eurodollar futures, 1 bp is typically USD 25 per contract. "
        "Short futures hedges a borrower (profits when rates rise / futures price falls)."
    ),
    "irs": (
        "A payer swap pays fixed / receives floating. A receiver swap does the opposite. Standard "
        "single-currency IRS notionals are not exchanged."
    ),
    "repo": (
        "Classic repo is one repurchase contract; legal title passes to the buyer. Coupons paid during "
        "the term are manufactured back to the seller. Repo interest = Cash × r × d/B."
    ),
    "basel": (
        "Capital ratios use RWA in the denominator. LCR = HQLA / 30-day stressed net outflows. "
        "NSFR = ASF / RSF over one year. Common equity carries a 100% ASF factor."
    ),
    "var": (
        "VaR is a probabilistic loss threshold for a horizon and confidence level — not the maximum "
        "possible loss and not by itself the full capital requirement."
    ),
    "alm": (
        "Duration and repricing-gap tools measure how NII and economic value of equity respond to rate "
        "moves. Positive gap (RSA > RSL) generally benefits when rates rise."
    ),
    "code-of-conduct": (
        "The FX Global Code and related codes set principles of good practice (ethics, governance, "
        "execution, information sharing, risk, confirmation/settlement). They are not statutes by themselves."
    ),
    "ndf": (
        "NDFs cash-settle the difference versus a fixing in a convertible currency (often USD) when "
        "the offshore currency cannot be freely delivered."
    ),
    "precious-metals": (
        "LBMA Good Delivery gold: min fineness 0.995 and 350–430 fine oz. ISO codes: XAU gold, XAG silver."
    ),
    "fx-quotes": (
        "In EUR/USD the euro is base and the dollar is quote. The market maker's bid is where they buy "
        "base; the offer is where they sell base."
    ),
    "benchmarks": (
        "EONIA was a volume-weighted euro overnight average (now superseded by €STR for new business). "
        "RFRs: SOFR (USD), SONIA (GBP), €STR (EUR), SARON (CHF), TONA (JPY)."
    ),
}


def letters_for(ans: int) -> str:
    return LETTERS[ans]


def try_calc_working(q: dict) -> str | None:
    """Best-effort numeric working for common ACI patterns."""
    text = q["question"] + " " + " ".join(q["options"])
    nums = [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*\.?\d*", text)]

    # Linear interpolation between two rates and a middle tenor
    m = re.search(
        r"(\d+)\s*-?\s*day[^\d]{0,40}(\d+\.?\d*)\s*%[\s\S]{0,80}?"
        r"(\d+)\s*-?\s*day[^\d]{0,40}(\d+\.?\d*)\s*%[\s\S]{0,120}?"
        r"(\d+)\s*-?\s*day",
        text,
        re.I,
    )
    if m and re.search(r"interpolat", text, re.I):
        t1, r1, t2, r2, t = map(float, m.groups())
        rt = r1 + (t - t1) / (t2 - t1) * (r2 - r1)
        return (
            f"Formula (straight-line interpolation):\n"
            f"  r = r1 + (t − t1)/(t2 − t1) × (r2 − r1)\n"
            f"Working:\n"
            f"  r = {r1}% + ({t:g} − {t1:g})/({t2:g} − {t1:g}) × ({r2}% − {r1}%)\n"
            f"    = {r1}% + {(t-t1)/(t2-t1):.6f} × {r2-r1}%\n"
            f"    = {rt:.3f}%"
        )

    # Simple interest / rate of return: interest, principal, days
    m = re.search(
        r"(?:investment|deposit|principal)?[^\d]{0,40}([\d,]+(?:\.\d+)?)\s*(?:million)?"
        r"[\s\S]{0,120}?(?:yields? a return of|interest of|returns?)\s*"
        r"(?:CHF|USD|EUR|GBP)?\s*([\d,]+(?:\.\d+)?)"
        r"[\s\S]{0,80}?(\d+)\s*-?\s*day",
        text,
        re.I,
    )
    if m and re.search(r"rate of return|what is the rate", text, re.I):
        p = float(m.group(1).replace(",", ""))
        if "million" in text.lower() and p < 1000:
            p *= 1_000_000
        interest = float(m.group(2).replace(",", ""))
        days = float(m.group(3))
        basis = 365 if re.search(r"\b(GBP|AUD|NZD|HKD|SGD|ZAR)\b", text) else 360
        # CHF etc use 360
        if re.search(r"\bCHF\b", text):
            basis = 360
        r = (interest / p) * (basis / days) * 100
        return (
            f"Formula:\n"
            f"  r = (Interest / Principal) × (Basis / Days)\n"
            f"Working:\n"
            f"  r = ({interest:,.0f} / {p:,.0f}) × ({basis:g} / {days:g})\n"
            f"    = {interest/p:.6f} × {basis/days:.6f}\n"
            f"    = {r:.3f}%   (basis {basis:g})"
        )

    # Semi-annual equivalent of annual yield
    m = re.search(r"(\d+(?:\.\d+)?)\s*%\s*annual", text, re.I)
    if m and re.search(r"semi-?annual", text, re.I):
        ann = float(m.group(1)) / 100
        y = 2 * (math.sqrt(1 + ann) - 1) * 100
        return (
            f"Formula:\n"
            f"  (1 + y/2)² = 1 + r_annual\n"
            f"  y = 2(√(1+r) − 1)\n"
            f"Working:\n"
            f"  y = 2(√{1+ann:.4f} − 1) = {y:.3f}%"
        )

    # FRA settlement rough detect
    if re.search(r"\bFRA\b", text) and re.search(r"settlement|EURIBOR|LIBOR|fix", text, re.I):
        return (
            "Formula (discounted FRA settlement):\n"
            "  Settlement = N × (L − F) × (d / B) / [1 + L × (d / B)]\n"
            "where N = notional, L = fixing, F = FRA rate, d = period days, B = day basis.\n"
            "Sign: the FRA buyer receives when L > F (and pays when L < F)."
        )

    # Eurodollar futures PnL
    if re.search(r"Eurodollar futures|ED futures|sell \d+ Eurodollar|buy \d+ Eurodollar", text, re.I):
        return (
            "Formula:\n"
            "  Futures price ≈ 100 − rate\n"
            "  P&L ≈ (# contracts) × (# basis points moved) × USD 25\n"
            "A short futures position profits when the futures price falls (implied rates rise)."
        )

    # Forward points / outright
    if re.search(r"outright|forward points", text, re.I):
        return (
            "Method:\n"
            "  1) Read whether points are ascending (premium / add) or descending (discount / subtract).\n"
            "  2) Choose the correct side: customer buys base → use offer; sells base → use bid.\n"
            "  3) Outright = Spot ± Points (scaled to the pair’s pip size).\n"
            "  4) Match the rounded result to the closest option."
        )

    # Forward-forward interest
    if re.search(r"forward-?forward|3v6|2v5|1x4|3x6", text, re.I) and re.search(
        r"interest|deposit|rate", text, re.I
    ):
        return (
            "Formula (ACT/360 example):\n"
            "  FF = {[1 + r_L×D_L/360] / [1 + r_S×D_S/360] − 1} × 360/(D_L − D_S)\n"
            "This is the break-even rate from the short date to the long date."
        )

    if q.get("kind") == "calculation":
        return (
            "Approach:\n"
            "  Identify the instrument and the standard ACI formula for it.\n"
            "  Insert the given notionals, rates and day counts using the correct basis.\n"
            "  Round only at the end and pick the closest listed option — common traps are wrong "
            "day basis, swapped bid/offer, or the wrong sign on forward points."
        )
    return None


def why_others_wrong(q: dict) -> str:
    ans = q["answer"]
    lines = []
    for i, opt in enumerate(q["options"]):
        if i == ans:
            continue
        letter = LETTERS[i]
        # Heuristic distractor comments
        low = opt.lower()
        hint = "does not match the correct convention or arithmetic for this stem."
        if re.search(r"all of the above", low):
            hint = "over-states the case — at least one listed element is not required/correct."
        elif re.search(r"none of the above", low):
            hint = "is too absolute; a valid choice exists among the other options."
        elif q["kind"] == "calculation":
            hint = (
                "is a common trap (wrong day basis, wrong bid/offer side, wrong sign on points, "
                "or an intermediate figure before discounting/rounding)."
            )
        lines.append(f"  {letter} — “{opt}” {hint}")
    return "Why the other options are weaker:\n" + "\n".join(lines)


def build_explanation(q: dict) -> str:
    ans = q["answer"]
    letter = letters_for(ans)
    correct = q["options"][ans]
    topic = q.get("topic", "rates")
    sub = q.get("subtopic", "")
    kind = q.get("kind", "theory")

    parts: list[str] = []
    parts.append(f"Correct answer: {letter} — {correct}")
    parts.append("")
    parts.append("Why this is correct:")
    # Prefer existing non-generic explanation content as a seed sentence
    old = (q.get("explanation") or "").strip()
    generic_markers = (
        "Per ACI money-market conventions",
        "Per ACI FX market practice",
        "Per ACI derivatives conventions",
        "Per ACI risk-management",
        "Per ACI Financial Markets Environment",
        "This is a calculation item — work it with the standard ACI formula",
    )
    if old and not any(old.startswith(m) for m in generic_markers) and len(old) > 80:
        # Keep the verified/authored body, then wrap with structure
        parts.append(old)
    else:
        parts.append(
            f"{TOPIC_CONTEXT.get(topic, '')} "
            f"Option {letter} is the statement/result that matches the syllabus rule or the "
            f"computed value for the data in the question."
        )
        if sub in SUBTOPIC_DETAIL:
            parts.append(SUBTOPIC_DETAIL[sub])
        # Echo the stem focus
        stem = re.sub(r"\s+", " ", q["question"]).strip()
        if len(stem) > 220:
            stem = stem[:217] + "…"
        parts.append(f"Applied to this question (“{stem}”), {letter} is the choice that fits.")

    working = try_calc_working(q)
    if working:
        parts.append("")
        parts.append("Worked method:")
        parts.append(working)

    if kind == "theory" and sub in SUBTOPIC_DETAIL and not working:
        parts.append("")
        parts.append("Syllabus note:")
        parts.append(SUBTOPIC_DETAIL[sub])

    parts.append("")
    parts.append(why_others_wrong(q))

    parts.append("")
    tip = {
        "fx": "Exam tip: write down bid/offer and point sign before you calculate — most FX traps are side/sign errors.",
        "rates": "Exam tip: circle the day basis (360 vs 365) before punching the calculator.",
        "ficc": "Exam tip: state who is hedging (borrower vs lender) — that tells you buy vs sell FRA/futures.",
        "fma": "Exam tip: name the risk type or Basel ratio in one line before eliminating options.",
        "fme": "Exam tip: codes of conduct are principles of good practice, not automatic statute.",
    }.get(topic, "Exam tip: eliminate options that break a basic market convention first.")
    parts.append(tip)

    if q.get("key_corrected") and q.get("correction_note"):
        parts.append("")
        parts.append(f"Source-key correction: {q['correction_note']}")

    return "\n".join(parts).strip()


def enrich_file(path: Path) -> int:
    items = json.loads(path.read_text())
    if not items or "front" in items[0]:
        return 0
    for q in items:
        q["explanation"] = build_explanation(q)
    path.write_text(json.dumps(items, indent=2, ensure_ascii=False))
    return len(items)


def main():
    total = 0
    for path in sorted(RAW.glob("*.questions.json")):
        n = enrich_file(path)
        print(f"{path.name}: {n}")
        total += n
    # rebuild merged bank from enriched raw files
    import importlib.util

    spec = importlib.util.spec_from_file_location("merge_bank", ROOT / "scripts" / "merge_bank.py")
    merge_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(merge_mod)
    merge_mod.main()

    bank = json.loads(BANK.read_text())
    avg = sum(len(q["explanation"]) for q in bank) // max(1, len(bank))
    print(f"bank={len(bank)} avg_explanation_chars={avg}")


if __name__ == "__main__":
    main()
