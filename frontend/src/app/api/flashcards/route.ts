import { NextResponse } from "next/server";
import { FLASHCARDS } from "@/lib/bank";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const topic = searchParams.get("topic");
  const limit = Number(searchParams.get("limit") || 40);
  const reveal = searchParams.get("reveal") === "true";

  let cards = FLASHCARDS.slice();
  if (topic) cards = cards.filter((c) => c.topic === topic);
  for (let i = cards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [cards[i], cards[j]] = [cards[j], cards[i]];
  }
  cards = cards.slice(0, limit);

  return NextResponse.json(
    cards.map((c) => ({
      id: c.id,
      topic: c.topic,
      subtopic: c.subtopic,
      front: c.front,
      back: reveal ? c.back : null,
      box: 1,
    }))
  );
}
