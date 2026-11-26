# ACI Dealing Certificate Exam System

Local study platform for the **ACI Dealing Certificate New Version (exam code 002-101)** built from your ICAP / Tridge materials.

## Stack

- **Frontend:** Next.js (App Router) + Tailwind
- **Backend:** FastAPI + SQLite
- **Content:** Parsed practice exams + workshop questions + original MCQs/flashcards authored from the study PDFs

## Features

- Mock exam (70 Qs, 120 min, official topic baskets & 50% basket minimums, Pass/Merit/Distinction)
- Topic / quick / weak-area practice with filters (theory vs calculation, difficulty)
- Full post-attempt review with an explanation on every question
- Flashcards with Leitner spaced repetition
- Dashboard: mastery by topic, weak subtopics, streak, history
- Progress tracking (ease / due dates) across attempts

## Live (Netlify)

**https://aci-dealing-prep.netlify.app**

The production app runs entirely on Netlify (Next.js + API route handlers). Progress/history are stored in the browser (`localStorage`). The optional FastAPI + SQLite backend is for local development only.

## Quick start (local)

```bash
# Frontend only (recommended — same as Netlify)
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

Optional local FastAPI (set `USE_FASTAPI=1` when starting Next):

```bash
cd backend && ../.venv/bin/uvicorn app.main:app --reload --port 8000
```

### Rebuild the question bank from source text

```bash
.venv/bin/python scripts/parse_practice_exams.py
.venv/bin/python scripts/parse_workshop.py
.venv/bin/python scripts/build_seed_content.py
.venv/bin/python scripts/expand_flashcards.py
.venv/bin/python scripts/merge_bank.py
# then hit POST /api/admin/reload or delete data/aci.db and restart the API
```

## Exam blueprint (encoded in the app)

| Topic | Questions | Min correct (50%) |
|-------|-----------|-------------------|
| Financial Markets Environment | 10 | 5 |
| Foreign Exchange | 18 | 9 |
| Rates | 18 | 9 |
| FICC Derivatives | 14 | 7 |
| Financial Markets Applications | 10 | 5 |

Overall pass **60% (42/70)**. Merit 70%+, Distinction 80%+.

## Content notes

- Practice-exam answer keys are known to contain errors. Calculation items that we have re-worked are corrected in the bank; remaining theory items keep the source key but should be treated as living content — flag anything suspicious.
- The WhatsApp-scanned workbook is a duplicate of the text-layer Workshop Exercise Book (no extra unique questions).
- Source PDF text lives in `source_text/` (for authoring only; not served to the browser).

## Project layout

```
backend/app/     FastAPI API
frontend/        Next.js UI
data/            SQLite DB + merged JSON banks
data/raw/        Per-batch extraction outputs
scripts/         PDF extract, parsers, validators
source_text/     Extracted study material
```
