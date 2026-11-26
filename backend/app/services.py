from __future__ import annotations

import json
import random
from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .config import EXAM_MINUTES, EXAM_PASS, EXAM_TOTAL, GRADES, TOPICS
from .models import Attempt, AttemptAnswer, Flashcard, FlashProgress, Progress, Question


def grade_for(pct: float) -> str:
    for threshold, name in GRADES:
        if pct >= threshold:
            return name
    return "Fail"


def options_of(q: Question) -> list[str]:
    return [q.option_a, q.option_b, q.option_c, q.option_d]


def public_q(q: Question) -> dict:
    return {
        "id": q.id,
        "topic": q.topic,
        "subtopic": q.subtopic,
        "kind": q.kind,
        "difficulty": q.difficulty,
        "question": q.question,
        "options": options_of(q),
        "source": q.source,
    }


def review_q(q: Question, selected: int | None, correct: bool | None) -> dict:
    return {
        **public_q(q),
        "answer": q.answer,
        "explanation": q.explanation,
        "selected": selected,
        "correct": correct,
        "key_corrected": q.key_corrected,
        "correction_note": q.correction_note,
    }


def pick_exam_set(db: Session) -> list[Question]:
    """Official ACI basket sizes: 10 / 18 / 18 / 14 / 10 = 70."""
    chosen: list[Question] = []
    for code, meta in TOPICS.items():
        pool = list(db.scalars(select(Question).where(Question.topic == code)).all())
        if len(pool) < meta["exam_count"]:
            # fall back: take all available and pad from other topics later
            chosen.extend(pool)
            continue
        chosen.extend(random.sample(pool, meta["exam_count"]))
    if len(chosen) < EXAM_TOTAL:
        remaining = list(
            db.scalars(select(Question).where(~Question.id.in_([q.id for q in chosen]))).all()
        )
        need = EXAM_TOTAL - len(chosen)
        chosen.extend(random.sample(remaining, min(need, len(remaining))))
    random.shuffle(chosen)
    return chosen[:EXAM_TOTAL]


def pick_questions(
    db: Session,
    *,
    mode: str,
    topics: list[str] | None,
    subtopics: list[str] | None,
    kinds: list[str] | None,
    difficulties: list[str] | None,
    count: int | None,
    exclude_seen: bool,
    only_original: bool | None,
) -> list[Question]:
    if mode == "exam":
        return pick_exam_set(db)

    q = select(Question)
    if topics:
        q = q.where(Question.topic.in_(topics))
    if subtopics:
        q = q.where(Question.subtopic.in_(subtopics))
    if kinds:
        q = q.where(Question.kind.in_(kinds))
    if difficulties:
        q = q.where(Question.difficulty.in_(difficulties))
    if only_original is True:
        q = q.where(Question.is_original.is_(True))
    if only_original is False:
        q = q.where(Question.is_original.is_(False))

    pool = list(db.scalars(q).all())

    if mode == "weak":
        # Prefer questions with low accuracy / due for review
        progress = {
            p.question_id: p
            for p in db.scalars(select(Progress)).all()
        }

        def weak_score(item: Question) -> float:
            p = progress.get(item.id)
            if not p or p.times_seen == 0:
                return 0.4  # unseen = somewhat priority
            acc = p.times_correct / max(1, p.times_seen)
            due_boost = 0.3 if p.due_at and p.due_at <= datetime.utcnow() else 0
            return (1 - acc) + due_boost

        pool.sort(key=weak_score, reverse=True)
        n = count or 20
        return pool[:n]

    if exclude_seen:
        seen_ids = {
            p.question_id
            for p in db.scalars(select(Progress).where(Progress.times_seen > 0)).all()
        }
        unseen = [x for x in pool if x.id not in seen_ids]
        if unseen:
            pool = unseen

    n = count or (20 if mode in ("practice", "topic", "custom", "quick") else 20)
    if mode == "quick":
        n = count or 10
    if len(pool) <= n:
        random.shuffle(pool)
        return pool
    return random.sample(pool, n)


