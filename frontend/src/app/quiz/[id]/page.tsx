"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AttemptStart } from "@/lib/api";
import { QuizPlayer } from "@/components/QuizPlayer";

export default function QuizPage() {
  const params = useParams<{ id: string }>();
  const [attempt, setAttempt] = useState<AttemptStart | null>(null);

  useEffect(() => {
    const raw = sessionStorage.getItem(`attempt:${params.id}`);
    if (raw) setAttempt(JSON.parse(raw) as AttemptStart);
  }, [params.id]);

  if (!attempt) {
    return (
      <div className="quiz-wrap">
        <div className="quiz-card" style={{ textAlign: "center", minHeight: 280, justifyContent: "center" }}>
          <h1 style={{ marginTop: 0 }}>Session not found</h1>
          <p className="muted">Start a new practice set or mock exam from the menu.</p>
          <Link href="/" className="btn btn-primary">
            Back to dashboard
          </Link>
        </div>
      </div>
    );
  }

  return <QuizPlayer attempt={attempt} />;
}
