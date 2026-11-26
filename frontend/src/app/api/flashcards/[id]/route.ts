import { NextResponse } from "next/server";
import { FLASHCARDS } from "@/lib/bank";

export async function GET(
  _req: Request,
  ctx: { params: Promise<{ id: string }> }
) {
  const { id } = await ctx.params;
  const c = FLASHCARDS.find((x) => x.id === id);
  if (!c) return NextResponse.json({ detail: "Not found" }, { status: 404 });
  return NextResponse.json({
    id: c.id,
    topic: c.topic,
    subtopic: c.subtopic,
    front: c.front,
    back: c.back,
    box: 1,
  });
}