def update_progress(db: Session, question_id: str, correct: bool) -> None:
    p = db.get(Progress, question_id)
    if not p:
        p = Progress(
            question_id=question_id,
            times_seen=0,
            times_correct=0,
            times_wrong=0,
            streak=0,
            ease=2.5,
            interval_days=0.0,
        )
        db.add(p)
        db.flush()
    p.times_seen = (p.times_seen or 0) + 1
    if correct:
        p.times_correct = (p.times_correct or 0) + 1
        p.streak = (p.streak or 0) + 1
        p.ease = min(3.0, (p.ease or 2.5) + 0.1)
        base = p.interval_days or 0.0
        p.interval_days = 1.0 if base == 0 else min(60.0, base * p.ease)
    else:
        p.times_wrong = (p.times_wrong or 0) + 1
        p.streak = 0
        p.ease = max(1.3, (p.ease or 2.5) - 0.2)
        p.interval_days = 0.5
    p.last_result = correct
    p.last_seen_at = datetime.utcnow()
    p.due_at = datetime.utcnow() + timedelta(days=p.interval_days or 0.5)


def finish_attempt(db: Session, attempt: Attempt, answers_in: list) -> dict:
    by_qid = {a.question_id: a for a in attempt.answers}
    qids = list(by_qid.keys())
    questions = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(qids))).all()}

    correct_count = 0
    basket: dict[str, list[int]] = defaultdict(lambda: [0, 0])  # correct, total
    reviews = []

    for ans_in in answers_in:
        row = by_qid.get(ans_in.question_id)
        q = questions.get(ans_in.question_id)
        if not row or not q:
            continue
        selected = ans_in.selected
        is_correct = selected is not None and selected == q.answer
        row.selected = selected
        row.correct = is_correct
        row.flagged = ans_in.flagged
        row.time_spent_sec = ans_in.time_spent_sec
        basket[q.topic][1] += 1
        if is_correct:
            correct_count += 1
            basket[q.topic][0] += 1
        update_progress(db, q.id, bool(is_correct))
        reviews.append(review_q(q, selected, is_correct))

    total = attempt.total
    pct = (correct_count / total * 100) if total else 0.0
    baskets = []
    all_baskets_ok = True
    for code, meta in TOPICS.items():
        c, t = basket.get(code, [0, 0])
        if t == 0 and attempt.mode != "exam":
            continue
        if attempt.mode == "exam" and t == 0:
            # still report empty baskets
            pass
        min_req = meta["min_pass"] if attempt.mode == "exam" else max(1, int(0.5 * t)) if t else 0
        passed_basket = c >= min_req if attempt.mode == "exam" else (t == 0 or c / t >= 0.5)
        if attempt.mode == "exam" and t > 0 and not passed_basket:
            all_baskets_ok = False
        baskets.append(
            {
                "topic": code,
                "name": meta["name"],
                "correct": c,
                "total": t,
                "pct": round(c / t * 100, 1) if t else 0.0,
                "min_required": min_req if attempt.mode == "exam" else 0,
                "passed": passed_basket,
            }
        )

    overall_pass = pct >= 60 and (all_baskets_ok if attempt.mode == "exam" else pct >= 60)
    if attempt.mode == "exam":
        overall_pass = correct_count >= EXAM_PASS and all_baskets_ok

    attempt.score = correct_count
    attempt.finished_at = datetime.utcnow()
    attempt.grade = grade_for(pct)
    attempt.passed = overall_pass
    attempt.basket_json = json.dumps(baskets)
    db.commit()

    return {
        "attempt_id": attempt.id,
        "mode": attempt.mode,
        "score": correct_count,
        "total": total,
        "pct": round(pct, 1),
        "grade": attempt.grade,
        "passed": overall_pass,
        "baskets": baskets,
        "started_at": attempt.started_at,
        "finished_at": attempt.finished_at,
        "reviews": reviews,
    }


