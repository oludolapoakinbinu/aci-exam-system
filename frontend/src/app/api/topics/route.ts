import { NextResponse } from "next/server";
import { topicStats } from "@/lib/quiz-engine";

export async function GET() {
  return NextResponse.json(topicStats());
}
