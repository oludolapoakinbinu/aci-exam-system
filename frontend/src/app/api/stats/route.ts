import { NextResponse } from "next/server";
import { bankStats } from "@/lib/quiz-engine";

export async function GET() {
  return NextResponse.json(bankStats());
}
