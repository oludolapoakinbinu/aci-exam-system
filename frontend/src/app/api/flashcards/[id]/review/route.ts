import { NextResponse } from "next/server";

export async function POST() {
  // Flash progress is stored client-side on Netlify.
  return NextResponse.json({ ok: true, box: 1, due_at: null });
}
