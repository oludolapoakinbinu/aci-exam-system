"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api, AttemptResult } from "@/lib/api";
import { topicName } from "@/lib/topics";

export default function ReviewPage() {
  const params = useParams<{ id: string }>();
  const [result, setResult] = useState<AttemptResult | null>(null);
  const [filter, setFilter] = useState<"all" | "wrong">("all");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const id = Number(params.id);
    const cached = sessionStorage.getItem(`result:${id}`);
    if (cached) {
      setResult(JSON.parse(cached));
      return;
    }
    api
      .getAttempt(id)
      .then(setResult)
      .catch((e) => setError(e.message));
  }, [params.id]);

  if (error) return <div style={{ color: "var(--danger)", padding: 24 }}>{error}</div>;
  if (!result) return <div className="muted" style={{ padding: 24 }}>Loading review…</div>;

  const reviews = result.reviews.filter((r) => (filter === "wrong" ? r.correct === false : true));

  return (
    <div style={{ maxWidth: 820 }}>
      <div className="panel" style={{ marginBottom: 18 }}>
        <div style={{ display: "flex", justifyContent: "space-between", gap: 16, flexWrap: "wrap" }}>
          <div>
            <div className="muted" style={{ fontSize: 13 }}>
              Attempt #{result.attempt_id} · {result.mode}
            </div>
            <h1 style={{ margin: "4px 0" }}>
              {result.score}/{result.total} · {result.pct}% · {result.grade}
            </h1>
            <div style={{ fontWeight: 700, color: result.passed ? "var(--success)" : "var(--danger)" }}>
              {result.passed ? "Passed" : "Not passed"}
            </div>
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <Link href="/practice" className="btn btn-ghost">
              Practice
            </Link>
            <Link href="/exam" className="btn btn-primary">
              New mock
            </Link>
          </div>
        </div>

        {result.baskets.length > 0 && (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
              gap: 10,
              marginTop: 18,
            }}
          >
            {result.baskets.map((b) => (
              <div
                key={b.topic}
                style={{
                  border: "1px solid var(--line)",
                  borderRadius: 14,
                  padding: 12,
                  background: "var(--shell)",
                }}
              >
                <div style={{ fontSize: 13, fontWeight: 700 }}>{b.name}</div>
                <div style={{ fontSize: 18, fontWeight: 800, marginTop: 4 }}>
                  {b.correct}/{b.total}
                </div>
                <div className="muted" style={{ fontSize: 12 }}>
                  {b.pct}%
                  {result.mode === "exam"
                    ? b.passed
                      ? " · basket OK"
                      : ` · need ≥ ${b.min_required}`
                    : ""}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 14 }}>
        <button
          type="button"
          className={`btn ${filter === "all" ? "btn-primary" : "btn-ghost"}`}
          onClick={() => setFilter("all")}
        >
          All
        </button>
        <button
          type="button"
          className={`btn ${filter === "wrong" ? "btn-primary" : "btn-ghost"}`}
          onClick={() => setFilter("wrong")}
        >
          Incorrect only
        </button>
      </div>

      <div style={{ display: "grid", gap: 14 }}>
        {reviews.map((r, i) => (
          <article key={r.id} className="panel">
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
              <span className="chip">Q{i + 1}</span>
              <span className="chip">{topicName(r.topic)}</span>
              <span
                className="chip"
                style={{
                  color: r.correct ? "var(--success)" : "var(--danger)",
                  borderColor: r.correct ? "#bbf7d0" : "#fecaca",
                }}
              >
                {r.correct ? "Correct" : r.selected == null ? "Blank" : "Incorrect"}
              </span>
            </div>
            <div className="question-text" style={{ marginBottom: 12 }}>
              {r.question}
            </div>
            <div className="options" style={{ marginBottom: 12 }}>
              {r.options.map((opt, oi) => {
                let cls = "option-row";
                if (oi === r.answer) cls += " correct";
                else if (oi === r.selected && !r.correct) cls += " wrong";
                return (
                  <div key={oi} className={cls}>
                    <span>
                      <strong style={{ marginRight: 8 }}>{String.fromCharCode(65 + oi)}.</strong>
                      {opt}
                      {oi === r.answer ? " ✓" : ""}
                      {oi === r.selected && oi !== r.answer ? " (yours)" : ""}
                    </span>
                  </div>
                );
              })}
            </div>
            <div className="explain-box">
              <div
                style={{
                  fontWeight: 800,
                  color: "var(--purple)",
                  marginBottom: 8,
                  fontSize: 12,
                  letterSpacing: "0.04em",
                }}
              >
                DETAILED EXPLANATION
              </div>
              <div
                style={{
                  whiteSpace: "pre-wrap",
                  lineHeight: 1.6,
                  fontSize: 14,
                  fontFamily: "var(--font-geist-mono), ui-monospace, monospace",
                }}
              >
                {r.explanation}
              </div>
              {r.source && (
                <div className="muted" style={{ marginTop: 10, fontSize: 12 }}>
                  Source: {r.source}
                </div>
              )}
              <div style={{ marginTop: 10 }}>
                <Link href="/formulas" className="chip active">
                  Open formula sheet →
                </Link>
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
