import questionsData from "../../data/question_bank.json";
import flashcardsData from "../../data/flashcards.json";

export type BankQuestion = {
  id: string;
  topic: string;
  subtopic: string;
  kind: string;
  difficulty: string;
  question: string;
  options: string[];
  answer: number;
  explanation: string;
  source?: string;
  source_key?: string | null;
  key_corrected?: boolean;
  correction_note?: string | null;
  is_original?: boolean;
};

export type BankFlashcard = {
  id: string;
  topic: string;
  subtopic: string;
  front: string;
  back: string;
  source?: string;
};

export const QUESTIONS = questionsData as BankQuestion[];
export const FLASHCARDS = flashcardsData as BankFlashcard[];

export const TOPIC_META: Record<
  string,
  { code: string; name: string; exam_count: number; min_pass: number; color: string }
> = {
  fme: {
    code: "fme",
    name: "Financial Markets Environment",
    exam_count: 10,
    min_pass: 5,
    color: "#0ea5e9",
  },
  fx: {
    code: "fx",
    name: "Foreign Exchange",
    exam_count: 18,
    min_pass: 9,
    color: "#8b5cf6",
  },
  rates: {
    code: "rates",
    name: "Rates",
    exam_count: 18,
    min_pass: 9,
    color: "#10b981",
  },
  ficc: {
    code: "ficc",
    name: "FICC Derivatives",
    exam_count: 14,
    min_pass: 7,
    color: "#f59e0b",
  },
  fma: {
    code: "fma",
    name: "Financial Markets Applications",
    exam_count: 10,
    min_pass: 5,
    color: "#ef4444",
  },
};

const byId = new Map(QUESTIONS.map((q) => [q.id, q]));

export function getQuestion(id: string) {
  return byId.get(id);
}
