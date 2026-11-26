import {
  BankQuestion,
  FLASHCARDS,
  QUESTIONS,
  TOPIC_META,
  getQuestion,
} from "./bank";

export function publicQuestion(q: BankQuestion) {
  return {
    id: q.id,
    topic: q.topic,
    subtopic: q.subtopic,
    kind: q.kind,
    difficulty: q.difficulty,
    question: q.question,
    options: q.options,
    source: q.source,
  };
}

export function pickExamSet(): BankQuestion[] {
  const chosen: BankQuestion[] = [];
  for (const [code, meta] of Object.entries(TOPIC_META)) {
    const pool = QUESTIONS.filter((q) => q.topic === code);
    if (pool.length <= meta.exam_count) chosen.push(...pool);
    else chosen.push(...shuffle(pool).slice(0, meta.exam_count));
  }
  if (chosen.length < 70) {
    const ids = new Set(chosen.map((q) => q.id));
    const extra = QUESTIONS.filter((q) => !ids.has(q.id));
    chosen.push(...shuffle(extra).slice(0, 70 - chosen.length));
  }
  return shuffle(chosen).slice(0, 70);
}

export function pickQuestions(opts: {
  mode: string;
  topics?: string[] | null;
  kinds?: string[] | null;
  difficulties?: string[] | null;
  count?: number | null;
  only_original?: boolean | null;
}): BankQuestion[] {
  if (opts.mode === "exam") return pickExamSet();

  let pool = QUESTIONS.slice();
  if (opts.topics?.length) pool = pool.filter((q) => opts.topics!.includes(q.topic));
  if (opts.kinds?.length) pool = pool.filter((q) => opts.kinds!.includes(q.kind));
  if (opts.difficulties?.length)
    pool = pool.filter((q) => opts.difficulties!.includes(q.difficulty));
  if (opts.only_original === true) {
    pool = pool.filter(
      (q) => q.is_original || (q.source || "").startsWith("Original")
    );
  }

  const n =
    opts.mode === "quick" ? opts.count || 10 : opts.count || 20;
  return shuffle(pool).slice(0, Math.min(n, pool.length));
}

export function gradeAttempt(input: {
  mode: string;
  attempt_id: number | string;
  answers: {
    question_id: string;
    selected: number | null;
    flagged?: boolean;
    time_spent_sec?: number;
  }[];
  started_at?: string;
}) {
  const reviews = [];
  const basket: Record<string, { correct: number; total: number }> = {};
  let score = 0;

  for (const a of input.answers) {
    const q = getQuestion(a.question_id);
    if (!q) continue;
    const correct = a.selected !== null && a.selected === q.answer;
    if (correct) score += 1;
    if (!basket[q.topic]) basket[q.topic] = { correct: 0, total: 0 };
    basket[q.topic].total += 1;
    if (correct) basket[q.topic].correct += 1;
    reviews.push({
      ...publicQuestion(q),
      answer: q.answer,
      explanation: q.explanation,
      selected: a.selected,
      correct,
      key_corrected: !!q.key_corrected,
      correction_note: q.correction_note || null,
    });
  }

  const total = input.answers.length;
  const pct = total ? Math.round((score / total) * 1000) / 10 : 0;
  const baskets = Object.entries(TOPIC_META).map(([code, meta]) => {
    const b = basket[code] || { correct: 0, total: 0 };
    const min_required = input.mode === "exam" ? meta.min_pass : 0;
    const passed =
      input.mode === "exam"
        ? b.total === 0 || b.correct >= min_required
        : b.total === 0 || b.correct / b.total >= 0.5;
    return {
      topic: code,
      name: meta.name,
      correct: b.correct,
      total: b.total,
      pct: b.total ? Math.round((b.correct / b.total) * 1000) / 10 : 0,
      min_required,
      passed,
    };
  }).filter((b) => input.mode === "exam" || b.total > 0);

  const allBasketsOk =
    input.mode !== "exam" || baskets.every((b) => b.total === 0 || b.passed);
  const passed =
    input.mode === "exam" ? score >= 42 && allBasketsOk : pct >= 60;
  const grade =
    pct >= 80 ? "Distinction" : pct >= 70 ? "Merit" : pct >= 60 ? "Pass" : "Fail";

  return {
    attempt_id: input.attempt_id,
    mode: input.mode,
    score,
    total,
    pct,
    grade,
    passed,
    baskets,
    started_at: input.started_at || new Date().toISOString(),
    finished_at: new Date().toISOString(),
    reviews,
  };
}

export function topicStats() {
  return Object.values(TOPIC_META).map((meta) => {
    const qs = QUESTIONS.filter((q) => q.topic === meta.code);
    const fc = FLASHCARDS.filter((f) => f.topic === meta.code);
    return {
      ...meta,
      question_count: qs.length,
      flashcard_count: fc.length,
      mastery: 0,
    };
  });
}

export function bankStats() {
  return {
    total_questions: QUESTIONS.length,
    total_flashcards: FLASHCARDS.length,
    attempts: 0,
    exams_passed: 0,
    overall_accuracy: 0,
    by_topic: Object.values(TOPIC_META).map((meta) => ({
      topic: meta.code,
      name: meta.name,
      color: meta.color,
      questions: QUESTIONS.filter((q) => q.topic === meta.code).length,
      accuracy: 0,
      seen: 0,
    })),
    weak_subtopics: [] as { topic: string; subtopic: string; accuracy: number; seen: number }[],
    recent: [] as unknown[],
    due_review: 0,
    streak_days: 0,
  };
}

function shuffle<T>(arr: T[]): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
