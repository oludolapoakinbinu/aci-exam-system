"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, Stats, Topic } from "@/lib/api";

function TopicCard({
  title,
  pct,
  href,
  highlight,
  meta,
}: {
  title: string;
  pct: number;
  href: string;
  highlight?: boolean;
  meta?: string;
}) {
  return (
    <div className="topic-card">
      <div className="pct">{pct}% Completed</div>
      <div className="progress-thin">
        <span style={{ width: `${pct}%` }} />
      </div>
      <div className="topic-icon" aria-hidden>
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
          <rect x="5" y="3" width="14" height="18" rx="2" stroke="currentColor" strokeWidth="1.8" />
          <path d="M8 8h8M8 12h8M8 16h5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      </div>
      <h3>{title}</h3>
      {meta && (
        <div className="muted" style={{ textAlign: "center", fontSize: 12, marginTop: -8, marginBottom: 10 }}>
          {meta}
        </div>
      )}
      <div style={{ marginTop: "auto" }}>
        <Link href={href} className={`btn ${highlight ? "btn-cyan" : "btn-ghost"}`} style={{ width: "100%" }}>
          Take Test
        </Link>
      </div>
    </div>
  );
}

export default function HomePage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.stats(), api.topics()])
      .then(async ([s, t]) => {
        const { mergeStats } = await import("@/lib/local-store");
        setStats(mergeStats(s) as typeof s);
        // overlay mastery from local results
        const merged = mergeStats(s) as typeof s;
        const by = Object.fromEntries(merged.by_topic.map((x) => [x.topic, x.accuracy]));
        setTopics(
          t.map((topic) => ({
            ...topic,
            mastery: by[topic.code] ?? topic.mastery,
          }))
        );
      })
      .catch((e) => setError(e.message || "Failed to load"));
  }, []);

  if (error) {
    return (
      <div className="panel" style={{ marginTop: 24, textAlign: "center" }}>
        <h1 style={{ marginTop: 0 }}>API not reachable</h1>
        <p className="muted">{error}</p>
        <p className="muted" style={{ fontSize: 14 }}>
          From <code>backend/</code> run{" "}
          <code>../.venv/bin/uvicorn app.main:app --reload --port 8000</code>
        </p>
      </div>
    );
  }

  if (!stats) {
    return <div className="muted" style={{ padding: 40, textAlign: "center" }}>Loading dashboard…</div>;
  }

  return (
    <>
      <div className="stat-strip">
        <div className="stat-pill">
          <div className="label">Questions</div>
          <div className="value">{stats.total_questions}</div>
        </div>
        <div className="stat-pill">
          <div className="label">Flashcards</div>
          <div className="value">{stats.total_flashcards}</div>
        </div>
        <div className="stat-pill">
          <div className="label">Accuracy</div>
          <div className="value">{stats.overall_accuracy}%</div>
        </div>
        <div className="stat-pill">
          <div className="label">Streak</div>
          <div className="value">{stats.streak_days}d</div>
        </div>
      </div>

      <div className="section-head">
        <h2>Mock Tests</h2>
        <Link href="/exam" className="muted" style={{ fontWeight: 600 }}>
          View More →
        </Link>
      </div>
      <div className="card-row">
        <TopicCard
          title="Full Mock Exam"
          pct={stats.exams_passed > 0 ? 100 : 0}
          href="/exam"
          highlight
          meta="70 Qs · 2 hours · baskets"
        />
        {topics.slice(0, 3).map((t, i) => (
          <TopicCard
            key={t.code}
            title={t.name}
            pct={Math.round(t.mastery)}
            href={`/practice?topic=${t.code}`}
            highlight={i === 0}
            meta={`${t.exam_count} on exam · ${t.question_count} in bank`}
          />
        ))}
      </div>

      <div className="section-head">
        <h2>Practice Questions</h2>
        <Link href="/practice" className="muted" style={{ fontWeight: 600 }}>
          View More →
        </Link>
      </div>
      <div className="card-row">
        {topics.map((t, i) => (
          <TopicCard
            key={t.code}
            title={t.name}
            pct={Math.round(t.mastery)}
            href={`/practice?topic=${t.code}`}
            highlight={i === 1}
            meta={`${t.question_count} questions · ${t.flashcard_count} cards`}
          />
        ))}
      </div>

      {topics.length === 5 && (
        <div className="card-row" style={{ marginTop: 16, gridTemplateColumns: "repeat(2, 1fr)" }}>
          <TopicCard
            title="Weak Areas"
            pct={stats.weak_subtopics.length ? 15 : 0}
            href="/practice?mode=weak"
            meta="Spaced review of low-accuracy topics"
          />
          <TopicCard
            title="Flashcards"
            pct={0}
            href="/flashcards"
            highlight
            meta={`${stats.total_flashcards} cards · Leitner boxes`}
          />
        </div>
      )}

      {stats.recent.length > 0 && (
        <>
          <div className="section-head">
            <h2>Recent attempts</h2>
            <Link href="/history" className="muted" style={{ fontWeight: 600 }}>
              History →
            </Link>
          </div>
          <div className="panel">
            {stats.recent.slice(0, 5).map((a) => (
              <div
                key={a.id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  padding: "10px 0",
                  borderBottom: "1px solid var(--line)",
                }}
              >
                <Link href={a.finished_at ? `/review/${a.id}` : "#"} style={{ fontWeight: 600 }}>
                  #{a.id} · {a.mode}
                  {a.grade ? ` · ${a.grade}` : ""}
                </Link>
                <span className="muted">
                  {a.score != null ? `${a.score}/${a.total} (${a.pct}%)` : "in progress"}
                </span>
              </div>
            ))}
          </div>
        </>
      )}
    </>
  );
}