def stats(db: Session) -> dict:
    total_q = db.scalar(select(func.count()).select_from(Question)) or 0
    total_f = db.scalar(select(func.count()).select_from(Flashcard)) or 0
    attempts = db.scalar(select(func.count()).select_from(Attempt)) or 0
    exams_passed = (
        db.scalar(
            select(func.count()).select_from(Attempt).where(
                Attempt.mode == "exam", Attempt.passed.is_(True)
            )
        )
        or 0
    )

    prog = list(db.scalars(select(Progress)).all())
    seen = sum(p.times_seen for p in prog)
    correct = sum(p.times_correct for p in prog)
    overall = (correct / seen * 100) if seen else 0.0

    by_topic = []
    for code, meta in TOPICS.items():
        qs = list(db.scalars(select(Question).where(Question.topic == code)).all())
        pmap = {p.question_id: p for p in prog}
        t_seen = t_ok = 0
        for q in qs:
            p = pmap.get(q.id)
            if p:
                t_seen += p.times_seen
                t_ok += p.times_correct
        by_topic.append(
            {
                "topic": code,
                "name": meta["name"],
                "color": meta["color"],
                "questions": len(qs),
                "accuracy": round(t_ok / t_seen * 100, 1) if t_seen else 0.0,
                "seen": t_seen,
            }
        )

    # weak subtopics
    sub: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    qmap = {q.id: q for q in db.scalars(select(Question)).all()}
    for p in prog:
        q = qmap.get(p.question_id)
        if not q or p.times_seen == 0:
            continue
        key = f"{q.topic}:{q.subtopic}"
        sub[key][0] += p.times_correct
        sub[key][1] += p.times_seen
    weak = []
    for key, (c, s) in sub.items():
        if s < 2:
            continue
        acc = c / s
        if acc < 0.65:
            topic, subt = key.split(":", 1)
            weak.append(
                {
                    "topic": topic,
                    "subtopic": subt,
                    "accuracy": round(acc * 100, 1),
                    "seen": s,
                }
            )
    weak.sort(key=lambda x: x["accuracy"])

    recent_rows = db.scalars(
        select(Attempt).order_by(Attempt.started_at.desc()).limit(10)
    ).all()
    recent = [
        {
            "id": a.id,
            "mode": a.mode,
            "score": a.score,
            "total": a.total,
            "grade": a.grade,
            "passed": a.passed,
            "started_at": a.started_at,
            "finished_at": a.finished_at,
            "pct": round(a.score / a.total * 100, 1) if a.score is not None and a.total else None,
        }
        for a in recent_rows
    ]

    due = (
        db.scalar(
            select(func.count()).select_from(Progress).where(
                Progress.due_at.is_not(None), Progress.due_at <= datetime.utcnow()
            )
        )
        or 0
    )

    # simple streak: consecutive calendar days with a finished attempt
    finished = db.scalars(
        select(Attempt)
        .where(Attempt.finished_at.is_not(None))
        .order_by(Attempt.finished_at.desc())
        .limit(60)
    ).all()
    days = {a.finished_at.date() for a in finished if a.finished_at}
    streak = 0
    day = datetime.utcnow().date()
    while day in days:
        streak += 1
        day -= timedelta(days=1)

    return {
        "total_questions": total_q,
        "total_flashcards": total_f,
        "attempts": attempts,
        "exams_passed": exams_passed,
        "overall_accuracy": round(overall, 1),
        "by_topic": by_topic,
        "weak_subtopics": weak[:8],
        "recent": recent,
        "due_review": due,
        "streak_days": streak,
    }


def leitner_interval(box: int) -> int:
    return {1: 0, 2: 1, 3: 3, 4: 7, 5: 14}.get(box, 1)
