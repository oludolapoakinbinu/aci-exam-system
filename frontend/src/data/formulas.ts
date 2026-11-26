export type FormulaItem = {
  id: string;
  topic: "fx" | "rates" | "ficc" | "fma" | "fme";
  title: string;
  formula: string;
  notes: string;
  variables?: string;
};

export const FORMULA_SECTIONS: {
  id: string;
  title: string;
  blurb: string;
  items: FormulaItem[];
}[] = [
  {
    id: "day-counts",
    title: "Day counts & simple interest",
    blurb: "Money-market interest uses actual days and a currency day basis.",
    items: [
      {
        id: "simple-int",
        topic: "rates",
        title: "Simple interest",
        formula: "I = P × r × (d / B)",
        variables: "P = principal · r = rate (decimal) · d = actual days · B = day basis (360 or 365)",
        notes:
          "ACT/360: USD, EUR, CHF, JPY (most MM currencies). ACT/365: GBP, AUD, NZD, HKD, SGD, ZAR (and others). Always use the currency’s market convention unless the question states otherwise.",
      },
      {
        id: "maturity",
        topic: "rates",
        title: "Maturity amount",
        formula: "FV = P × [1 + r × (d / B)]",
        notes: "Future value of a deposit/loan under simple money-market interest.",
      },
      {
        id: "rate-from-int",
        topic: "rates",
        title: "Implied rate from interest earned",
        formula: "r = (I / P) × (B / d)",
        notes: "Rearrangement of the simple interest formula — common exam item.",
      },
      {
        id: "interp",
        topic: "rates",
        title: "Straight-line rate interpolation",
        formula: "r_t = r₁ + [(t − t₁) / (t₂ − t₁)] × (r₂ − r₁)",
        notes: "Used for broken dates between two known tenors (rates or FX points).",
      },
    ],
  },
  {
    id: "yields",
    title: "Yield conversions & discount instruments",
    blurb: "Convert between compounding conventions and discount vs yield quotes.",
    items: [
      {
        id: "eff-semi",
        topic: "rates",
        title: "Annual effective → semi-annual bond basis",
        formula: "(1 + y/2)² = 1 + r_annual   ⇒   y = 2(√(1+r) − 1)",
        notes: "If an investment quotes 5% annual effective, semi-annual equivalent ≈ 4.939%.",
      },
      {
        id: "discount-rate",
        topic: "rates",
        title: "Discount rate (T-bill style)",
        formula: "d = ((F − P) / F) × (B / d_days)",
        variables: "F = face · P = price",
        notes: "Discount instruments are priced below face; return is embedded in the discount.",
      },
      {
        id: "investment-yield",
        topic: "rates",
        title: "Investment / true yield on a discount bill",
        formula: "y = ((F − P) / P) × (B / d_days)",
        notes: "Yield uses purchase price in the denominator; discount rate uses face.",
      },
      {
        id: "ff-rate",
        topic: "rates",
        title: "Forward-forward (break-even) interest rate",
        formula:
          "FF = { [1 + r_L×D_L/B] / [1 + r_S×D_S/B] − 1 } × B / (D_L − D_S)",
        notes:
          "No-arbitrage rate from the short date to the long date. Same basis B throughout (usually 360 for USD/EUR).",
      },
    ],
  },
  {
    id: "fx",
    title: "Foreign exchange",
    blurb: "Spot, points, outrights, crosses and interest-rate parity.",
    items: [
      {
        id: "outright",
        topic: "fx",
        title: "Outright forward",
        formula: "Outright = Spot + Forward points  (with correct sign & side)",
        notes:
          "Ascending points (low/high) = premium (add). Descending (high/low) = discount (subtract). Customer buying base deals on the offer; selling base deals on the bid.",
      },
      {
        id: "fwd-points",
        topic: "fx",
        title: "Forward points from interest rates (CIP)",
        formula:
          "Points ≈ Spot × [ (1 + i_Q×d/B_Q) / (1 + i_B×d/B_B) − 1 ]",
        variables: "i_Q = quoted-ccy rate · i_B = base-ccy rate · d = days",
        notes:
          "Exact ACI form uses each currency’s day basis. Positive points ⇒ base at premium (i_B < i_Q). Negative ⇒ base at discount.",
      },
      {
        id: "pip-scale",
        topic: "fx",
        title: "Pip / point scaling",
        formula: "Most pairs: 1 pip = 0.0001 · JPY pairs: 1 pip ≈ 0.01",
        notes:
          "21.5 EUR/USD points → 0.00215. 21.5 USD/JPY points → 0.215. Always confirm decimals in the question.",
      },
      {
        id: "cross-mult",
        topic: "fx",
        title: "Cross rate (USD in the middle, multiply)",
        formula: "EUR/JPY bid ≈ EUR/USD bid × USD/JPY bid",
        notes:
          "For offers use offer × offer. When dividing crosses, invert the appropriate pair and watch bid/offer sides carefully.",
      },
      {
        id: "value-tom",
        topic: "fx",
        title: "Value tomorrow from spot & T/N",
        formula: "Value-tomorrow ≈ Spot adjusted by tom/next swap points",
        notes:
          "Moving settlement earlier than spot reverses the usual far-leg point direction — use the T/N swap carefully on bid and offer.",
      },
      {
        id: "ndf",
        topic: "fx",
        title: "NDF settlement",
        formula: "Settlement = Notional × (Fixing − NDF rate) × scaling  (in USD usually)",
        notes: "No delivery of the non-convertible currency — cash-settle the difference vs fixing.",
      },
    ],
  },
  {
    id: "repo-bonds",
    title: "Bonds & repo",
    blurb: "Accrued interest, dirty price and repo cash amounts.",
    items: [
      {
        id: "dirty",
        topic: "rates",
        title: "Dirty bond price",
        formula: "Dirty = Clean + Accrued interest",
        notes: "Buyer pays dirty; accrued compensates seller for coupon earned since last pay date.",
      },
      {
        id: "repo-interest",
        topic: "rates",
        title: "Repo interest / repurchase price",
        formula: "Repo interest = Cash × r × (d / B) ·  Repurchase = Cash + Repo interest",
        notes:
          "Classic repo: one contract; manufactured coupon if collateral pays during the term. Undocumented sell/buy-back is two contracts.",
      },
      {
        id: "haircut",
        topic: "rates",
        title: "Haircut / initial margin",
        formula: "Cash ≈ Market value × (1 − haircut)",
        notes: "Protects the cash lender if collateral falls in value.",
      },
    ],
  },
  {
    id: "derivatives",
    title: "FRAs, futures, swaps & options",
    blurb: "Core FICC derivative formulae tested on the Dealing Certificate.",
    items: [
      {
        id: "fra-settle",
        topic: "ficc",
        title: "FRA settlement (discounted)",
        formula:
          "Settle = N × (L − F) × (d / B) / [1 + L × (d / B)]",
        variables: "N = notional · L = fixing · F = FRA rate · d = FRA period days",
        notes:
          "Buyer receives if L > F (borrower’s hedge). Settlement usually at start of the period, discounted.",
      },
      {
        id: "fra-notation",
        topic: "ficc",
        title: "FRA notation A×B",
        formula: "Starts in A months, ends in B months",
        notes: "3×6 = 3-month rate starting in 3 months. Buy FRA to hedge future borrowing.",
      },
      {
        id: "stir",
        topic: "ficc",
        title: "STIR / Eurodollar futures",
        formula: "Price ≈ 100 − rate ·  1 bp ≈ USD 25 per contract (3m USD)",
        notes:
          "Long futures profits when rates fall (price rises). Short futures hedge a future borrower.",
      },
      {
        id: "irs",
        topic: "ficc",
        title: "Interest rate swap",
        formula: "Payer = pay fixed / receive floating · Receiver = opposite",
        notes: "Standard single-currency IRS does not exchange notionals — only interest differentials.",
      },
      {
        id: "ois",
        topic: "ficc",
        title: "OIS floating leg",
        formula: "Compound overnight RFR over the period (SOFR / SONIA / €STR / …)",
        notes: "Fixed vs compounded overnight — the modern IRS floating index family.",
      },
      {
        id: "option-payoff",
        topic: "ficc",
        title: "Vanilla option payoff (long)",
        formula: "Call payoff = max(S − K, 0) · Put payoff = max(K − S, 0)",
        notes:
          "FX: EUR call / USD put = right to buy EUR (sell USD) at strike. Higher IV raises both call and put premiums (positive vega).",
      },
    ],
  },
  {
    id: "risk",
    title: "Risk, ALM & Basel",
    blurb: "Key ratios and risk expressions from Financial Markets Applications.",
    items: [
      {
        id: "el",
        topic: "fma",
        title: "Expected loss",
        formula: "EL ≈ PD × LGD × EAD",
        notes: "Unexpected loss (variability around EL) drives economic / regulatory capital.",
      },
      {
        id: "lcr",
        topic: "fma",
        title: "Liquidity Coverage Ratio (LCR)",
        formula: "LCR = HQLA / Net cash outflows (30-day stress) ≥ 100%",
        notes: "Level 1 HQLA: cash, CB reserves, 0% RW sovereigns. Covered bonds are not Level 1.",
      },
      {
        id: "nsfr",
        topic: "fma",
        title: "Net Stable Funding Ratio (NSFR)",
        formula: "NSFR = ASF / RSF (1-year) ≥ 100%",
        notes: "Common equity ASF factor = 100%. Many short-term wholesale liabilities have 0% ASF.",
      },
      {
        id: "cap-ratio",
        topic: "fma",
        title: "Capital ratio (Basel)",
        formula: "Capital ratio = Eligible capital / RWA",
        notes: "RWA = Risk-Weighted Assets. Classic Basel I minimum 8% for internationally active banks.",
      },
      {
        id: "var",
        topic: "fma",
        title: "Value-at-Risk (intuition)",
        formula: "VaR_α,T = loss threshold not expected to be exceeded with probability α over horizon T",
        notes: "e.g. 99% 1-day VaR of 5m ⇒ ~1% chance of a worse 1-day loss under the model — not a maximum loss.",
      },
      {
        id: "gap",
        topic: "fma",
        title: "Repricing gap",
        formula: "Gap = Rate-sensitive assets − Rate-sensitive liabilities (in a bucket)",
        notes: "Positive (asset-sensitive) gap: NII tends to rise when rates rise.",
      },
    ],
  },
];
