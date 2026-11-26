import { NextResponse } from "next/server";
import { gradeAttempt } from "@/lib/quiz-engine";

export async function POST(
  req: Request,
  ctx: { params: Promise<{ id: string }> }
) {
  const { id } = await ctx.params;
  const body = await req.json();
  const mode = body.mode || "practice";
  const result = gradeAttempt({
    mode,
    attempt_id: Number(id),
    answers: body.answers || [],
    started_at: body.started_at,
  });
  return NextResponse.json(result);
}
