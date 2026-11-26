from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from .config import DATA_DIR, EXAM_MINUTES, TOPICS
from .db import Base, engine, get_db
from .models import Attempt, AttemptAnswer, Flashcard, FlashProgress, Progress, Question
from .schemas import (
    AnswerIn,
    AttemptCreate,
    AttemptResult,
    AttemptStartOut,
    AttemptSummary,
    FlashcardOut,
    FlashReviewIn,
    QuestionPublic,
    SearchOut,
    StatsOut,
    SubmitIn,
    TopicOut,
)
from . import services

app = FastAPI(title="ACI Exam System", version="1.0.0")


def _cors_origins() -> list[str]:
    defaults = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://aci-dealing-prep.netlify.app",
    ]
    extra = os.getenv("CORS_ORIGINS", "")
    for part in extra.split(","):
        origin = part.strip()
        if origin and origin not in defaults:
            defaults.append(origin)
    return defaults


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    # Auto-seed if empty
    from sqlalchemy.orm import Session as SASession

    with SASession(engine) as db:
        n = db.scalar(select(func.count()).select_from(Question)) or 0
        if n == 0:
            bank = DATA_DIR / "question_bank.json"
            cards = DATA_DIR / "flashcards.json"
            if bank.exists():
                _load_questions(db, json.loads(bank.read_text()))
            if cards.exists():
                _load_flashcards(db, json.loads(cards.read_text()))
            db.commit()


def _load_questions(db: Session, items: list[dict]) -> int:
    count = 0
    for item in items:
        if db.get(Question, item["id"]):
            continue
        opts = item["options"]
        db.add(
            Question(
                id=item["id"],
                topic=item["topic"],
                subtopic=item["subtopic"],
                kind=item["kind"],
                difficulty=item["difficulty"],
                question=item["question"],
                option_a=opts[0],
                option_b=opts[1],
                option_c=opts[2],
                option_d=opts[3],
                answer=item["answer"],
                explanation=item["explanation"],
                source=item.get("source") or "",
                source_key=item.get("source_key"),
                key_corrected=bool(item.get("key_corrected")),
                correction_note=item.get("correction_note"),
                is_original=str(item.get("source", "")).startswith("Original")
                or bool(item.get("is_original")),
            )
        )
        count += 1
    return count


def _load_flashcards(db: Session, items: list[dict]) -> int:
    count = 0
    for item in items:
        if db.get(Flashcard, item["id"]):
            continue
        db.add(
            Flashcard(
                id=item["id"],
                topic=item["topic"],
                subtopic=item["subtopic"],
                front=item["front"],
                back=item["back"],
                source=item.get("source") or "",
            )
        )
        count += 1
    return count


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/topics", response_model=list[TopicOut])
def topics(db: Session = Depends(get_db)):
    prog = {p.question_id: p for p in db.scalars(select(Progress)).all()}
    out = []
    for code, meta in TOPICS.items():
        qs = list(db.scalars(select(Question).where(Question.topic == code)).all())
        fc = db.scalar(
            select(func.count()).select_from(Flashcard).where(Flashcard.topic == code)
        ) or 0
        seen = ok = 0
        for q in qs:
            p = prog.get(q.id)
            if p:
                seen += p.times_seen
                ok += p.times_correct
        out.append(
            TopicOut(
                **meta,
                question_count=len(qs),
                flashcard_count=fc,
                mastery=round(ok / seen * 100, 1) if seen else 0.0,
            )
        )
    return out


@app.get("/api/stats", response_model=StatsOut)
def get_stats(db: Session = Depends(get_db)):
    return services.stats(db)


@app.post("/api/attempts", response_model=AttemptStartOut)
def start_attempt(body: AttemptCreate, db: Session = Depends(get_db)):
    questions = services.pick_questions(
        db,
        mode=body.mode,
        topics=body.topics,
        subtopics=body.subtopics,
        kinds=body.kinds,
        difficulties=body.difficulties,
        count=body.count,
        exclude_seen=body.exclude_seen,
        only_original=body.only_original,
    )
    if not questions:
        raise HTTPException(404, "No questions match those filters. Seed the bank first.")

    time_limit = None
    if body.mode == "exam" or body.timed:
        time_limit = EXAM_MINUTES * 60 if body.mode == "exam" else (body.count or 20) * 90

    attempt = Attempt(
        mode=body.mode,
        topic_filter=",".join(body.topics) if body.topics else None,
        time_limit_sec=time_limit,
        total=len(questions),
    )
    db.add(attempt)
    db.flush()
    for q in questions:
        db.add(AttemptAnswer(attempt_id=attempt.id, question_id=q.id))
    db.commit()
    db.refresh(attempt)
    return AttemptStartOut(
        attempt_id=attempt.id,
        mode=attempt.mode,
        time_limit_sec=time_limit,
        total=len(questions),
        questions=[QuestionPublic(**services.public_q(q)) for q in questions],
    )


