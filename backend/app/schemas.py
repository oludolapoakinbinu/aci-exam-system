from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TopicOut(BaseModel):
    code: str
    name: str
    exam_count: int
    min_pass: int
    color: str
    question_count: int = 0
    flashcard_count: int = 0
    mastery: float = 0.0


class QuestionPublic(BaseModel):
    id: str
    topic: str
    subtopic: str
    kind: str
    difficulty: str
    question: str
    options: list[str]
    source: str | None = None


class QuestionReview(QuestionPublic):
    answer: int
    explanation: str
    selected: int | None = None
    correct: bool | None = None
    key_corrected: bool = False
    correction_note: str | None = None


class AttemptCreate(BaseModel):
    mode: Literal["practice", "exam", "topic", "weak", "custom", "quick"] = "practice"
    topics: list[str] | None = None
    subtopics: list[str] | None = None
    kinds: list[str] | None = None
    difficulties: list[str] | None = None
    count: int | None = Field(default=None, ge=1, le=200)
    timed: bool = False
    exclude_seen: bool = False
    only_original: bool | None = None


class AttemptStartOut(BaseModel):
    attempt_id: int
    mode: str
    time_limit_sec: int | None
    total: int
    questions: list[QuestionPublic]


class AnswerIn(BaseModel):
    question_id: str
    selected: int | None = Field(default=None, ge=0, le=3)
    flagged: bool = False
    time_spent_sec: int = 0


class SubmitIn(BaseModel):
    answers: list[AnswerIn]


class BasketScore(BaseModel):
    topic: str
    name: str
    correct: int
    total: int
    pct: float
    min_required: int
    passed: bool


class AttemptResult(BaseModel):
    attempt_id: int
    mode: str
    score: int
    total: int
    pct: float
    grade: str
    passed: bool
    baskets: list[BasketScore]
    started_at: datetime
    finished_at: datetime
    reviews: list[QuestionReview]


class AttemptSummary(BaseModel):
    id: int
    mode: str
    score: int | None
    total: int
    grade: str | None
    passed: bool | None
    started_at: datetime
    finished_at: datetime | None
    pct: float | None = None


class StatsOut(BaseModel):
    total_questions: int
    total_flashcards: int
    attempts: int
    exams_passed: int
    overall_accuracy: float
    by_topic: list[dict]
    weak_subtopics: list[dict]
    recent: list[AttemptSummary]
    due_review: int
    streak_days: int


class FlashcardOut(BaseModel):
    id: str
    topic: str
    subtopic: str
    front: str
    back: str | None = None
    box: int = 1


class FlashReviewIn(BaseModel):
    remembered: bool


class SearchOut(BaseModel):
    questions: list[QuestionPublic]
    flashcards: list[FlashcardOut]
