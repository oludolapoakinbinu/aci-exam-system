"""Append additional flashcards covering syllabus facts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data" / "raw" / "ORIG.flashcards.json"
cards = json.loads(path.read_text())
start = len(cards)

extra = [
    ("fx", "value-dates", "What is tom/next (T/N)?",
     "An FX swap from tomorrow to the spot date (next) — used to roll positions and derive value-tomorrow rates."),
    ("fx", "value-dates", "What is spot/next?",
     "An FX swap from spot to the following business day."),
    ("fx", "forward-points", "Pip vs pipette (EUR/USD)?",
     "A pip is usually the 4th decimal (0.0001); a pipette is a 5th decimal (0.00001). JPY pairs often use 2nd/3rd decimals."),
    ("fx", "ndf", "Why use NDFs?",
     "For currencies with convertibility/delivery constraints — hedge FX risk without delivering the non-convertible currency."),
    ("fx", "precious-metals", "Allocated vs unallocated loco account?",
     "Allocated: specific bars owned. Unallocated: claim on the bullion bank's general pool (most London OTC trading)."),
    ("fx", "precious-metals", "Silver Good Delivery fineness?",
     "Minimum fineness 0.999; recommended weight about 750–1,100 troy oz (~1,000 typical)."),
    ("rates", "benchmarks", "What was LIBOR conceptually?",
     "London Interbank Offered Rate — panel banks' offered interbank funding rates across tenors/currencies; largely replaced by RFRs."),
    ("rates", "benchmarks", "EURIBOR is…?",
     "Euro Interbank Offered Rate — unsecured euro term fixing from a panel (still used; reformed methodology)."),
    ("rates", "repo", "General collateral (GC) vs special?",
     "GC: any issue from an accepted basket. Special: a specific ISIN in demand, often trading richer (lower repo rate)."),
    ("rates", "repo", "Haircut / initial margin purpose?",
     "Protects the cash lender against collateral price falls — borrower delivers extra collateral value."),
    ("rates", "bonds", "Day-count often used for US Treasuries accrued?",
     "ACT/ACT (with specific conventions). Many eurobonds historically 30/360."),
    ("rates", "money-market-instruments", "CD vs deposit?",
     "Certificate of Deposit is typically transferable; interbank deposits are usually non-transferable bilateral loans."),
    ("rates", "forward-rates", "Break-even forward rate idea?",
     "The rate that equalises rolling short deposits vs locking a longer deposit — no-arbitrage forward-forward."),
    ("ficc", "futures", "Long Eurodollar futures = view on rates?",
     "Long futures profits when futures price rises ⇒ implied rate falls. Hedge for a future lender/investor."),
    ("ficc", "futures", "Short Eurodollar futures hedge?",
     "Hedge for a future borrower: profits when rates rise (futures price falls)."),
    ("ficc", "irs", "Receiver swap = ?",
     "Receive fixed / pay floating."),
    ("ficc", "irs", "Are notionals exchanged on a standard single-currency IRS?",
     "No — only interest differentials are exchanged (net)."),
    ("ficc", "option-pricing", "Delta of an option?",
     "Sensitivity of premium to a small move in the underlying price/rate."),
    ("ficc", "option-pricing", "Theta?",
     "Sensitivity of premium to the passage of time (time decay) — usually negative for long vanillas."),
    ("ficc", "option-strategies", "Risk reversal (FX)?",
     "Typically long OTM call + short OTM put (or reverse) — expresses skew / directional vol view."),
    ("ficc", "ir-options", "Collar for a borrower?",
     "Long cap + short floor — caps upside rate cost while giving up benefit below the floor strike."),
    ("fma", "basel", "Basel I headline capital ratio?",
     "Minimum capital (Tier 1+2) of 8% of risk-weighted assets for internationally active banks."),
    ("fma", "basel", "What is CCF?",
     "Credit Conversion Factor — converts certain off-balance-sheet items into on-balance credit exposure equivalents."),
    ("fma", "basel", "Standardized RW for many unrated corporates (classic teaching)?",
     "Often 100% (check current national tables — materials use this baseline)."),
    ("fma", "var", "Historical simulation VaR?",
     "Revalues the portfolio using past return scenarios and reads the loss quantile — few distributional assumptions."),
    ("fma", "alm", "NII vs EVE?",
     "Net Interest Income: earnings over a horizon. Economic Value of Equity: PV of assets − liabilities sensitivity."),
    ("fma", "liquidity-risk", "HQLA means?",
     "High-Quality Liquid Assets eligible for the LCR (Level 1 / Level 2A / 2B with haircuts)."),
    ("fme", "regulation", "Volcker Rule aim (as taught)?",
     "Limit proprietary trading and bank investments in hedge funds / private equity."),
    ("fme", "regulation", "Dodd-Frank high-level aim?",
     "Promote US financial stability via accountability/transparency and reduce taxpayer bailout risk."),
    ("fme", "regulation", "MiFID II applies broadly to…?",
     "Investment firms, venues, funds/managers and trading venues across EU financial markets (wholesale & retail perimeter)."),
    ("fme", "code-of-conduct", "UK Money Markets Code covers?",
     "Wholesale unsecured deposits, repo and related UK money-market activity (not general retail transactional banking)."),
    ("fx", "fx-quotes", "Cable means?",
     "Market slang for GBP/USD."),
    ("rates", "day-counts", "Interest on CHF deposit — basis?",
     "ACT/360."),
    ("rates", "simple-compound", "Compounding more frequently raises…?",
     "Effective annual yield versus a stated nominal rate with less frequent compounding."),
    ("ficc", "derivatives-general", "Exchange-traded vs OTC derivative?",
     "ETD: standardised, cleared, margined. OTC: bespoke, bilateral (increasingly cleared when mandated)."),
    ("fma", "risk-general", "Seven major risk groups in FMA syllabus?",
     "Market, credit, liquidity, operational, legal, regulatory, reputational."),
    ("fx", "forward-points", "Value-tomorrow from spot and T/N?",
     "Adjust spot by the tom/next swap points (careful with bid/offer direction when moving earlier than spot)."),
    ("rates", "repo", "Buy/sell-back documented variation/margin?",
     "If cash vs collateral values diverge significantly, adjustment is usually by re-pricing (vs variation margin on classic repo)."),
    ("ficc", "fra", "FRA settlement timing?",
     "Usually at the start of the FRA period (discounted); some markets may settle at end undiscounted — ACI teaches discounted start."),
    ("fma", "basel", "NSFR ASF 0% examples?",
     "Many short-term financial liabilities, derivatives, trading liabilities — cannot be relied on as stable funding."),
]

for topic, sub, front, back in extra:
    start += 1
    cards.append({
        "id": f"FC-{start:03d}",
        "topic": topic,
        "subtopic": sub,
        "front": front,
        "back": back,
        "source": "ACI study materials",
    })

# renumber
for i, c in enumerate(cards, 1):
    c["id"] = f"FC-{i:03d}"
path.write_text(json.dumps(cards, indent=2, ensure_ascii=False))
print(len(cards))