@app.get("/api/attempts", response_model=list[AttemptSummary])
def list_attempts(db: Session = Depends(get_db), limit: int = 30):
    rows = db.scalars(select(Attempt).order_by(Attempt.started_at.desc()).limit(limit)).all()
    return [
        AttemptSummary(
            id=a.id,
            mode=a.mode,
            score=a.score,
            total=a.total,
            grade=a.grade,
            passed=a.passed,
            started_at=a.started_at,
            finished_at=a.finished_at,
            pct=round(a.score / a.total * 100, 1) if a.score is not None and a.total else None,
        )
        for a in rows
    ]


@app.post("/api/attempts/{attempt_id}/submit", response_model=AttemptResult)
def submit_attempt(attempt_id: int, body: SubmitIn, db: Session = Depends(get_db)):
    attempt = db.get(Attempt, attempt_id)
    if not attempt:
        raise HTTPException(404, "Attempt not found")
    if attempt.finished_at:
        raise HTTPException(400, "Attempt already submitted")
    return services.finish_attempt(db, attempt, body.answers)


@app.get("/api/attempts/{attempt_id}", response_model=AttemptResult)
def get_attempt(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.get(Attempt, attempt_id)
    if not attempt or not attempt.finished_at:
        raise HTTPException(404, "Finished attempt not found")
    answers = list(db.scalars(select(AttemptAnswer).where(AttemptAnswer.attempt_id == attempt_id)))
    qids = [a.question_id for a in answers]
    qmap = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(qids))).all()}
    reviews = [
        services.review_q(qmap[a.question_id], a.selected, a.correct)
        for a in answers
        if a.question_id in qmap
    ]
    baskets = json.loads(attempt.basket_json or "[]")
    pct = round(attempt.score / attempt.total * 100, 1) if attempt.score is not None else 0
    return AttemptResult(
        attempt_id=attempt.id,
        mode=attempt.mode,
        score=attempt.score or 0,
        total=attempt.total,
        pct=pct,
        grade=attempt.grade or "Fail",
        passed=bool(attempt.passed),
        baskets=baskets,
        started_at=attempt.started_at,
        finished_at=attempt.finished_at,
        reviews=reviews,
    )


@app.get("/api/questions/{qid}/explain")
def explain(qid: str, db: Session = Depends(get_db)):
    q = db.get(Question, qid)
    if not q:
        raise HTTPException(404)
    return {
        "id": q.id,
        "answer": q.answer,
        "explanation": q.explanation,
        "options": services.options_of(q),
        "key_corrected": q.key_corrected,
        "correction_note": q.correction_note,
    }


@app.get("/api/flashcards", response_model=list[FlashcardOut])
def list_flashcards(
    db: Session = Depends(get_db),
    topic: str | None = None,
    due: bool = False,
    limit: int = 40,
    reveal: bool = False,
):
    q = select(Flashcard)
    if topic:
        q = q.where(Flashcard.topic == topic)
    cards = list(db.scalars(q).all())
    prog = {p.flashcard_id: p for p in db.scalars(select(FlashProgress)).all()}
    if due:
        now = datetime.utcnow()
        filtered = []
        for c in cards:
            p = prog.get(c.id)
            if not p or p.due_at is None or p.due_at <= now:
                filtered.append(c)
        cards = filtered
    import random

    random.shuffle(cards)
    cards = cards[:limit]
    out = []
    for c in cards:
        p = prog.get(c.id)
        out.append(
            FlashcardOut(
                id=c.id,
                topic=c.topic,
                subtopic=c.subtopic,
                front=c.front,
                back=c.back if reveal else None,
                box=p.box if p else 1,
            )
        )
    return out


@app.get("/api/flashcards/{fid}", response_model=FlashcardOut)
def get_flashcard(fid: str, db: Session = Depends(get_db)):
    c = db.get(Flashcard, fid)
    if not c:
        raise HTTPException(404)
    p = db.get(FlashProgress, fid)
    return FlashcardOut(
        id=c.id,
        topic=c.topic,
        subtopic=c.subtopic,
        front=c.front,
        back=c.back,
        box=p.box if p else 1,
    )


