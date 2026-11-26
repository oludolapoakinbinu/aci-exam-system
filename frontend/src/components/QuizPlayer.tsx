"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { AttemptStart, QuestionPublic, api } from "@/lib/api";

type AnswerState = {
  selected: number | null;
  flagged: boolean;
  time_spent_sec: number;
};

function formatClock(totalSec: number) {
  const s = Math.max(0, Math.floor(totalSec));
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${String(m).padStart(2, "0")}:${String(r).padStart(2, "0")}`;
}

export function QuizPlayer({ attempt }: { attempt: AttemptStart }) {
  const router = useRouter();
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<string, AnswerState>>(() => {
    const init: Record<string, AnswerState> = {};
    for (const q of attempt.questions) {
      init[q.id] = { selected: null, flagged: false, time_spent_sec: 0 };
    }
    return init;
  });
  // Always show a live clock: countdown if timed, else elapsed
  const timed = attempt.time_limit_sec != null && attempt.time_limit_sec > 0;
  const [clock, setClock] = useState(() =>
    timed ? attempt.time_limit_sec! : 0
  );
  const [submitting, setSubmitting] = useState(false);
  const [reviewOpen, setReviewOpen] = useState(false);
  const qStartedAt = useRef(Date.now());
  const submitted = useRef(false);
  const answersRef = useRef(answers);
  answersRef.current = answers;

  const q: QuestionPublic = attempt.questions[idx];
  const answered = useMemo(
    () => Object.values(answers).filter((a) => a.selected !== null).length,
    [answers]
  );
  const progress = Math.round((answered / Math.max(1, attempt.total)) * 100);

  useEffect(() => {
    const id = window.setInterval(() => {
      setClock((c) => {
        if (timed) {
          const next = c - 1;
          return next;
        }
        return c + 1;
      });
    }, 1000);
    return () => window.clearInterval(id);
  }, [timed]);

  useEffect(() => {
    if (!timed) return;
    if (clock <= 0 && !submitted.current) {
      void finish();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [clock, timed]);

  function bumpTime() {
    const spent = Math.max(0, Math.round((Date.now() - qStartedAt.current) / 1000));
    setAnswers((prev) => ({
      ...prev,
      [q.id]: { ...prev[q.id], time_spent_sec: prev[q.id].time_spent_sec + spent },
    }));
    qStartedAt.current = Date.now();
  }

  function go(to: number) {
    if (to < 0 || to >= attempt.total) return;
    bumpTime();
    setIdx(to);
  }

  function select(i: number) {
    setAnswers((prev) => ({
      ...prev,
      [q.id]: { ...prev[q.id], selected: i },
    }));
  }

  function toggleFlag() {
    setAnswers((prev) => ({
      ...prev,
      [q.id]: { ...prev[q.id], flagged: !prev[q.id].flagged },
    }));
  }

  async function finish() {
    if (submitted.current || submitting) return;
    submitted.current = true;
    setSubmitting(true);
    bumpTime();
    try {
      const current = answersRef.current;
      const lastSpent = Math.max(0, Math.round((Date.now() - qStartedAt.current) / 1000));
      const payload = attempt.questions.map((qq) => ({
        question_id: qq.id,
        selected: current[qq.id]?.selected ?? null,
        flagged: current[qq.id]?.flagged ?? false,
        time_spent_sec:
          (current[qq.id]?.time_spent_sec ?? 0) + (qq.id === q.id ? lastSpent : 0),
      }));
      const result = await api.submitAttempt(attempt.attempt_id, payload, {
        mode: attempt.mode,
        started_at: attempt.started_at,
      });
      const { saveResult } = await import("@/lib/local-store");
      saveResult(result as unknown as import("@/lib/local-store").StoredResult);
      sessionStorage.setItem(`result:${attempt.attempt_id}`, JSON.stringify(result));
      router.push(`/review/${attempt.attempt_id}`);
    } catch (e) {
      submitted.current = false;
      setSubmitting(false);
      alert(e instanceof Error ? e.message : "Submit failed");
    }
  }

  const timerLabel = timed
    ? `${formatClock(clock)} Min Time Left`
    : `${formatClock(clock)} Elapsed`;

  const modeTitle =
    attempt.mode === "exam"
      ? "ACI Mock Exam"
      : attempt.mode === "weak"
        ? "Weak Area Drill"
        : "ACI Practice";

  const selected = answers[q.id]?.selected ?? null;

  return (
    <div className="quiz-wrap">
      <div className="quiz-card">
        <div className="quiz-top">
          <div className="quiz-title">
            <h1>{modeTitle}</h1>
            <p>
              Session {attempt.attempt_id} · Question {idx + 1} of {attempt.total}
            </p>
          </div>

          <div className="quiz-progress">
            <div className="track">
              <span style={{ width: `${progress}%` }} />
            </div>
            <div className="pct">{progress}%</div>
            <div className="review-actions">
              <button type="button" className="chip" onClick={() => setReviewOpen((v) => !v)}>
                review
              </button>
              <button
                type="button"
                className={`chip mark ${answers[q.id]?.flagged ? "active" : ""}`}
                onClick={toggleFlag}
              >
                {answers[q.id]?.flagged ? "Marked" : "Mark as review"}
              </button>
            </div>
          </div>

          <div className="timer-box" style={{ color: timed && clock < 60 ? "#ef4444" : undefined }}>
            <span aria-hidden>⏱</span>
            {timerLabel}
          </div>
        </div>

        {reviewOpen && (
          <div className="quiz-nav-grid">
            {attempt.questions.map((qq, i) => {
              const a = answers[qq.id];
              const state =
                i === idx ? "current" : a.selected != null ? "done" : a.flagged ? "flag" : "";
              return (
                <button
                  key={qq.id}
                  type="button"
                  className={`quiz-nav-btn ${state}`}
                  onClick={() => {
                    setReviewOpen(false);
                    go(i);
                  }}
                >
                  {i + 1}
                </button>
              );
            })}
          </div>
        )}

        <div className="question-label">Question {idx + 1}</div>
        <div className="question-text">{q.question}</div>

        <div className="options" role="radiogroup" aria-label="Answer choices">
          {q.options.map((opt, i) => {
            const isSelected = selected === i;
            return (
              <button
                key={`${q.id}-${i}`}
                type="button"
                role="radio"
                aria-checked={isSelected}
                className={`option-row ${isSelected ? "selected" : ""}`}
                onClick={() => select(i)}
              >
                <span className="option-text">
                  <strong>{String.fromCharCode(65 + i)}.</strong> {opt}
                </span>
                <span className={`radio ${isSelected ? "on" : ""}`} aria-hidden />
              </button>
            );
          })}
        </div>

        <div className="quiz-footer">
          <div />
          <div className="nav-pair">
            <button
              type="button"
              className="btn btn-ghost"
              disabled={idx === 0}
              onClick={() => go(idx - 1)}
            >
              ← Previous
            </button>
            <button
              type="button"
              className="btn btn-ghost"
              disabled={idx >= attempt.total - 1}
              onClick={() => go(idx + 1)}
            >
              Next →
            </button>
          </div>
          <div className="finish-slot">
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => void finish()}
              disabled={submitting}
            >
              {submitting ? "Submitting…" : "Finish"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
