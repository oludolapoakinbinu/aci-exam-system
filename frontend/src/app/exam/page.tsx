"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";
import { TOPIC_META } from "@/lib/topics";

const BASKETS: Record<string, [number, number]> = {
  fme: [10, 5],
  fx: [18, 9],
  rates: [18, 9],
  ficc: [14, 7],
  fma: [10, 5],
};

export default function ExamPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function start() {
    setLoading(true);
    setError(null);
    try {
      const attempt = await api.startAttempt({ mode: "exam", timed: true });
      sessionStorage.setItem(`attempt:${attempt.attempt_id}`, JSON.stringify(attempt));
      router.push(`/quiz/${attempt.attempt_id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed");
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 720 }}>
      <h1 style={{ margin: "8px 0 6px", fontSize: "1.8rem" }}>Mock Exams</h1>
      <p className="muted" style={{ marginTop: 0, marginBottom: 20 }}>
        Official ACI Dealing Certificate format: 70 questions, 120 minutes, 60% overall pass with
        50% minimum in every topic basket.
      </p>

      <div className="card-row" style={{ marginBottom: 20, gridTemplateColumns: "1fr" }}>
        <div className="topic-card" style={{ minHeight: 0, flexDirection: "row", alignItems: "center", gap: 20 }}>
          <div className="topic-icon" style={{ margin: 0 }}>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
              <rect x="5" y="3" width="14" height="18" rx="2" stroke="currentColor" strokeWidth="1.8" />
              <path d="M8 8h8M8 12h8M8 16h5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
            </svg>
          </div>
          <div style={{ flex: 1 }}>
            <h3 style={{ margin: 0, textAlign: "left" }}>Full Mock Exam</h3>
            <div className="muted" style={{ fontSize: 13 }}>
              70 Qs · Pass / Merit / Distinction · Calculator allowed
            </div>
          </div>
          <button type="button" className="btn btn-cyan" disabled={loading} onClick={() => void start()}>
            {loading ? "Building…" : "Take Test"}
          </button>
        </div>
      </div>

      <div className="panel">
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <thead>
            <tr className="muted" style={{ textAlign: "left" }}>
              <th style={{ padding: "10px 8px" }}>Topic basket</th>
              <th style={{ padding: "10px 8px" }}>Questions</th>
              <th style={{ padding: "10px 8px" }}>Min correct</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(TOPIC_META).map(([code, meta]) => {
              const [n, m] = BASKETS[code];
              return (
                <tr key={code} style={{ borderTop: "1px solid var(--line)" }}>
                  <td style={{ padding: "12px 8px", fontWeight: 650 }}>{meta.name}</td>
                  <td style={{ padding: "12px 8px" }}>{n}</td>
                  <td style={{ padding: "12px 8px" }}>{m} (50%)</td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <p className="muted" style={{ fontSize: 13, marginBottom: 0, marginTop: 12 }}>
          Grades: Pass 60–69.99% · Merit 70–79.99% · Distinction 80%+
        </p>
      </div>

      {error && <p style={{ color: "var(--danger)" }}>{error}</p>}
    </div>
  );
}
