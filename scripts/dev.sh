#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
.venv/bin/pip install -q -r backend/requirements.txt

# Ensure bank exists
if [[ ! -f data/question_bank.json ]]; then
  .venv/bin/python scripts/merge_bank.py
fi

# Reset DB seed if empty / missing
export PYTHONPATH="$ROOT/backend"

.venv/bin/uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000 &
API_PID=$!
trap 'kill $API_PID 2>/dev/null || true' EXIT

cd frontend
if [[ ! -d node_modules ]]; then
  npm install
fi
npm run dev
