"use client";

import { useEffect, useState } from "react";
import { api, Flashcard } from "@/lib/api";
import { TOPIC_META } from "@/lib/topics";

export default function FlashcardsPage() {
  const [topic, setTopic] = useState("");
  const [dueOnly, setDueOnly] = useState(true);
  const [deck, setDeck] = useState<Flashcard[]>([]);
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [back, setBack] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(0);

  async function load() {
    setLoading(true);
    setFlipped(false);
    setBack(null);
    setIdx(0);
    setDone(0);
    try {
      const cards = await api.flashcards({
        topic: topic || undefined,
        due: dueOnly,
        limit: 40,
      });
      setDeck(cards);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const card = deck[idx];

  async function reveal() {
    if (!card) return;
    const full = await api.getFlashcard(card.id);
    setBack(full.back);
    setFlipped(true);
  }

  async function rate(remembered: boolean) {
    if (!card) return;
    await api.reviewFlashcard(card.id, remembered);
    setDone((d) => d + 1);
    setFlipped(false);
    setBack(null);
    if (idx + 1 >= deck.length) setDeck([]);
    else setIdx((i) => i + 1);
  }

  return (
    <div style={{ maxWidth: 640 }}>
      <h1 style={{ margin: "8px 0 6px", fontSize: "1.8rem" }}>Flashcards</h1>
      <p className="muted" style={{ marginTop: 0, marginBottom: 18 }}>
        Flip, then rate — forgotten cards return to box 1 (Leitner).
      </p>

      <div className="panel" style={{ display: "flex", flexWrap: "wrap", gap: 12, marginBottom: 16 }}>
        <label style={{ display: "grid", gap: 6, fontWeight: 650 }}>
          Topic
          <select
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            style={{ border: "1px solid var(--line)", borderRadius: 12, padding: "10px 12px" }}
          >
            <option value="">All topics</option>
            {Object.entries(TOPIC_META).map(([code, meta]) => (
              <option key={code} value={code}>
                {meta.name}
              </option>
            ))}
          </select>
        </label>
        <label style={{ display: "flex", alignItems: "center", gap: 8, paddingTop: 22 }}>
          <input type="checkbox" checked={dueOnly} onChange={(e) => setDueOnly(e.target.checked)} />
          Due / new only
        </label>
        <button
          type="button"
          className="btn btn-primary"
          style={{ alignSelf: "end" }}
          onClick={() => void load()}
          disabled={loading}
        >
          {loading ? "Loading…" : "Load deck"}
        </button>
      </div>

      {!card ? (
        <div className="panel" style={{ textAlign: "center", padding: 40 }}>
          <p className="muted">
            {done > 0 ? `Session complete — reviewed ${done} cards.` : "No cards in this filter."}
          </p>
          <button type="button" className="btn btn-ghost" onClick={() => void load()}>
            Reload
          </button>
        </div>
      ) : (
        <div className="panel">
          <div
            className="muted"
            style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 10 }}
          >
            <span>
              {card.topic} · {card.subtopic} · box {card.box}
            </span>
            <span>
              {idx + 1}/{deck.length} · reviewed {done}
            </span>
          </div>
          <button
            type="button"
            onClick={() => void (flipped ? null : reveal())}
            style={{
              width: "100%",
              minHeight: 220,
              borderRadius: 18,
              border: "1px solid var(--line)",
              background: "var(--shell)",
              padding: 24,
              textAlign: "left",
              cursor: flipped ? "default" : "pointer",
            }}
          >
            <div style={{ color: "var(--purple)", fontWeight: 800, fontSize: 12, marginBottom: 8 }}>
              {flipped ? "ANSWER" : "PROMPT — click to flip"}
            </div>
            <div style={{ fontSize: 18, lineHeight: 1.5, whiteSpace: "pre-wrap" }}>
              {flipped ? back : card.front}
            </div>
          </button>
          {flipped && (
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginTop: 14 }}>
              <button type="button" className="btn btn-ghost" onClick={() => void rate(false)}>
                Forgot
              </button>
              <button type="button" className="btn btn-cyan" onClick={() => void rate(true)}>
                Remembered
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
