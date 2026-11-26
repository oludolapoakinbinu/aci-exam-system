"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";

const MAIN = [
  { href: "/", label: "Dashboard", icon: "▦" },
  { href: "/exam", label: "Mock Exams", icon: "◉" },
  { href: "/practice", label: "Practice Questions", icon: "✎" },
  { href: "/flashcards", label: "Flashcards", icon: "▣" },
  { href: "/formulas", label: "Formula Sheet", icon: "ƒ" },
  { href: "/traps", label: "Exam Traps", icon: "⚠" },
  { href: "/history", label: "History", icon: "◷" },
];

const HELP = [
  { href: "/practice?mode=weak", label: "Weak Areas", icon: "!" },
  { href: "/practice?mode=quick", label: "Quick 10", icon: "⚡" },
  { href: "/traps", label: "All section traps", icon: "⚠" },
]

export function AppShell({ children }: { children: ReactNode }) {
  const path = usePathname();
  const quizMode = path.startsWith("/quiz");

  if (quizMode) {
    return (
      <div className="app-stage">
        <span className="geo-dot" style={{ top: "22%", left: "8%" }} />
        <span className="geo-dot" style={{ top: "70%", left: "18%" }} />
        <span className="geo-dot" style={{ top: "30%", right: "12%" }} />
        <div className="app-shell quiz-mode">{children}</div>
      </div>
    );
  }

  return (
    <div className="app-stage">
      <span className="geo-dot" style={{ top: "16%", left: "6%" }} />
      <span className="geo-dot" style={{ top: "58%", left: "4%" }} />
      <span className="geo-dot" style={{ top: "24%", right: "7%" }} />
      <span className="geo-dot" style={{ bottom: "18%", right: "16%" }} />
      <span
        aria-hidden
        style={{
          position: "absolute",
          top: "12%",
          right: "6%",
          width: 56,
          height: 56,
          borderRadius: "50%",
          border: "10px solid rgba(255,255,255,0.16)",
          zIndex: 0,
        }}
      />
      <span
        aria-hidden
        style={{
          position: "absolute",
          bottom: "14%",
          left: "5%",
          width: 0,
          height: 0,
          borderLeft: "28px solid transparent",
          borderRight: "28px solid transparent",
          borderBottom: "48px solid rgba(42,212,201,0.45)",
          zIndex: 0,
        }}
      />

      <div className="app-shell">
        <aside className="sidebar">
          <Link href="/" className="brand">
            <span className="brand-mark">ACI</span>
            <span>ACI Prep</span>
          </Link>

          <div className="nav-section">Main</div>
          {MAIN.map((item) => {
            const active =
              item.href === "/"
                ? path === "/"
                : path === item.href || path.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`nav-link ${active ? "active" : ""}`}
              >
                <span aria-hidden>{item.icon}</span>
                {item.label}
              </Link>
            );
          })}

          <div className="nav-section" style={{ marginTop: 18 }}>
            Study tools
          </div>
          {HELP.map((item) => (
            <Link key={item.href} href={item.href} className="nav-link">
              <span aria-hidden>{item.icon}</span>
              {item.label}
            </Link>
          ))}

          <div style={{ flex: 1 }} />
          <div className="muted" style={{ fontSize: 11, padding: "8px 12px" }}>
            ACI Dealing Certificate 002-101
          </div>
        </aside>

        <div style={{ display: "flex", flexDirection: "column", minWidth: 0 }}>
          <div className="mobile-nav">
            {MAIN.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`chip ${path === item.href ? "active" : ""}`}
              >
                {item.label}
              </Link>
            ))}
          </div>
          <header className="topbar">
            <form
              className="search"
              onSubmit={(e) => {
                e.preventDefault();
                const q = new FormData(e.currentTarget).get("q");
                if (typeof q === "string" && q.trim()) {
                  window.location.href = `/practice?q=${encodeURIComponent(q.trim())}`;
                }
              }}
            >
              <span aria-hidden>⌕</span>
              <input name="q" placeholder="Search topics or start a drill…" />
            </form>
            <div className="profile">
              <span className="muted" style={{ fontSize: 18 }} aria-hidden>
                🔔
              </span>
              <div className="avatar">D</div>
              <div style={{ lineHeight: 1.2 }}>
                <div style={{ fontWeight: 700, fontSize: 0.92 }}>Candidate</div>
                <div className="muted" style={{ fontSize: 0.78 }}>
                  Student
                </div>
              </div>
            </div>
          </header>
          <div className="content">{children}</div>
        </div>
      </div>
    </div>
  );
}
