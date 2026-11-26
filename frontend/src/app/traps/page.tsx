"use client";

import { Suspense, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { TRAP_SECTIONS } from "@/data/traps";

const TOPIC_FILTERS = [
  { id: "all", label: "All sections" },
  { id: "fme", label: "FME" },
  { id: "fx", label: "FX" },
  { id: "rates", label: "Rates" },
  { id: "ficc", label: "FICC" },
  { id: "fma", label: "FMA" },
];

function TrapsContent() {
  const params = useSearchParams();
  const initial = params.get("topic");
  const valid = TOPIC_FILTERS.some((t) => t.id === initial);
  const [topic, setTopic] = useState(valid && initial ? initial : "all");
  const [q, setQ] = useState("");

  const sections = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return TRAP_SECTIONS.map((sec) => ({
      ...sec,
      items: sec.items.filter((item) => {
        if (topic !== "all" && item.topic !== topic) return false;
        if (!needle) return true;
        const blob = `${item.title} ${item.trap} ${item.correct} ${item.tip} ${item.subtopic || ""}`.toLowerCase();
        return blob.includes(needle);
      }),
    })).filter((sec) => sec.items.length > 0);
  }, [topic, q]);

  const total = sections.reduce((n, s) => n + s.items.length, 0);

  return (
    <div style={{ maxWidth: 900 }}>
      <h1 style={{ margin: "8px 0 6px", fontSize: "1.8rem" }}>Exam traps</h1>
      <p className="muted" style={{ marginTop: 0, marginBottom: 18 }}>
        Common ACI Dealing Certificate (002-101) mistakes by syllabus section — side/sign errors, day
        basis mix-ups, hedge direction, and wording traps. {total} traps loaded
        {topic !== "all" ? ` in this filter` : ""}.
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
          placeholder="Search traps…"
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
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                gap: 8,
                flexWrap: "wrap",
                alignItems: "baseline",
              }}
            >
              <h2 style={{ margin: "0 0 4px", fontSize: "1.2rem" }}>{sec.title}</h2>
              <span className="chip" style={{ textTransform: "uppercase" }}>
                {sec.items.length} traps · {sec.topic}
              </span>
            </div>
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
                      marginBottom: 10,
                    }}
                  >
                    <strong>{item.title}</strong>
                    {item.subtopic && (
                      <span className="muted" style={{ fontSize: 12 }}>
                        {item.subtopic}
                      </span>
                    )}
                  </div>

                  <div style={{ display: "grid", gap: 8 }}>
                    <div
                      style={{
                        borderLeft: "3px solid #ef4444",
                        paddingLeft: 12,
                        fontSize: 14,
                        lineHeight: 1.5,
                      }}
                    >
                      <div
                        style={{
                          fontSize: 11,
                          fontWeight: 700,
                          letterSpacing: "0.04em",
                          textTransform: "uppercase",
                          color: "#ef4444",
                          marginBottom: 2,
                        }}
                      >
                        Trap
                      </div>
                      {item.trap}
                    </div>
                    <div
                      style={{
                        borderLeft: "3px solid #10b981",
                        paddingLeft: 12,
                        fontSize: 14,
                        lineHeight: 1.5,
                      }}
                    >
                      <div
                        style={{
                          fontSize: 11,
                          fontWeight: 700,
                          letterSpacing: "0.04em",
                          textTransform: "uppercase",
                          color: "#059669",
                          marginBottom: 2,
                        }}
                      >
                        Correct
                      </div>
                      {item.correct}
                    </div>
                    <div
                      style={{
                        borderLeft: "3px solid #6366f1",
                        paddingLeft: 12,
                        fontSize: 14,
                        lineHeight: 1.5,
                      }}
                    >
                      <div
                        style={{
                          fontSize: 11,
                          fontWeight: 700,
                          letterSpacing: "0.04em",
                          textTransform: "uppercase",
                          color: "#4f46e5",
                          marginBottom: 2,
                        }}
                      >
                        Exam tip
                      </div>
                      {item.tip}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>
        ))}

        {sections.length === 0 && (
          <div className="panel muted" style={{ textAlign: "center" }}>
            No traps match that filter.
          </div>
        )}
      </div>

      <p className="muted" style={{ fontSize: 12, marginTop: 20 }}>
        Drawn from Tutorial Letters, workshop notes and recurring calculation side/sign errors. Use with
        the formula sheet while you drill each basket.
      </p>
    </div>
  );
}

export default function TrapsPage() {
  return (
    <Suspense fallback={<div className="muted" style={{ padding: 40 }}>Loading traps…</div>}>
      <TrapsContent />
    </Suspense>
  );
}
