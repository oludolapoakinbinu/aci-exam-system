"""Hand-authored original MCQs + flashcards grounded in the ACI materials."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw"


def Q(i, topic, sub, kind, diff, stem, opts, ans, expl, src_note=""):
    return {
        "id": f"ORIG-{i:03d}",
        "topic": topic,
        "subtopic": sub,
        "kind": kind,
        "difficulty": diff,
        "question": stem,
        "options": opts,
        "answer": ans,
        "explanation": expl,
        "source": f"Original - based on {src_note or topic.upper() + ' syllabus'}",
        "source_key": None,
        "key_corrected": False,
        "correction_note": None,
        "is_original": True,
    }


def FC(i, topic, sub, front, back, src=""):
    return {
        "id": f"FC-{i:03d}",
        "topic": topic,
        "subtopic": sub,
        "front": front,
        "back": back,
        "source": src or "ACI study materials",
    }


questions = []
n = 0


def add(*args, **kwargs):
    global n
    n += 1
    questions.append(Q(n, *args, **kwargs))


# ========== FME ==========
add("fme", "market-functions", "theory", "easy",
    "Which of the following is a primary function of financial markets?",
    ["Setting statutory tax rates for corporates",
     "Price discovery and determination of fair value",
     "Guaranteeing positive real returns to all investors",
     "Eliminating credit risk between counterparties"],
    1,
    "Financial markets facilitate price discovery on a willing-buyer/willing-seller basis so that assets "
    "trade near fair value. They also mobilise capital, provide liquidity, and allow risk transfer — "
    "they do not set taxes, guarantee returns, or eliminate credit risk.",
    "ICAP Module 1 / 2025 Study Guide §1")

add("fme", "market-structure", "theory", "easy",
    "A market in which newly issued securities are sold to investors for the first time is called the:",
    ["Secondary market", "Money market", "Primary market", "Derivatives market"],
    2,
    "The primary market is where issuers raise capital by selling new securities. The secondary market "
    "is where existing securities trade between investors.",
    "Tutorial Letter 01")

add("fme", "code-of-conduct", "theory", "medium",
    "Under the FX Global Code, which statement is correct?",
    ["The Code is a legally binding statute in every jurisdiction",
     "It sets out principles of good practice for wholesale FX market participants",
     "It applies only to bank FX dealers and not to non-bank liquidity providers",
     "It replaces MiFID II reporting obligations"],
    1,
    "The FX Global Code is a set of global principles of good practice for the wholesale FX market. "
    "It is not itself a statute, covers a broad set of Market Participants (including non-bank LPs and "
    "platforms), and does not replace local regulation such as MiFID II.",
    "Tutorial Letter 01 / FX Global Code")

add("fme", "code-of-conduct", "theory", "medium",
    "Which of the following is generally NOT treated as a Market Participant under the FX Global Code?",
    ["A non-bank liquidity provider active in FX",
     "An FX benchmark execution provider",
     "A money changer interacting only with retail customers",
     "An operator of an FX e-trading platform"],
    2,
    "Retail money-changing activity with the general public is typically outside the Code's Market "
    "Participant perimeter. Wholesale FX intermediaries, platforms and benchmark providers are in scope.",
    "Workshop Exercise Book Topic 1")

add("fme", "aml-ethics", "theory", "medium",
    "The classic stages of money laundering are:",
    ["Integration, placement, layering, and dissolution",
     "Placement, layering, and integration",
     "Origination, concealment, and repatriation only",
     "Structuring, hedging, and settlement"],
    1,
    "Standard AML teaching uses three stages: placement (introducing illicit funds), layering "
    "(obscuring the trail), and integration (returning funds as apparently legitimate).",
    "Tutorial Letter 01")

add("fme", "settlement", "theory", "medium",
    "CLS primarily mitigates which FX risk?",
    ["Market risk from spot rate moves",
     "Herstatt / settlement risk via PvP",
     "Operational risk from misbooked trades",
     "Interest-rate risk on the forward points"],
    1,
    "Continuous Linked Settlement (CLS) uses payment-versus-payment (PvP) so that each currency leg "
    "settles if and only if the other does, sharply reducing Herstatt (settlement) risk.",
    "2025 Study Guide §1")

add("fme", "regulation", "theory", "medium",
    "EMIR requires that both OTC and exchange-traded derivatives:",
    ["Be reported to a trade repository the following day",
     "Be cleared only through US CCPs",
     "Be exempt from collateralisation if under €1m",
     "Use LIBOR as the sole floating index"],
    0,
    "Under EMIR, both OTC and exchange-traded derivatives must be reported to trade repositories on "
    "a T+1 basis (among other clearing/collateral rules).",
    "Workshop Topic 1")

add("fme", "central-banks", "theory", "easy",
    "Open-market operations by a central bank are primarily used to:",
    ["Set corporate income-tax rates",
     "Influence short-term interest rates and liquidity in the banking system",
     "Guarantee equity market levels",
     "Replace commercial bank credit officers"],
    1,
    "OMOs (repos, reverse repos, outright purchases/sales) adjust banking-system liquidity and steer "
    "short-term rates toward the policy target.",
    "ICAP Module 1")

add("fme", "economic-indicators", "theory", "easy",
    "Which of the following is typically a coincident indicator of economic activity?",
    ["Building permits", "GDP", "Yield-curve slope", "New unemployment insurance claims"],
    1,
    "GDP moves with the economy and is a classic coincident indicator. Building permits and initial "
    "jobless claims are leading; long-short yield curve shape is often treated as leading.",
    "Tutorial Letter 01")

add("fme", "efficient-markets", "theory", "medium",
    "In a semi-strong form efficient market, prices reflect:",
    ["Only past trading volumes",
     "All publicly available information",
     "All public and all private information",
     "Only central-bank speeches"],
    1,
    "Weak form: past prices; semi-strong: all public info; strong form: public + private. Semi-strong "
    "efficiency means fundamental public data is already in the price.",
    "2025 Study Guide §1")

# ========== FX ==========
add("fx", "fx-quotes", "theory", "easy",
    "In the pair EUR/USD 1.0850, which is the base currency?",
    ["USD", "EUR", "Neither — both are quoted currencies", "The currency with the higher interest rate"],
    1,
    "FX pairs are quoted as BASE/QUOTE. EUR/USD means how many USD (quote) per 1 EUR (base).",
    "Tutorial Letter 02")

add("fx", "fx-quotes", "theory", "medium",
    "A market maker quotes EUR/USD 1.0845–50. A customer wants to buy EUR. At which rate does the customer deal?",
    ["1.0845", "1.0850", "The mid 1.08475", "Whatever rate the customer nominates"],
    1,
    "The customer buying the base (EUR) deals on the market maker's offer (ask) = 1.0850. "
    "The bid is where the MM buys base / customer sells base.",
    "Slides / Tutorial Letter 02")

add("fx", "cross-rates", "calculation", "medium",
    "Spot EUR/USD = 1.1000–10 and USD/JPY = 150.00–10. What is the EUR/JPY bid (market maker's bid)?",
    ["165.000", "165.011", "165.121", "165.110"],
    0,
    "To make a EUR/JPY bid the MM buys EUR / sells JPY: buy EUR vs USD at the EUR/USD bid (1.1000) "
    "and sell JPY vs USD by buying USD/JPY at the offer is wrong — for the cross bid you use "
    "EUR/USD bid × USD/JPY bid = 1.1000 × 150.00 = 165.00 when both quotes are same-side for "
    "multiplying crosses with USD as the common currency in the middle. "
    "(EUR/JPY bid = EUR/USD bid × USD/JPY bid = 165.00.)",
    "Tutorial Letter 02 cross-rate rules")

add("fx", "forward-points", "theory", "medium",
    "Forward points quoted as 12.5 / 11.8 (descending) imply that the forward is at a:",
    ["Premium to spot", "Discount to spot", "Parity with spot", "Volatility smile"],
    1,
    "Ascending points (low/high) = premium; descending (high/low) = discount. The points are applied "
    "with a minus sign when quoted descending.",
    "Tutorial Letter 02")

add("fx", "outright-forwards", "calculation", "medium",
    "Spot GBP/USD = 1.2500–05. Forward points = 25.0 / 22.0 (pips, descending). What is the  "
    "outright offer?",
    ["1.25270", "1.24825", "1.24780", "1.25250"],
    2,
    "Descending points ⇒ discount: −25.0 / −22.0 pips. Outright offer = spot offer + offer points "
    "= 1.2505 + (−22.0)/10,000 = 1.2505 − 0.00220 = 1.24830… closest listed consistent working "
    "with pip scale: 1.2505 − 0.00220 = 1.24830. Rechecking options: 1.24780 = 1.2500 − 0.00220 "
    "(bid+offer mix). Correct offer path: 1.2505 − 0.00220 = 1.24830. Among options, 1.24780 is "
    "nearest common trap; wait — recalculate: 22.0 pips on GBP/USD = 0.00220. 1.2505-0.0022=1.2483. "
    "None exact — use 1.24780 as closest listed if pip convention differs. FIX: choose option that "
    "matches 1.2505-0.0022. Adjusting options in final set.",
    "Tutorial Letter 02")

# Fix the previous question properly
questions[-1] = Q(n, "fx", "outright-forwards", "calculation", "medium",
    "Spot GBP/USD = 1.2500–05. Forward points = 25.0 / 22.0 (descending, pipettes of 0.0001). "
    "What is the outright offer?",
    ["1.25250", "1.25270", "1.24830", "1.24750"],
    2,
    "Descending points mean a discount: −25.0 / −22.0 pips. The outright offer uses the spot offer "
    "and the offer-side points: 1.2505 + (−22.0 × 0.0001) = 1.2505 − 0.0022 = 1.2483.",
    "Tutorial Letter 02")

add("fx", "fx-swaps", "theory", "medium",
    "In a near-leg sell / far-leg buy FX swap on EUR/USD, the dealer has effectively:",
    ["Gone long EUR for the swap period",
     "Gone short EUR for the swap period (lent EUR / borrowed USD)",
     "Bought a EUR call option",
     "Eliminated all FX risk permanently"],
    1,
    "Sell/buy EUR (spot/near vs forward/far) is economically lending the base currency and borrowing "
    "the quoted currency for the tenor — short base until the far leg reverses it.",
    "2025 Study Guide §2")

add("fx", "value-dates", "theory", "easy",
    "Standard spot FX for EUR/USD normally settles on:",
    ["Trade date (T+0)", "T+1", "T+2", "T+5"],
    2,
    "Most major pairs (including EUR/USD) settle spot on T+2. USD/CAD is a notable T+1 exception.",
    "Tutorial Letter 02")

add("fx", "ndf", "theory", "medium",
    "An NDF settles by:",
    ["Physical delivery of both currencies",
     "Cash settlement of the difference versus a fixing rate in a convertible currency (often USD)",
     "Exchange of gold bars",
     "Novation into an IRS"],
    1,
    "Non-deliverable forwards are used where the offshore currency cannot be freely delivered; only "
    "the P&L versus a fixing is paid in a convertible currency such as USD.",
    "2025 Study Guide §2")

add("fx", "precious-metals", "theory", "medium",
    "An LBMA Good Delivery gold bar must have a minimum fineness of:",
    ["0.900", "0.995", "0.999", "1.000"],
    1,
    "London Good Delivery gold: minimum fineness 995 parts per 1,000 (0.995) and gold content "
    "between 350 and 430 fine troy ounces (typically ~400).",
    "ICAP Module 2 / Workshop FX")

add("fx", "precious-metals", "theory", "easy",
    "The ISO currency code for gold is:",
    ["GLD", "XAU", "AU$", "GOL"],
    1,
    "Precious metals use ISO codes XAU (gold), XAG (silver), XPT (platinum), XPD (palladium).",
    "Tutorial Letter 02")

add("fx", "forward-forwards", "theory", "hard",
    "A forward/forward FX swap's 'spot basis' for pricing is generally:",
    ["Always today's spot mid only",
     "The prevailing forward mid to the first leg date",
     "The far-leg outright bid only",
     "The previous day's ECB fixing"],
    1,
    "A forward/forward (e.g. 3v6) is priced off the forward to the near leg as its 'spot basis', "
    "not today's cash spot.",
    "Workshop FX Calculations")

# ========== RATES ==========
add("rates", "day-counts", "theory", "easy",
    "In the London market, which currency conventionally uses a 365-day year for money-market interest?",
    ["USD", "EUR", "CHF", "GBP"],
    3,
    "GBP (and AUD, NZD, HKD, SGD, ZAR, PLN, among others) use ACT/365. USD, EUR, CHF, JPY use ACT/360.",
    "Practice exams / Tutorial Letter 03")

add("rates", "day-counts", "calculation", "medium",
    "Interest on a USD 10,000,000 deposit for 90 days at 3.60% (ACT/360) is:",
    ["USD 90,000", "USD 88,767", "USD 91,250", "USD 36,000"],
    0,
    "Interest = Principal × rate × days/basis = 10,000,000 × 0.036 × 90/360 = 90,000.",
    "Tutorial Letter 03")

add("rates", "simple-compound", "calculation", "medium",
    "A 182-day investment of CHF 15,500,000 returns CHF 100,000. The ACT/360 rate of return is closest to:",
    ["1.32%", "1.29%", "1.28%", "0.65%"],
    2,
    "Rate = (interest/principal) × (basis/days) = (100,000/15,500,000) × (360/182) "
    "= 0.0064516 × 1.9780 ≈ 0.01276 = 1.276% ≈ 1.28%.",
    "ACI Practice Exam 1 Q5 (verified)")

add("rates", "interpolation", "calculation", "medium",
    "If the 90-day USD rate is 3.10% and the 180-day rate is 3.50%, the straight-line 120-day rate is:",
    ["3.233%", "3.300%", "3.333%", "3.367%"],
    0,
    "Linear interpolation: 3.10% + (120−90)/(180−90) × (3.50−3.10)% = 3.10% + 30/90 × 0.40% "
    "= 3.10% + 0.1333% = 3.233%.",
    "ACI Practice Exam 1 Q3 (verified)")

add("rates", "yield-conversion", "calculation", "hard",
    "An investment quotes a 5% annual effective yield. The equivalent semi-annual bond basis yield is closest to:",
    ["4.939%", "5.000%", "5.062%", "4.880%"],
    0,
    "Semi-annual equivalent y satisfies (1 + y/2)² = 1.05 ⇒ 1 + y/2 = √1.05 ≈ 1.024695 "
    "⇒ y/2 ≈ 0.024695 ⇒ y ≈ 4.939%.",
    "ACI Practice Exam 1 Q4 (verified)")

add("rates", "benchmarks", "theory", "easy",
    "EONIA was best described as:",
    ["An ECB policy rate corridor ceiling",
     "A volume-weighted average of euro overnight unsecured interbank rates",
     "A simple average of EURIBOR panel quotes",
     "The Bank of England bank rate"],
    1,
    "EONIA was the euro overnight index average — volume-weighted unsecured overnight. It has been "
    "replaced by €STR (Euro Short-Term Rate) as of 2022 for most new use.",
    "Tutorial Letter 03 / 2025 guide")

add("rates", "benchmarks", "theory", "medium",
    "Which is the euro risk-free overnight rate that replaced EONIA?",
    ["EURIBOR", "€STR (ESTR)", "SONIA", "SOFR"],
    1,
    "€STR is the euro short-term rate administered by the ECB; SONIA is GBP, SOFR is USD.",
    "2025 Study Guide §3")

add("rates", "forward-rates", "calculation", "hard",
    "USD 90-day rate 6.57%, 183-day rate 6.73% (ACT/360). The 3v6 forward-forward rate is closest to:",
    ["6.850%", "6.776%", "6.888%", "6.838%"],
    0,
    "FF = {[1 + r_long×D_long/360] / [1 + r_short×D_short/360] − 1} × 360/(D_long−D_short). "
    "Numerator 1 + 0.0673×183/360 = 1.034218; denominator 1 + 0.0657×90/360 = 1.016425; "
    "ratio 1.017505; −1 → 0.017505; ×360/93 ≈ 0.06776? Recalc: "
    "(1.034218/1.016425 − 1) × 360/93 = 0.017505 × 3.87097 ≈ 0.06776 = 6.776%. "
    "Answer B 6.776%.",
    "ACI Practice Exam 5 Q37 style")

# Fix answer to B
questions[-1]["answer"] = 1
questions[-1]["explanation"] = (
    "Forward-forward = {[1 + r_L D_L/360]/[1 + r_S D_S/360] − 1} × 360/(D_L − D_S). "
    "1 + 0.0673×183/360 = 1.0342175; 1 + 0.0657×90/360 = 1.016425; ratio − 1 = 0.017504; "
    "× 360/93 ≈ 6.776%."
)

add("rates", "repo", "theory", "medium",
    "In a classic repo, if a coupon is paid on the collateral during the term:",
    ["The buyer keeps the coupon with no further obligation",
     "The issuer pays the buyer, who must pay an equivalent amount through to the seller (manufactured payment)",
     "The issuer pays the seller directly and the repo ignores it",
     "The coupon is always added to the repo rate instead"],
    1,
    "Legal title sits with the buyer, so the issuer pays the buyer; under a classic repo the buyer "
    "manufactures an equivalent payment back to the seller.",
    "Tutorial Letter 03 / Practice Exam 1 Q9")

add("rates", "repo", "theory", "medium",
    "A key legal difference between a classic repo and an undocumented sell/buy-back is:",
    ["Classic repo is one contract; undocumented SBB is two separate contracts",
     "Only SBB transfers legal title",
     "Classic repo never moves custody of collateral",
     "SBB always requires variation margin"],
    0,
    "A classic repo is a single repurchase agreement. An undocumented sell/buy-back is economically "
    "similar but documented as two outright trades.",
    "Practice Exam 1 Q11")

add("rates", "bonds", "theory", "easy",
    "Accrued interest on a bond compensates the seller for:",
    ["Credit spread only",
     "Coupon earned since the last coupon date but not yet paid",
     "The issuer's underwriting fee",
     "Expected future dividends"],
    1,
    "Dirty price = clean price + accrued. Accrued is the portion of the next coupon earned by the "
    "seller up to settlement.",
    "Tutorial Letter 03")

add("rates", "money-market-instruments", "theory", "easy",
    "Which instrument is typically issued at a discount and pays no coupon?",
    ["Fixed-rate corporate bond", "Treasury bill", "Floating-rate note", "Convertible bond"],
    1,
    "T-bills (and many CP/BA instruments) are discount instruments — redeemed at face value with "
    "the return embedded in the discount.",
    "2025 Study Guide §3")

add("rates", "discount-instruments", "calculation", "medium",
    "A 90-day T-bill with face 100 is priced at 98.50 on an ACT/360 discount basis. The discount "
    "rate is closest to:",
    ["6.00%", "6.08%", "1.50%", "5.40%"],
    0,
    "Discount rate d = ((F − P)/F) × (basis/days) = (1.50/100) × (360/90) = 0.015 × 4 = 6.00%.",
    "Tutorial Letter 03")

# ========== FICC ==========
add("ficc", "fra", "theory", "easy",
    "Buying a FRA is economically equivalent to:",
    ["Locking in a borrowing rate (hedging a future loan)",
     "Locking in a lending rate only via futures",
     "Buying the bond outright",
     "Selling an interest-rate call"],
    0,
    "A FRA buyer is compensated when rates fix above the FRA rate — the hedge used by a future "
    "borrower. A FRA seller hedges a future deposit/loan made.",
    "Tutorial Letter 04")

add("ficc", "fra", "calculation", "hard",
    "You buy a FRA on EUR 500m at 0.50%. Fixing is 0.75%. Period = 334 days (ACT/360). Settlement "
    "amount (to the FRA buyer) is closest to:",
    ["Pay 2,303,417", "Receive 1,154,367", "Receive 1,159,722", "Receive 1,151,708"],
    3,
    "Settlement = Notional × (L − F) × d/360 / [1 + L×d/360]. "
    "Numerator 500m × 0.0025 × 334/360 = 1,159,722.22; discount factor 1 + 0.0075×334/360 = 1.006958; "
    "1,159,722.22 / 1.006958 ≈ 1,151,708. Buyer receives because fixing > FRA rate.",
    "ACI Practice Exam 5 Q39 (verified)")

add("ficc", "futures", "theory", "easy",
    "A 3-month Eurodollar futures price of 95.30 implies a futures rate of:",
    ["95.30%", "4.70%", "5.30%", "0.953%"],
    1,
    "STIR futures price ≈ 100 − implied rate ⇒ rate = 100 − 95.30 = 4.70%.",
    "Tutorial Letter 04")

add("ficc", "futures", "calculation", "medium",
    "You sell 20 Eurodollar futures at 95.30. Same-day close is 95.20. P&L is:",
    ["USD 5,000 profit", "USD 5,000 loss", "USD 50,000 profit", "USD 50,000 loss"],
    0,
    "Each 0.01 (1 bp) on a Eurodollar future = USD 25 per contract. Price rose in rate terms "
    "(futures price fell 10 bp): short futures profits. 20 × 10 bp × USD 25 = USD 5,000 profit.",
    "ACI Practice Exam 5 Q41 (verified)")

add("ficc", "irs", "theory", "medium",
    "In a plain-vanilla payer IRS, the party:",
    ["Pays fixed and receives floating",
     "Pays floating and receives fixed",
     "Pays fixed in one currency and fixed in another",
     "Only exchanges notionals each period"],
    0,
    "A payer swap pays fixed / receives floating — used to hedge floating-rate liabilities or to "
    "express a view that rates will rise. Notionals on a standard IRS are not exchanged.",
    "Tutorial Letter 04")

add("ficc", "ois", "theory", "medium",
    "An overnight index swap (OIS) floating leg compounds which type of rate?",
    ["A 6-month term LIBOR fixing only",
     "Daily overnight risk-free rates (e.g. SOFR, SONIA, €STR)",
     "The central bank's corridor ceiling exclusively",
     "Equity dividend yields"],
    1,
    "OIS floating legs compound overnight RFRs over the calculation period and pay versus fixed.",
    "2025 Study Guide §4")

add("ficc", "fx-options", "theory", "easy",
    "The buyer of a EUR call / USD put has the right to:",
    ["Sell EUR against USD at the strike",
     "Buy EUR against USD at the strike",
     "Must buy EUR at spot whatever happens",
     "Receive the strike in gold"],
    1,
    "A call on the base currency is the right to buy the base (EUR) / sell the quote (USD) at strike.",
    "Tutorial Letter 04")

add("ficc", "option-pricing", "theory", "medium",
    "All else equal, higher implied volatility:",
    ["Always lowers both call and put premiums",
     "Raises both call and put premiums",
     "Affects only puts",
     "Changes delta but never premium"],
    1,
    "Vega is positive for long vanilla calls and puts — higher IV ⇒ richer option premiums.",
    "Tutorial Letter 04")

add("ficc", "option-strategies", "theory", "medium",
    "A long straddle is constructed by:",
    ["Buying a call and selling a put at the same strike",
     "Buying a call and buying a put at the same strike (and usually same expiry)",
     "Buying two calls at different strikes",
     "Selling a call spread"],
    1,
    "Long straddle = long call + long put, typically same strike/expiry — profits from a large move "
    "in either direction if realised volatility beats implied.",
    "Workshop Options")

add("ficc", "ir-options", "theory", "medium",
    "A borrower hedging against higher rates with options would typically:",
    ["Sell a cap", "Buy a cap", "Sell a floor", "Buy a receiver swaption only to raise rates"],
    1,
    "A cap pays when the floating index exceeds the strike — the classic option hedge for a borrower. "
    "Floors protect lenders/investors against lower rates.",
    "Tutorial Letter 04")

# ========== FMA ==========
add("fma", "basel", "theory", "easy",
    "Under Basel, RWA stands for:",
    ["Risk Weighted Assets", "Risk Weighted Average", "Recovery Weighted Assets", "Risk Weighted Adjustments"],
    0,
    "Capital ratios are expressed as eligible capital divided by risk-weighted assets (RWA).",
    "Workshop Risk / 2025 §5")

add("fma", "basel", "theory", "medium",
    "The Basel III Liquidity Coverage Ratio (LCR) requires banks to hold enough HQLA to cover:",
    ["Net cash outflows over a 30-day stress scenario",
     "All assets to maturity beyond 5 years",
     "Only equity trading losses",
     "Operational risk events over 10 years"],
    0,
    "LCR = HQLA / net cash outflows under a prescribed 30-day stress ≥ 100%.",
    "2025 Study Guide §5")

add("fma", "basel", "theory", "medium",
    "Which of the following is NOT a Level 1 HQLA for LCR purposes?",
    ["Coins and banknotes",
     "Central-bank reserves",
     "Claims on sovereigns with a 0% risk weight",
     "Covered bonds"],
    3,
    "Covered bonds are typically Level 2 (subject to haircuts/caps), not Level 1. Level 1 includes "
    "cash, central-bank reserves and 0% RW sovereigns (with conditions).",
    "Workshop detailed solutions")

add("fma", "basel", "theory", "medium",
    "For NSFR, common equity typically carries an Available Stable Funding (ASF) factor of:",
    ["0%", "50%", "85%", "100%"],
    3,
    "Common equity is assigned a 100% ASF factor — it is the most stable funding source over the "
    "1-year NSFR horizon.",
    "Workshop Risk explanations")

add("fma", "var", "theory", "medium",
    "Value-at-Risk (VaR) at 99% / 1-day of USD 5m means:",
    ["The firm will lose exactly USD 5m tomorrow",
     "Under the model, a 1-day loss worse than USD 5m is expected only 1% of the time",
     "Capital required is always USD 5m",
     "Credit spreads cannot move"],
    1,
    "VaR is a probabilistic loss threshold for a horizon and confidence level — not a maximum loss "
    "and not a capital formula by itself (though Basel uses VaR-based market-risk charges historically).",
    "2025 Study Guide §5")

add("fma", "alm", "theory", "medium",
    "Duration gap analysis is primarily used to assess:",
    ["FX settlement risk",
     "Sensitivity of equity/economic value to interest-rate moves",
     "Operational cyber risk",
     "AML alert volumes"],
    1,
    "Duration gap compares duration of assets vs liabilities to gauge how the market value of equity "
    "moves when yields change.",
    "Workshop ALM")

add("fma", "gap-analysis", "theory", "medium",
    "A bank that is 'asset sensitive' (positive gap) in a period generally benefits when:",
    ["Interest rates fall", "Interest rates rise", "FX volatility falls", "Equity markets rally only"],
    1,
    "Positive gap (RSA > RSL) means more assets than liabilities reprice in the bucket — net interest "
    "income rises when rates rise.",
    "Workshop ALM")

add("fma", "credit-risk", "theory", "medium",
    "Wrong-way risk arises when:",
    ["Exposure to a counterparty rises as that counterparty's creditworthiness deteriorates",
     "Collateral haircuts are too large",
     "VaR uses a 1-day horizon",
     "LCR is above 100%"],
    0,
    "Example: buying credit protection on insurers from an insurer, or lending to a gold miner while "
    "being long gold forwards that hurt the miner when gold falls — exposure and default likelihood "
    "move together.",
    "Workshop Risk detailed solutions")

add("fma", "liquidity-risk", "theory", "easy",
    "Funding liquidity risk is the risk that:",
    ["A bank cannot meet cash obligations as they fall due without costly measures",
     "A bond's mid-price is stale on the screen",
     "Delta of an option is misestimated",
     "A sovereign is upgraded"],
    0,
    "Funding liquidity = ability to raise cash/pay obligations. Market liquidity = ability to exit "
    "positions without moving the price — related but distinct.",
    "2025 Study Guide §5")

add("fma", "operational-risk", "theory", "easy",
    "Under Basel, operational risk includes losses from:",
    ["Equity price moves only",
     "Failed processes, people, systems, or external events",
     "Parallel yield-curve shifts only",
     "FX delta only"],
    1,
    "Operational risk is the risk of loss from inadequate or failed internal processes, people and "
    "systems, or from external events (including legal risk in Basel's definition).",
    "2025 Study Guide §5")

add("fma", "transfer-pricing", "theory", "hard",
    "Modern matched-maturity funds transfer pricing in banks typically:",
    ["Uses one flat transfer rate for all tenors",
     "Differentiates FTP by maturity and reflects marginal funding cost (plus liquidity premia)",
     "Ignores the wholesale curve entirely",
     "Applies only to the trading book"],
    1,
    "Matched-maturity FTP assigns a tenor-specific transfer rate so businesses are charged/credited "
    "the marginal cost of funds for the commitment's maturity, often with liquidity add-ons.",
    "Workshop ALM")

add("fma", "market-risk", "theory", "medium",
    "Interest-rate risk in the banking book (IRRBB) is primarily concerned with:",
    ["Trading-desk FX options only",
     "How rate moves affect NII and the economic value of banking-book positions",
     "Settlement fails in CLS",
     "Card-fraud operational losses"],
    1,
    "IRRBB covers the banking book: net interest income sensitivity and economic-value sensitivity "
    "to rate shocks — now also emphasised under Basel frameworks.",
    "2025 Study Guide §5")

# More originals to bulk up coverage
add("fx", "fx-risk", "theory", "medium",
    "Replacement risk (pre-settlement risk) on an FX forward is the risk that:",
    ["The counterparty defaults before settlement and the trade must be replaced at a worse rate",
     "CLS fails to open",
     "The dealing system loses power during the quote",
     "The currency is redenominated overnight always"],
    0,
    "Pre-settlement / replacement risk is the positive MtM exposure if the counterparty defaults "
    "before the value date; settlement risk is the principal exchange risk on the value date.",
    "Tutorial Letter 02")

add("rates", "central-bank-ops", "theory", "medium",
    "A central-bank reverse repo (from the commercial bank's perspective receiving cash) typically:",
    ["Drains liquidity from the banking system when the CB does it as a liquidity-absorbing op",
     "Always injects gold into vaults",
     "Sets the corporate tax rate",
     "Is identical to an equity underwriting"],
    0,
    "Terminology varies by jurisdiction, but when the central bank borrows cash against collateral "
    "(liquidity-absorbing reverse repo), it drains system liquidity.",
    "ICAP Module 3")

add("rates", "yield-curve", "theory", "medium",
    "A positively sloped (normal) yield curve most often indicates:",
    ["Short rates above long rates",
     "Long-term rates above short-term rates",
     "Identical rates at all tenors",
     "Negative policy rates only"],
    1,
    "A normal curve has longer tenors yielding more than shorter tenors, embedding term premium and "
    "expected future short rates.",
    "2025 Study Guide §3")

add("ficc", "ccs", "theory", "hard",
    "A cross-currency basis swap typically exchanges:",
    ["Only equity notional",
     "Principal in two currencies at start/end plus floating interest in each currency",
     "Gold for silver monthly",
     "A single premium for a vanilla FX option"],
    1,
    "Cross-currency swaps usually exchange notionals at start and re-exchange at maturity, with each "
    "party paying floating (or fixed) in one currency — the basis reflects supply/demand for each "
    "currency's funding.",
    "2025 Study Guide §4")

add("fme", "participants", "theory", "easy",
    "Market makers in FX typically:",
    ["Only take customer orders without risking capital",
     "Provide continuous bid/offer quotes and manage inventory risk",
     "Set national fiscal policy",
     "Act solely as retail money changers"],
    1,
    "Market makers quote two-way prices, supply liquidity and warehouse risk until they can hedge "
    "or unwind.",
    "ICAP Module 1")

add("fme", "trade-lifecycle", "theory", "medium",
    "Which function should be segregated from the dealing room under good market practice?",
    ["Pricing of customer FX quotes",
     "Independent confirmation and settlement/operations",
     "Economic research commentary",
     "Voice brokerage contact"],
    1,
    "Front-to-back controls require independent confirmation/settlement so dealers cannot alone "
    "originate, confirm and settle trades (a classic Model Code / Global Code theme).",
    "Tutorial Letter 01 / Model Code")

add("fx", "fx-theory", "theory", "medium",
    "Interest-rate parity links FX forward points primarily to:",
    ["Equity index levels",
     "Interest-rate differentials between the two currencies",
     "The gold lease rate only",
     "GDP revision magnitude only"],
    1,
    "Covered interest parity: forward points ≈ spot × (r_quote − r_base) × days/basis (with day-count "
    "details). The higher-yielding currency trades at a forward discount.",
    "Tutorial Letter 02")

add("rates", "simple-compound", "calculation", "medium",
    "EUR 25,000,000 for 91 days at 3.25% (ACT/360). Interest is closest to:",
    ["EUR 205,295", "EUR 203,125", "EUR 812,500", "EUR 73,785"],
    0,
    "I = 25m × 0.0325 × 91/360 = 25m × 0.0082153 = 205,381.9… ≈ 205,295 depending on rounding; "
    "25,000,000 × 0.0325 × 91/360 = 205,381.94. Closest listed standard exam figure often 205,295 "
    "with slight day/rate variants — using exact: 205,381.94. Adjust option A to exact.",
    "Tutorial Letter 03")

questions[-1]["options"] = ["EUR 205,381.94", "EUR 203,125.00", "EUR 812,500.00", "EUR 73,958.33"]
questions[-1]["explanation"] = (
    "Interest = 25,000,000 × 0.0325 × 91/360 = 205,381.94."
)

add("ficc", "fra", "theory", "medium",
    "A 3x6 FRA covers a 3-month rate starting in:",
    ["0 months", "3 months", "6 months", "9 months"],
    1,
    "FRA notation AxB: the rate period starts in A months and ends in B months. 3x6 starts in 3 "
    "months and ends in 6 (a 3-month underlying).",
    "Tutorial Letter 04")

add("fma", "credit-risk", "theory", "medium",
    "Exposure at Default (EAD) × Loss Given Default (LGD) × Probability of Default (PD) is the "
    "usual expression for:",
    ["Expected loss", "Unexpected loss only", "VaR at 99.9%", "NSFR required stable funding"],
    0,
    "Expected loss ≈ PD × LGD × EAD. Unexpected loss is the variability around that expectation "
    "and drives economic/regulatory capital.",
    "Workshop Risk")


# ========== FLASHCARDS ==========
cards = []
c = 0


def card(topic, sub, front, back, src=""):
    global c
    c += 1
    cards.append(FC(c, topic, sub, front, back, src))


card("fme", "market-functions", "List 4 functions of financial markets.",
     "Price discovery; mobilisation of capital; provision of liquidity; transfer/distribution of risk "
     "(also: lower transaction costs, information, access, global allocation).",
     "ICAP Module 1")
card("fme", "code-of-conduct", "Is the FX Global Code legally binding?",
     "No — it is a voluntary set of principles of good practice, reinforced by Statements of Commitment "
     "and supervisory expectations, but not a statute by itself.",
     "FX Global Code")
card("fme", "code-of-conduct", "Name the FX Global Code principle themes (high level).",
     "Ethics; Governance; Execution; Information sharing; Risk management & compliance; "
     "Confirmation & settlement.",
     "FX Global Code")
card("fme", "settlement", "What risk does CLS mainly reduce?",
     "FX settlement (Herstatt) risk, via payment-versus-payment (PvP).",
     "2025 Study Guide")
card("fme", "aml-ethics", "Three stages of money laundering?",
     "Placement → Layering → Integration.",
     "Tutorial Letter 01")
card("fme", "regulation", "EMIR reporting timing for OTC & ETD?",
     "Both reported to trade repositories on a T+1 (following day) basis under EMIR rules taught in the materials.",
     "Workshop Topic 1")
card("fme", "efficient-markets", "Semi-strong EMH means prices reflect…?",
     "All publicly available information.",
     "2025 Study Guide")
card("fme", "market-structure", "Primary vs secondary market?",
     "Primary: new issuance / capital raising. Secondary: trading of existing securities.",
     "Tutorial Letter 01")
card("fme", "central-banks", "Purpose of open-market operations?",
     "Manage banking-system liquidity and steer short-term interest rates.",
     "ICAP Module 1")
card("fme", "participants", "What does a market maker do?",
     "Quotes two-way prices, provides liquidity, and manages inventory/risk.",
     "ICAP Module 1")

card("fx", "fx-quotes", "In EUR/USD, which is base / quote?",
     "EUR is base; USD is quote. Price = USD per 1 EUR.",
     "Tutorial Letter 02")
card("fx", "fx-quotes", "Customer buys base currency — which side of the quote?",
     "The offer (ask) side of the market maker's quote.",
     "Tutorial Letter 02")
card("fx", "value-dates", "Standard spot value date for EUR/USD?",
     "T+2. (USD/CAD is typically T+1.)",
     "Tutorial Letter 02")
card("fx", "forward-points", "Ascending vs descending forward points?",
     "Ascending (low/high) = premium; descending (high/low) = discount (apply as negative).",
     "Tutorial Letter 02")
card("fx", "outright-forwards", "Outright ≈ ?",
     "Outright = Spot + Forward points (with correct sign and bid/offer side).",
     "Tutorial Letter 02")
card("fx", "fx-theory", "Covered interest parity intuition?",
     "Higher-yielding currency trades at a forward discount; points ≈ spot × interest differential × time.",
     "Tutorial Letter 02")
card("fx", "ndf", "How does an NDF settle?",
     "Cash settlement of the difference vs a fixing, usually in USD — no local-currency delivery.",
     "2025 Study Guide")
card("fx", "precious-metals", "LBMA Good Delivery gold fineness & weight?",
     "Min fineness 0.995; gold content 350–430 fine troy oz (≈400 typical).",
     "ICAP Module 2")
card("fx", "precious-metals", "ISO codes XAU / XAG?",
     "XAU = gold; XAG = silver (also XPT platinum, XPD palladium).",
     "Tutorial Letter 02")
card("fx", "fx-swaps", "Sell/buy FX swap on base currency means you…?",
     "Lend the base / borrow the quote for the tenor (short base until far leg).",
     "2025 Study Guide")
card("fx", "cross-rates", "Multiplying cross with USD in the middle — bid side?",
     "Generally multiply bid × bid for the cross bid (and offer × offer for the offer), watching quote order.",
     "Tutorial Letter 02")
card("fx", "fx-risk", "Pre-settlement vs settlement risk?",
     "Pre-settlement: replacement cost if default before value date. Settlement: loss of principal on exchange day.",
     "Tutorial Letter 02")

card("rates", "day-counts", "ACT/360 currencies (examples)?",
     "USD, EUR, CHF, JPY (most money-market currencies).",
     "Tutorial Letter 03")
card("rates", "day-counts", "ACT/365 currencies (examples)?",
     "GBP, AUD, NZD, HKD, SGD, ZAR (and others).",
     "Tutorial Letter 03")
card("rates", "simple-compound", "Simple interest formula (money market)?",
     "I = P × r × days/basis.",
     "Tutorial Letter 03")
card("rates", "benchmarks", "EONIA vs €STR?",
     "EONIA was volume-weighted euro overnight; replaced by €STR (ECB) for new business from 2022.",
     "2025 Study Guide")
card("rates", "benchmarks", "SOFR / SONIA / €STR / SARON / TONA — currencies?",
     "SOFR=USD, SONIA=GBP, €STR=EUR, SARON=CHF, TONA=JPY — overnight RFRs.",
     "2025 Study Guide")
card("rates", "interpolation", "Straight-line rate interpolation?",
     "r = r1 + (t−t1)/(t2−t1) × (r2−r1).",
     "Practice exams")
card("rates", "forward-rates", "Forward-forward rate formula (ACT/360)?",
     "FF = {[1+r_L D_L/360]/[1+r_S D_S/360] − 1} × 360/(D_L−D_S).",
     "Tutorial Letter 03")
card("rates", "repo", "Classic repo coupon during term?",
     "Issuer pays buyer; buyer makes manufactured payment to seller.",
     "Tutorial Letter 03")
card("rates", "repo", "Classic repo vs undocumented sell/buy-back?",
     "Classic = one repo contract; undocumented SBB = two outright contracts.",
     "Practice Exam 1")
card("rates", "bonds", "Clean vs dirty bond price?",
     "Dirty = clean + accrued interest.",
     "Tutorial Letter 03")
card("rates", "discount-instruments", "Discount rate on a T-bill?",
     "d = ((F−P)/F) × (basis/days).",
     "Tutorial Letter 03")
card("rates", "yield-curve", "Normal yield curve shape?",
     "Upward sloping: longer tenors yield more than shorter tenors.",
     "2025 Study Guide")
card("rates", "money-market-instruments", "Name three money-market instruments.",
     "Examples: interbank deposits, T-bills, CP, CDs, BAs, repo.",
     "2025 Study Guide")

card("ficc", "fra", "What does 2x5 FRA mean?",
     "Forward rate from 2 months to 5 months (3-month underlying starting in 2 months).",
     "Tutorial Letter 04")
card("ficc", "fra", "FRA settlement (buyer) intuition?",
     "Buyer receives if fixing > FRA rate (discounted difference × notional × d/basis).",
     "Tutorial Letter 04")
card("ficc", "fra", "FRA settlement formula?",
     "N × (L−F) × d/basis / [1 + L×d/basis].",
     "Tutorial Letter 04")
card("ficc", "futures", "Eurodollar futures price vs rate?",
     "Price ≈ 100 − rate; each bp typically USD 25 per contract.",
     "Tutorial Letter 04")
card("ficc", "irs", "Payer swap = ?",
     "Pay fixed / receive floating.",
     "Tutorial Letter 04")
card("ficc", "ois", "OIS floating leg?",
     "Compounds overnight RFR (SOFR/SONIA/€STR/etc.) over the period.",
     "2025 Study Guide")
card("ficc", "fx-options", "EUR call / USD put right?",
     "Right to buy EUR (sell USD) at the strike.",
     "Tutorial Letter 04")
card("ficc", "option-pricing", "Effect of higher IV on vanilla premiums?",
     "Raises both call and put premiums (positive vega).",
     "Tutorial Letter 04")
card("ficc", "option-strategies", "Long straddle components?",
     "Long call + long put (same strike/expiry).",
     "Workshop Options")
card("ficc", "ir-options", "Cap vs floor — who buys which?",
     "Borrowers buy caps (protection vs higher rates); investors/lenders buy floors.",
     "Tutorial Letter 04")
card("ficc", "ccs", "Cross-currency swap notionals?",
     "Usually exchanged at start and re-exchanged at maturity, with interest in each currency.",
     "2025 Study Guide")

card("fma", "basel", "What is RWA?",
     "Risk-Weighted Assets — denominator of regulatory capital ratios.",
     "Workshop Risk")
card("fma", "basel", "LCR definition?",
     "HQLA / net cash outflows over a 30-day stress ≥ 100%.",
     "2025 Study Guide")
card("fma", "basel", "NSFR definition?",
     "Available Stable Funding / Required Stable Funding over a 1-year horizon ≥ 100%.",
     "2025 Study Guide")
card("fma", "basel", "ASF factor for common equity?",
     "100%.",
     "Workshop explanations")
card("fma", "basel", "Level 1 HQLA examples?",
     "Cash, central-bank reserves, 0% RW sovereigns (conditions apply). Covered bonds are not Level 1.",
     "Workshop Risk")
card("fma", "var", "VaR meaning?",
     "A loss threshold for a horizon/confidence level (e.g. 99% 1-day) — not the maximum possible loss.",
     "2025 Study Guide")
card("fma", "alm", "Duration gap purpose?",
     "Measure sensitivity of equity/economic value to interest-rate changes.",
     "Workshop ALM")
card("fma", "gap-analysis", "Positive gap (asset sensitive) — rates up?",
     "Net interest income tends to rise.",
     "Workshop ALM")
card("fma", "credit-risk", "Expected loss ≈ ?",
     "PD × LGD × EAD.",
     "Workshop Risk")
card("fma", "credit-risk", "Wrong-way risk?",
     "Exposure rises as counterparty credit quality falls (positively correlated).",
     "Workshop Risk")
card("fma", "liquidity-risk", "Funding vs market liquidity risk?",
     "Funding: can't meet cash obligations. Market: can't exit positions without moving price.",
     "2025 Study Guide")
card("fma", "operational-risk", "Basel operational risk?",
     "Loss from failed processes, people, systems, or external events (includes legal risk).",
     "2025 Study Guide")
card("fma", "transfer-pricing", "Matched-maturity FTP idea?",
     "Tenor-specific transfer rates reflecting marginal funding cost (+ liquidity premia).",
     "Workshop ALM")
card("fma", "market-risk", "IRRBB focuses on?",
     "Banking-book NII and economic-value sensitivity to interest-rate shocks.",
     "2025 Study Guide")

# Exam structure cards
card("fme", "market-structure", "ACI Dealing Certificate exam format?",
     "70 MCQs, 2 hours. Pass 60% (42/70) with ≥50% in each topic basket. Merit 70%+, Distinction 80%+.",
     "2025 Study Guide intro")
card("fme", "market-structure", "Topic basket sizes on the exam?",
     "FME 10, FX 18, Rates 18, FICC 14, FMA 10 (=70). Min correct: 5, 9, 9, 7, 5.",
     "ICAP intro / ACI syllabus")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # re-number ORIG ids sequentially in case of edits
    for i, q in enumerate(questions, 1):
        q["id"] = f"ORIG-{i:03d}"
    for i, f in enumerate(cards, 1):
        f["id"] = f"FC-{i:03d}"
    qp = OUT / "ORIG.questions.json"
    fp = OUT / "ORIG.flashcards.json"
    qp.write_text(json.dumps(questions, indent=2, ensure_ascii=False))
    fp.write_text(json.dumps(cards, indent=2, ensure_ascii=False))
    print(f"questions={len(questions)} flashcards={len(cards)}")


if __name__ == "__main__":
    main()
