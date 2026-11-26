from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    topic: Mapped[str] = mapped_column(String(16), index=True)
    subtopic: Mapped[str] = mapped_column(String(64), index=True)
    kind: Mapped[str] = mapped_column(String(16), index=True)  # theory|calculation
    difficulty: Mapped[str] = mapped_column(String(16), index=True)
    question: Mapped[str] = mapped_column(Text)
    option_a: Mapped[str] = mapped_column(Text)
    option_b: Mapped[str] = mapped_column(Text)
    option_c: Mapped[str] = mapped_column(Text)
    option_d: Mapped[str] = mapped_column(Text)
    answer: Mapped[int] = mapped_column(Integer)  # 0-3
    explanation: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(256), default="")
    source_key: Mapped[str | None] = mapped_column(String(4), nullable=True)
    key_corrected: Mapped[bool] = mapped_column(Boolean, default=False)
    correction_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_original: Mapped[bool] = mapped_column(Boolean, default=False, index=True)


class Flashcard(Base):
    __tablename__ = "flashcards"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    topic: Mapped[str] = mapped_column(String(16), index=True)
    subtopic: Mapped[str] = mapped_column(String(64), index=True)
    front: Mapped[str] = mapped_column(Text)
    back: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(256), default="")


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mode: Mapped[str] = mapped_column(String(32))  # practice|exam|topic|weak|custom
    topic_filter: Mapped[str | None] = mapped_column(String(64), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    time_limit_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total: Mapped[int] = mapped_column(Integer, default=0)
    grade: Mapped[str | None] = mapped_column(String(32), nullable=True)
    passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    basket_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    answers: Mapped[list["AttemptAnswer"]] = relationship(
        back_populates="attempt", cascade="all, delete-orphan"
    )


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"
    __table_args__ = (UniqueConstraint("attempt_id", "question_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("attempts.id"), index=True)
    question_id: Mapped[str] = mapped_column(ForeignKey("questions.id"), index=True)
    selected: Mapped[int | None] = mapped_column(Integer, nullable=True)
    correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    flagged: Mapped[bool] = mapped_column(Boolean, default=False)
    time_spent_sec: Mapped[int] = mapped_column(Integer, default=0)

    attempt: Mapped[Attempt] = relationship(back_populates="answers")


class Progress(Base):
    """Per-question spaced-repetition / mastery tracking."""

    __tablename__ = "progress"

    question_id: Mapped[str] = mapped_column(ForeignKey("questions.id"), primary_key=True)
    times_seen: Mapped[int] = mapped_column(Integer, default=0)
    times_correct: Mapped[int] = mapped_column(Integer, default=0)
    times_wrong: Mapped[int] = mapped_column(Integer, default=0)
    streak: Mapped[int] = mapped_column(Integer, default=0)
    ease: Mapped[float] = mapped_column(Float, default=2.5)
    interval_days: Mapped[float] = mapped_column(Float, default=0)
    due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_result: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class FlashProgress(Base):
    __tablename__ = "flash_progress"

    flashcard_id: Mapped[str] = mapped_column(ForeignKey("flashcards.id"), primary_key=True)
    box: Mapped[int] = mapped_column(Integer, default=1)  # Leitner box 1-5
    times_seen: Mapped[int] = mapped_column(Integer, default=0)
    last_result: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
