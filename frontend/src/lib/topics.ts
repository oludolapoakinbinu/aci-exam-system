export const TOPIC_META: Record<
  string,
  { name: string; short: string; color: string }
> = {
  fme: { name: "Financial Markets Environment", short: "FME", color: "#0ea5e9" },
  fx: { name: "Foreign Exchange", short: "FX", color: "#8b5cf6" },
  rates: { name: "Rates", short: "Rates", color: "#10b981" },
  ficc: { name: "FICC Derivatives", short: "FICC", color: "#f59e0b" },
  fma: { name: "Financial Markets Applications", short: "FMA", color: "#ef4444" },
};

export function topicName(code: string) {
  return TOPIC_META[code]?.name || code;
}

export function topicColor(code: string) {
  return TOPIC_META[code]?.color || "#64748b";
}
