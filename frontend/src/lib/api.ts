const BASE = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") || "";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json() as Promise<T>;
}

export type Topic = {
  code: string;
  name: string;
  exam_count: number;
  min_pass: number;
  color: string;
  question_count: number;
  flashcard_count: number;
  mastery: number;
};

export type QuestionPublic = {
  id: string;
  topic: string;
  subtopic: string;
  kind: string;
  difficulty: string;
  question: string;
  options: string[];
  source?: string;
};

export type QuestionReview = QuestionPublic & {
  answer: number;
  explanation: string;
  selected: number | null;
  correct: boolean | null;
  key_corrected?: boolean;
  correction_note?: string | null;
};

export type AttemptStart = {
  attempt_id: number;
  mode: string;
  time_limit_sec: number | null;
  total: number;
  questions: QuestionPublic[];
  started_at?: string;
};

export type AttemptResult = {
  attempt_id: number;
  mode: string;
  score: number;
  total: number;
  pct: number;
  grade: string;
  passed: boolean;
  baskets: {
    topic: string;
    name: string;
    correct: number;
    total: number;
    pct: number;
    min_required: number;
    passed: boolean;
  }[];
  started_at: string;
  finished_at: string;
  reviews: QuestionReview[];
};

export type Stats = {
  total_questions: number;
  total_flashcards: number;
  attempts: number;
  exams_passed: number;
  overall_accuracy: number;
  by_topic: {
    topic: string;
    name: string;
    color: string;
    questions: number;
    accuracy: number;
    seen: number;
  }[];
  weak_subtopics: {
    topic: string;
    subtopic: string;
    accuracy: number;
    seen: number;
  }[];
  recent: {
    id: number;
    mode: string;
    score: number | null;
    total: number;
    grade: string | null;
    passed: boolean | null;
    started_at: string;
    finished_at: string | null;
    pct: number | null;
  }[];
  due_review: number;
  streak_days: number;
};

export type Flashcard = {
  id: string;
  topic: string;
  subtopic: string;
  front: string;
  back: string | null;
  box: number;
};

export const api = {
  topics: () => req<Topic[]>("/api/topics"),
  stats: () => req<Stats>("/api/stats"),
  startAttempt: (body: Record<string, unknown>) =>
    req<AttemptStart>("/api/attempts", { method: "POST", body: JSON.stringify(body) }),
  submitAttempt: (
    id: number,
    answers: unknown[],
    extra?: { mode?: string; started_at?: string }
  ) =>
    req<AttemptResult>(`/api/attempts/${id}/submit`, {
      method: "POST",
      body: JSON.stringify({ answers, ...extra }),
    }),
  getAttempt: async (id: number) => {
    const { getResult } = await import("./local-store");
    const local = getResult(id);
    if (local) return local as unknown as AttemptResult;
    return req<AttemptResult>(`/api/attempts/${id}`);
  },
  listAttempts: async () => {
    const { listResults } = await import("./local-store");
    return listResults().map((r) => ({
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
  },
  flashcards: (params: { topic?: string; due?: boolean; limit?: number; reveal?: boolean } = {}) => {
    const q = new URLSearchParams();
    if (params.topic) q.set("topic", params.topic);
    if (params.due) q.set("due", "true");
    if (params.limit) q.set("limit", String(params.limit));
    if (params.reveal) q.set("reveal", "true");
    return req<Flashcard[]>(`/api/flashcards?${q}`);
  },
  getFlashcard: (id: string) => req<Flashcard>(`/api/flashcards/${id}`),
  reviewFlashcard: (id: string, remembered: boolean) =>
    req<{ ok: boolean; box: number }>(`/api/flashcards/${id}/review`, {
      method: "POST",
      body: JSON.stringify({ remembered }),
    }),
  search: (q: string) =>
    req<{ questions: QuestionPublic[]; flashcards: Flashcard[] }>(
      `/api/search?q=${encodeURIComponent(q)}`
    ),
  reload: () => req<Record<string, number>>("/api/admin/reload", { method: "POST" }),
};