@app.post("/api/flashcards/{fid}/review")
def review_flashcard(fid: str, body: FlashReviewIn, db: Session = Depends(get_db)):
    c = db.get(Flashcard, fid)
    if not c:
        raise HTTPException(404)
    p = db.get(FlashProgress, fid)
    if not p:
        p = FlashProgress(flashcard_id=fid)
        db.add(p)
    p.times_seen += 1
    p.last_result = body.remembered
    p.last_seen_at = datetime.utcnow()
    if body.remembered:
        p.box = min(5, p.box + 1)
    else:
        p.box = 1
    p.due_at = datetime.utcnow() + timedelta(days=services.leitner_interval(p.box))
    db.commit()
    return {"ok": True, "box": p.box, "due_at": p.due_at}


@app.get("/api/search", response_model=SearchOut)
def search(q: str = Query(min_length=2), db: Session = Depends(get_db), limit: int = 20):
    like = f"%{q}%"
    qs = list(
        db.scalars(
            select(Question)
            .where(or_(Question.question.ilike(like), Question.explanation.ilike(like)))
            .limit(limit)
        ).all()
    )
    fs = list(
        db.scalars(
            select(Flashcard)
            .where(or_(Flashcard.front.ilike(like), Flashcard.back.ilike(like)))
            .limit(limit)
        ).all()
    )
    return SearchOut(
        questions=[QuestionPublic(**services.public_q(x)) for x in qs],
        flashcards=[
            FlashcardOut(id=f.id, topic=f.topic, subtopic=f.subtopic, front=f.front, back=None)
            for f in fs
        ],
    )


def _upsert_questions(db: Session, items: list[dict], *, update_existing: bool) -> tuple[int, int]:
    added = updated = 0
    for item in items:
        opts = item["options"]
        existing = db.get(Question, item["id"])
        if existing:
            if not update_existing:
                continue
            existing.topic = item["topic"]
            existing.subtopic = item["subtopic"]
            existing.kind = item["kind"]
            existing.difficulty = item["difficulty"]
            existing.question = item["question"]
            existing.option_a = opts[0]
            existing.option_b = opts[1]
            existing.option_c = opts[2]
            existing.option_d = opts[3]
            existing.answer = item["answer"]
            existing.explanation = item["explanation"]
            existing.source = item.get("source") or ""
            existing.source_key = item.get("source_key")
            existing.key_corrected = bool(item.get("key_corrected"))
            existing.correction_note = item.get("correction_note")
            existing.is_original = str(item.get("source", "")).startswith("Original") or bool(
                item.get("is_original")
            )
            updated += 1
            continue
        db.add(
            Question(
                id=item["id"],
                topic=item["topic"],
                subtopic=item["subtopic"],
                kind=item["kind"],
                difficulty=item["difficulty"],
                question=item["question"],
                option_a=opts[0],
                option_b=opts[1],
                option_c=opts[2],
                option_d=opts[3],
                answer=item["answer"],
                explanation=item["explanation"],
                source=item.get("source") or "",
                source_key=item.get("source_key"),
                key_corrected=bool(item.get("key_corrected")),
                correction_note=item.get("correction_note"),
                is_original=str(item.get("source", "")).startswith("Original")
                or bool(item.get("is_original")),
            )
        )
        added += 1
    return added, updated


@app.post("/api/admin/reload")
def reload_bank(force: bool = False, db: Session = Depends(get_db)):
    """Reload banks. force=true updates existing question explanations/fields."""
    bank = DATA_DIR / "question_bank.json"
    cards = DATA_DIR / "flashcards.json"
    nq = nf = uq = 0
    if bank.exists():
        a, u = _upsert_questions(db, json.loads(bank.read_text()), update_existing=force)
        nq += a
        uq += u
    if cards.exists():
        nf += _load_flashcards(db, json.loads(cards.read_text()))
    raw = DATA_DIR / "raw"
    if raw.exists():
        for path in sorted(raw.glob("*.questions.json")):
            a, u = _upsert_questions(db, json.loads(path.read_text()), update_existing=force)
            nq += a
            uq += u
        for path in sorted(raw.glob("*.flashcards.json")):
            nf += _load_flashcards(db, json.loads(path.read_text()))
    db.commit()
    total_q = db.scalar(select(func.count()).select_from(Question)) or 0
    total_f = db.scalar(select(func.count()).select_from(Flashcard)) or 0
    return {
        "added_questions": nq,
        "updated_questions": uq,
        "added_flashcards": nf,
        "total_questions": total_q,
        "total_flashcards": total_f,
        "forced": force,
    }
