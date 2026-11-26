"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Row = {
  id: number;
  mode: string;
  score: number | null;
  total: number;
  grade: string | null;
  passed: boolean | null;
  started_at: string;
  finished_at: string | null;
  pct: number | null;
};

export default function HistoryPage() {
  const [rows, setRows] = useState<Row[]>([]);

  useEffect(() => {
    api.listAttempts().then(setRows).catch(console.error);
  }, []);
  // Netlify: history comes from browser localStorage via api.listAttempts

  return (
    <div style={{ maxWidth: 860 }}>
      <h1 style={{ margin: "8px 0 18px", fontSize: "1.8rem" }}>History</h1>
      <div className="panel" style={{ padding: 0, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <thead>
            <tr className="muted" style={{ textAlign: "left", background: "var(--shell)" }}>
              <th style={{ padding: "12px 16px" }}>ID</th>
              <th style={{ padding: "12px 16px" }}>Mode</th>
              <th style={{ padding: "12px 16px" }}>Score</th>
              <th style={{ padding: "12px 16px" }}>Grade</th>
              <th style={{ padding: "12px 16px" }}>When</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id} style={{ borderTop: "1px solid var(--line)" }}>
                <td style={{ padding: "12px 16px" }}>
                  {r.finished_at ? (
                    <Link href={`/review/${r.id}`} style={{ color: "var(--purple)", fontWeight: 700 }}>
                      #{r.id}
                    </Link>
                  ) : (
                    `#${r.id}`
                  )}
                </td>
                <td style={{ padding: "12px 16px" }}>{r.mode}</td>
                <td style={{ padding: "12px 16px" }}>
                  {r.score != null ? `${r.score}/${r.total} (${r.pct}%)` : "—"}
                </td>
                <td
                  style={{
                    padding: "12px 16px",
                    color: r.passed ? "var(--success)" : r.passed === false ? "var(--danger)" : undefined,
                    fontWeight: 700,
                  }}
                >
                  {r.grade || "—"}
                </td>
                <td style={{ padding: "12px 16px" }} className="muted">
                  {new Date(r.started_at).toLocaleString()}
                </td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr>
                <td colSpan={5} style={{ padding: 32, textAlign: "center" }} className="muted">
                  No attempts yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
