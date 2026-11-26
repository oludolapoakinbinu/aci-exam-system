"use client";

const RESULTS_KEY = "aci:results";
const PROGRESS_KEY = "aci:progress";
const FLASH_KEY = "aci:flash";

export type StoredResult = {
  attempt_id: number;
  mode: string;
  score: number;
  total: number;
  pct: number;
  grade: string;
  passed: boolean;
  baskets: unknown[];
  started_at: string;
  finished_at: string;
  reviews: unknown[];
};

function read<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function write(key: string, value: unknown) {
  if (typeof window === "undefined") return;
  localStorage.setItem(key, JSON.stringify(value));
}

export function saveResult(result: StoredResult) {
  const all = read<StoredResult[]>(RESULTS_KEY, []);
  const next = [result, ...all.filter((r) => r.attempt_id !== result.attempt_id)].slice(0, 50);
  write(RESULTS_KEY, next);

  const progress = read<Record<string, { seen: number; correct: number }>>(PROGRESS_KEY, {});
  for (const r of result.reviews as { id: string; correct: boolean | null }[]) {
    if (!progress[r.id]) progress[r.id] = { seen: 0, correct: 0 };
    progress[r.id].seen += 1;
    if (r.correct) progress[r.id].correct += 1;
  }
  write(PROGRESS_KEY, progress);
}

export function getResult(id: number) {
  return read<StoredResult[]>(RESULTS_KEY, []).find((r) => r.attempt_id === id) || null;
}

export function listResults() {
  return read<StoredResult[]>(RESULTS_KEY, []);
}

export function getProgress() {
  return read<Record<string, { seen: number; correct: number }>>(PROGRESS_KEY, {});
}

export function mergeStats<T extends Record<string, unknown>>(base: T): T {
  const results = listResults();
  const progress = getProgress();
  const seen = Object.values(progress).reduce((s, p) => s + p.seen, 0);
  const correct = Object.values(progress).reduce((s, p) => s + p.correct, 0);
  const exams_passed = results.filter((r) => r.mode === "exam" && r.passed).length;

  const by_topic = (base.by_topic as { topic: string; questions: number; color: string; name: string }[]).map(
    (t) => {
      let tSeen = 0;
      let tOk = 0;
      for (const [qid, p] of Object.entries(progress)) {
        // topic prefix heuristic from id is weak; skip detailed — keep 0 unless we store topic
        void qid;
        void p;
      }
      return { ...t, accuracy: 0, seen: tSeen };
    }
  );

  // Compute by_topic from reviews in results
  const topicAcc: Record<string, { ok: number; seen: number }> = {};
  for (const res of results) {
    for (const rev of res.reviews as { topic: string; correct: boolean | null }[]) {
      if (!topicAcc[rev.topic]) topicAcc[rev.topic] = { ok: 0, seen: 0 };
      topicAcc[rev.topic].seen += 1;
      if (rev.correct) topicAcc[rev.topic].ok += 1;
    }
  }
  const byTopicMerged = (base.by_topic as { topic: string; name: string; color: string; questions: number }[]).map(
    (t) => {
      const a = topicAcc[t.topic];
      return {
        ...t,
        seen: a?.seen || 0,
        accuracy: a && a.seen ? Math.round((a.ok / a.seen) * 1000) / 10 : 0,
      };
    }
  );

  const recent = results.slice(0, 10).map((r) => ({
    id: r.attempt_id,
    mode: r.mode,
    score: r.score,
    total: r.total,
    grade: r.grade,
    passed: r.passed,
    started_at: r.started_at,
    finished_at: r.finished_at,
    pct: r.pct,
  }));

  // streak
  const days = new Set(
    results.filter((r) => r.finished_at).map((r) => r.finished_at.slice(0, 10))
  );
  let streak = 0;
  const d = new Date();
  while (days.has(d.toISOString().slice(0, 10))) {
    streak += 1;
    d.setDate(d.getDate() - 1);
  }

  return {
    ...base,
    attempts: results.length,
    exams_passed,
    overall_accuracy: seen ? Math.round((correct / seen) * 1000) / 10 : 0,
    by_topic: byTopicMerged,
    recent,
    streak_days: streak,
  };
}

export function saveFlashReview(id: string, remembered: boolean) {
  const map = read<Record<string, { box: number; times: number }>>(FLASH_KEY, {});
  const cur = map[id] || { box: 1, times: 0 };
  cur.times += 1;
  cur.box = remembered ? Math.min(5, cur.box + 1) : 1;
  map[id] = cur;
  write(FLASH_KEY, map);
  return cur;
}
