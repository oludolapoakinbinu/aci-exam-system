"use client";

import { useMemo, useState } from "react";
import { FORMULA_SECTIONS } from "@/data/formulas";

const TOPIC_FILTERS = [
  { id: "all", label: "All" },
  { id: "fx", label: "FX" },
  { id: "rates", label: "Rates" },
  { id: "ficc", label: "FICC" },
  { id: "fma", label: "Risk / ALM" },
];

export default function FormulasPage() {
  const [topic, setTopic] = useState("all");
  const [q, setQ] = useState("");

  const sections = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return FORMULA_SECTIONS.map((sec) => ({
      ...sec,
      items: sec.items.filter((item) => {
        if (topic !== "all" && item.topic !== topic) return false;
        if (!needle) return true;
        const blob = `${item.title} ${item.formula} ${item.notes} ${item.variables || ""}`.toLowerCase();
        return blob.includes(needle);
      }),
    })).filter((sec) => sec.items.length > 0);
  }, [topic, q]);

  return (
    <div style={{ maxWidth: 900 }}>
      <h1 style={{ margin: "8px 0 6px", fontSize: "1.8rem" }}>Formula sheet</h1>
      <p className="muted" style={{ marginTop: 0, marginBottom: 18 }}>
        ACI Dealing Certificate (002-101) formulae — day counts, FX outrights, FRAs, futures, repo and
        Basel ratios. Keep this open while you practise calculation questions.
      </p>

      <div className="panel" style={{ display: "flex", flexWrap: "wrap", gap: 10, marginBottom: 18 }}>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {TOPIC_FILTERS.map((t) => (
            <button
              key={t.id}
              type="button"
              className={`chip ${topic === t.id ? "active" : ""}`}
              onClick={() => setTopic(t.id)}
            >
              {t.label}
            </button>
          ))}
        </div>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search formulae…"
          style={{
            flex: 1,
            minWidth: 180,
            border: "1px solid var(--line)",
            borderRadius: 999,
            padding: "10px 14px",
          }}
        />
      </div>

      <div style={{ display: "grid", gap: 18 }}>
        {sections.map((sec) => (
          <section key={sec.id} className="panel">
            <h2 style={{ margin: "0 0 4px", fontSize: "1.2rem" }}>{sec.title}</h2>
            <p className="muted" style={{ marginTop: 0, marginBottom: 14, fontSize: 14 }}>
              {sec.blurb}
            </p>
            <div style={{ display: "grid", gap: 12 }}>
              {sec.items.map((item) => (
                <article
                  key={item.id}
                  style={{
                    border: "1px solid var(--line)",
                    borderRadius: 14,
                    padding: 14,
                    background: "var(--shell)",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      gap: 8,
                      flexWrap: "wrap",
                      marginBottom: 8,
                    }}
                  >
                    <strong>{item.title}</strong>
                    <span className="chip" style={{ textTransform: "uppercase" }}>
                      {item.topic}
                    </span>
                  </div>
                  <pre
                    style={{
                      margin: 0,
                      padding: "12px 14px",
                      borderRadius: 12,
                      background: "#1f2430",
                      color: "#f8fafc",
                      fontFamily: "var(--font-geist-mono), ui-monospace, monospace",
                      fontSize: 13,
                      whiteSpace: "pre-wrap",
                      overflowX: "auto",
                    }}
                  >
                    {item.formula}
                  </pre>
                  {item.variables && (
                    <div className="muted" style={{ fontSize: 13, marginTop: 8 }}>
                      {item.variables}
                    </div>
                  )}
                  <div style={{ fontSize: 14, marginTop: 8, lineHeight: 1.5 }}>{item.notes}</div>
                </article>
              ))}
            </div>
          </section>
        ))}

        {sections.length === 0 && (
          <div className="panel muted" style={{ textAlign: "center" }}>
            No formulae match that filter.
          </div>
        )}
      </div>

      <p className="muted" style={{ fontSize: 12, marginTop: 20 }}>
        Conventions follow the course materials (ICAP / Tridge ACI Dealing Certificate). Always read the
        question for the stated day count and quoting convention.
      </p>
    </div>
  );
}
