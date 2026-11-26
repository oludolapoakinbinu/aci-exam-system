"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";
import { api } from "@/lib/api";
import { TOPIC_META } from "@/lib/topics";

function PracticeForm() {
  const router = useRouter();
  const params = useSearchParams();
  const initialTopic = params.get("topic");
  const initialMode = params.get("mode") || "practice";

  const [mode, setMode] = useState(initialMode === "weak" ? "weak" : initialMode === "quick" ? "quick" : "practice");
  const [topics, setTopics] = useState<string[]>(initialTopic ? [initialTopic] : []);
  const [count, setCount] = useState(20);
  const [kind, setKind] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [timed, setTimed] = useState(true);
  const [excludeSeen, setExcludeSeen] = useState(false);
  const [onlyOriginal, setOnlyOriginal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function toggleTopic(code: string) {
    setTopics((prev) => (prev.includes(code) ? prev.filter((x) => x !== code) : [...prev, code]));
  }

  async function start() {
    setLoading(true);
    setError(null);
    try {
      const attempt = await api.startAttempt({
        mode: mode === "quick" ? "quick" : mode,
        topics: topics.length ? topics : null,
        kinds: kind ? [kind] : null,
        difficulties: difficulty ? [difficulty] : null,
        count: mode === "quick" ? 10 : count,
        timed,
        exclude_seen: excludeSeen,
        only_original: onlyOriginal ? true : null,
      });
      sessionStorage.setItem(`attempt:${attempt.attempt_id}`, JSON.stringify(attempt));
      router.push(`/quiz/${attempt.attempt_id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to start");
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 640 }}>
      <h1 style={{ margin: "8px 0 6px", fontSize: "1.8rem" }}>Practice Questions</h1>
      <p className="muted" style={{ marginTop: 0, marginBottom: 20 }}>
        Build a custom drill. Every answer gets an explanation after you finish.
      </p>

      <div className="panel" style={{ display: "grid", gap: 18 }}>
        <div>
          <div style={{ fontWeight: 700, marginBottom: 8 }}>Mode</div>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {[
              ["practice", "Practice"],
              ["quick", "Quick 10"],
              ["weak", "Weak areas"],
            ].map(([v, label]) => (
              <button
                key={v}
                type="button"
                className={`btn ${mode === v ? "btn-primary" : "btn-ghost"}`}
                onClick={() => setMode(v)}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <div style={{ fontWeight: 700, marginBottom: 8 }}>Topics</div>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {Object.entries(TOPIC_META).map(([code, meta]) => (
              <button
                key={code}
                type="button"
                className={`chip ${topics.includes(code) ? "active" : ""}`}
                onClick={() => toggleTopic(code)}
              >
                {meta.short}
              </button>
            ))}
          </div>
        </div>

        {mode !== "quick" && (
          <label style={{ display: "grid", gap: 6, fontWeight: 600 }}>
            Number of questions
            <input
              type="number"
              min={5}
              max={70}
              value={count}
              onChange={(e) => setCount(Number(e.target.value))}
              style={{
                border: "1px solid var(--line)",
                borderRadius: 12,
                padding: "10px 12px",
                fontWeight: 500,
              }}
            />
          </label>
        )}

        <div style={{ display: "grid", gap: 12, gridTemplateColumns: "1fr 1fr" }}>
          <label style={{ display: "grid", gap: 6, fontWeight: 600 }}>
            Kind
            <select
              value={kind}
              onChange={(e) => setKind(e.target.value)}
              style={{ border: "1px solid var(--line)", borderRadius: 12, padding: "10px 12px" }}
            >
              <option value="">Any</option>
              <option value="theory">Theory</option>
              <option value="calculation">Calculation</option>
            </select>
          </label>
          <label style={{ display: "grid", gap: 6, fontWeight: 600 }}>
            Difficulty
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              style={{ border: "1px solid var(--line)", borderRadius: 12, padding: "10px 12px" }}
            >
              <option value="">Any</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </label>
        </div>

        <div style={{ display: "grid", gap: 8, fontSize: 14 }}>
          <label>
            <input type="checkbox" checked={timed} onChange={(e) => setTimed(e.target.checked)} /> Timed
          </label>
          <label>
            <input
              type="checkbox"
              checked={excludeSeen}
              onChange={(e) => setExcludeSeen(e.target.checked)}
            />{" "}
            Prefer unseen
          </label>
          <label>
            <input
              type="checkbox"
              checked={onlyOriginal}
              onChange={(e) => setOnlyOriginal(e.target.checked)}
            />{" "}
            Original questions only
          </label>
        </div>

        {error && <p style={{ color: "var(--danger)", margin: 0 }}>{error}</p>}

        <button type="button" className="btn btn-cyan" disabled={loading} onClick={() => void start()}>
          {loading ? "Preparing…" : "Take Test"}
        </button>
      </div>
    </div>
  );
}

export default function PracticePage() {
  return (
    <Suspense fallback={<div className="muted">Loading…</div>}>
      <PracticeForm />
    </Suspense>
  );
}
