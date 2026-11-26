import { NextResponse } from "next/server";
import { pickQuestions, publicQuestion } from "@/lib/quiz-engine";

export async function GET() {
  // History is client-local on Netlify; return empty list for API compatibility.
  return NextResponse.json([]);
}

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}));
  const mode = body.mode || "practice";
  const questions = pickQuestions({
    mode,
    topics: body.topics,
    kinds: body.kinds,
    difficulties: body.difficulties,
    count: body.count,
    only_original: body.only_original,
  });

  if (!questions.length) {
    return NextResponse.json(
      { detail: "No questions match those filters." },
      { status: 404 }
    );
  }

  const attempt_id = Date.now() % 1_000_000_000;
  const timed = mode === "exam" || !!body.timed;
  const time_limit_sec = timed
    ? mode === "exam"
      ? 120 * 60
      : (body.count || questions.length) * 90
    : null;

  return NextResponse.json({
    attempt_id,
    mode,
    time_limit_sec,
    total: questions.length,
    questions: questions.map(publicQuestion),
    started_at: new Date().toISOString(),
  });
}
