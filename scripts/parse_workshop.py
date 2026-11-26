"""Parse Workshop Exercise Book section questions + 4 practice exams."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source_text" / "ACI Dealing Workshop Exercise Book With Practice Exams January 2021.txt"
OUT = ROOT / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

# Reuse classify from practice exam parser
import importlib.util

spec = importlib.util.spec_from_file_location(
    "pe", ROOT / "scripts" / "parse_practice_exams.py"
)
pe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pe)


def clean(s: str) -> str:
    s = s.replace("\xa0", " ").replace("\u00a0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{2,}", "\n", s)
    return s.strip()


def parse_answer_block(text: str) -> dict[int, str]:
    keys = {}
    for m in re.finditer(r"(?m)^\s*(\d+)\s*[\.\)]\s*([A-Da-d])\b", text):
        keys[int(m.group(1))] = m.group(2).upper()
    # also "1. C" with special spaces
    for m in re.finditer(r"(\d+)[\.\)]\s*([A-Da-d])\b", text):
        keys.setdefault(int(m.group(1)), m.group(2).upper())
    return keys


def parse_mcqs(block: str) -> dict[int, dict]:
    """Parse numbered questions with A-D options."""
    block = clean(block)
    # Split on question numbers at line starts
    starts = list(re.finditer(r"(?m)^(?:Question\s+)?(\d+)[\.\)]\s+", block))
    # Also match "1. " after newlines when "Question" missing
    if len(starts) < 3:
        starts = list(re.finditer(r"(?m)^(\d+)[\.\)]\s+", block))
    result = {}
    for i, m in enumerate(starts):
        qn = int(m.group(1))
        end = starts[i + 1].start() if i + 1 < len(starts) else len(block)
        body = block[m.end():end]
        opt_m = list(re.finditer(r"(?m)^\s*([A-D])[\.\)]\s+", body))
        if len(opt_m) < 4:
            opt_m = list(re.finditer(r"(?m)([A-D])[\.\)]\s+", body))
        if len(opt_m) < 4:
            continue
        # take first 4 A,B,C,D in order if possible
        by_letter = {}
        for om in opt_m:
            letter = om.group(1).upper()
            if letter in by_letter:
                continue
            s = om.end()
            # end at next option marker
            nxt = None
            for om2 in opt_m:
                if om2.start() > om.start() and om2.group(1).upper() not in by_letter:
                    # find next unused
                    pass
            # simpler: find next A-D marker after this
            nxt_m = re.search(r"(?m)^\s*[A-D][\.\)]\s+", body[s:])
            e = s + nxt_m.start() if nxt_m else len(body)
            # also stop at Answers
            ans_m = re.search(r"(?i)\bAnswers?\b", body[s:e])
            if ans_m:
                e = s + ans_m.start()
            by_letter[letter] = re.sub(r"\s+", " ", body[s:e]).strip()
            if len(by_letter) == 4:
                break
        if set(by_letter) != {"A", "B", "C", "D"}:
            continue
        stem = re.sub(r"\s+", " ", body[: opt_m[0].start()]).strip()
        # strip trailing "Answers" contamination from stem if any
        stem = re.split(r"(?i)\bAnswers?\b", stem)[0].strip()
        if len(stem) < 10:
            continue
        result[qn] = {"stem": stem, "options": [by_letter[x] for x in "ABCD"]}
    return result


SECTIONS = [
    # (batch_prefix, topic, start_marker, end_marker, answer_marker)
    ("WB-FME", "fme", r"Topic\s*1", r"Topic\s*2", r"Answers\s*[–\-—]?\s*Financial Market Environment"),
    ("WB-FXT", "fx", r"Foreign\s*Exchange\s*Theory", r"Foreign\s*Exchange\s*Calculations|Answers\s*[–\-—]?\s*Foreign Exchange Theory", r"Answers\s*[–\-—]?\s*Foreign Exchange Theory"),
    ("WB-FXC", "fx", r"Foreign\s*Exchange\s*Calculations", r"Topic\s*3|Section\s*3|Basic Interest", r"Answers\s*[–\-—]?\s*Foreign Exchange Calculations"),
    ("WB-IRC", "rates", r"Basic\s*Interest\s*Rate\s*Calculations", r"Money\s*Market\s*Theory", r"Answers\s*[–\-—]?\s*Basic Interest"),
    ("WB-MMT", "rates", r"Money\s*Market\s*Theory", r"Money\s*Market\s*Calculations", r"Answers\s*[–\-—]?\s*Money Market Theory"),
    ("WB-MMC", "rates", r"Money\s*Market\s*Calculations", r"Bonds", r"Answers\s*[–\-—]?\s*Money Market Calculations"),
    ("WB-BND", "rates", r"(?m)Bonds\s*$|Topic.*Bonds|^d\.\s*Bonds", r"Topic\s*4|FICC|FRAs?,?\s*Futures", r"Answers\s*[–\-—]?\s*Bonds"),
]


def extract_between(text: str, start_pat: str, end_pat: str | None) -> str:
    sm = re.search(start_pat, text, re.I)
    if not sm:
        return ""
    rest = text[sm.end():]
    if end_pat:
        em = re.search(end_pat, rest, re.I)
        if em:
            return rest[: em.start()]
    return rest


def main():
    text = SRC.read_text()
    # Only Part 1 (before Part 2 / Practice Exam) for section questions — Part 3 exams separately
    part1 = text
    pe1 = re.search(r"SECTION\s*1\s*[–\-—]?\s*FINANCIAL\s*MARKET\s*ENVIRONMENT", text, re.I)
    part1_end = pe1.start() if pe1 else len(text)
    section_text = text[:part1_end]

    all_items = []

    # Broader section split using answer headers
    answer_headers = list(
        re.finditer(
            r"(?mi)^Answers?\s*[–\-—:]?\s*(.+?)\s*$",
            section_text,
        )
    )
    print(f"Found {len(answer_headers)} answer tables in Part 1 area")

    # For each answer table, take text before it back to previous answer table / topic header
    for i, ah in enumerate(answer_headers):
        # skip practice exam solutions that might leak
        header = ah.group(1).strip()
        if re.search(r"practice exam|solutions to", header, re.I):
            continue
        ans_start = ah.start()
        ans_end = answer_headers[i + 1].start() if i + 1 < len(answer_headers) else part1_end
        # questions are between previous answer end and this answer start
        prev_end = answer_headers[i - 1].end() if i > 0 else 0
        q_block = section_text[prev_end:ans_start]
        a_block = section_text[ans_start:ans_end]
        keys = parse_answer_block(a_block)
        qs = parse_mcqs(q_block)
        # topic guess from header
        h = header.lower()
        if "environment" in h or "market environment" in h:
            topic = "fme"
            prefix = "WB-FME"
        elif "exchange calculation" in h or "fx calculation" in h:
            topic = "fx"
            prefix = "WB-FXC"
        elif "exchange" in h or "fx" in h:
            topic = "fx"
            prefix = "WB-FXT"
        elif "basic interest" in h:
            topic = "rates"
            prefix = "WB-IRC"
        elif "money market theory" in h:
            topic = "rates"
            prefix = "WB-MMT"
        elif "money market calc" in h:
            topic = "rates"
            prefix = "WB-MMC"
        elif "bond" in h:
            topic = "rates"
            prefix = "WB-BND"
        elif "fra" in h or "future" in h or "irs" in h or "swap" in h:
            topic = "ficc"
            prefix = "WB-FRA"
        elif "option" in h:
            topic = "ficc"
            prefix = "WB-OPT"
        elif "alm" in h or "asset" in h:
            topic = "fma"
            prefix = "WB-ALM"
        elif "risk" in h:
            topic = "fma"
            prefix = "WB-RSK"
        else:
            topic = "fme"
            prefix = "WB-GEN"

        matched = 0
        for qn, q in sorted(qs.items()):
            if qn not in keys:
                continue
            letter = keys[qn]
            ans = "ABCD".index(letter)
            t, sub, kind, diff = pe.classify(q["stem"] + " " + " ".join(q["options"]))
            # prefer section topic
            if topic in pe.SUBTOPIC_DEFAULT:
                t = topic
                if sub not in pe.SUBTOPICS_SAFE(t) if False else True:
                    sub = pe.SUBTOPIC_DEFAULT[t]
            items = {
                "id": f"{prefix}-{qn:03d}",
                "topic": t,
                "subtopic": pe.SUBTOPIC_DEFAULT[t],
                "kind": kind,
                "difficulty": diff,
                "question": q["stem"],
                "options": q["options"],
                "answer": ans,
                "explanation": pe.build_explanation(t, letter, q["options"][ans], kind, q["stem"]),
                "source": f"Workshop Exercise Book - {header} Q{qn}",
                "source_key": letter,
                "key_corrected": False,
                "correction_note": None,
            }
            # refine subtopic
            _, sub2, _, _ = pe.classify(q["stem"] + " " + " ".join(q["options"]))
            # classify returns topic too - get sub via hints
            for pat, tp, s in pe.SUBTOPIC_HINTS:
                if tp == t and re.search(pat, (q["stem"] + " ".join(q["options"])).lower()):
                    items["subtopic"] = s
                    break
            else:
                items["subtopic"] = pe.SUBTOPIC_DEFAULT[t]
            all_items.append(items)
            matched += 1
        print(f"  {header[:50]!r}: qs={len(qs)} keys={len(keys)} matched={matched}")

    # Practice exams in workshop (Part 3)
    for exam_n, sol_pat in [
        (1, r"Practice Exam 1 solutions"),
        (2, r"Practice Exam 2 solutions"),
        (3, r"Practice Exam 3 solutions"),
        (4, r"Practice Exam 4 solutions"),
    ]:
        sol_m = re.search(sol_pat, text, re.I)
        if not sol_m:
            print(f"WPE{exam_n}: no solutions")
            continue
        # questions: previous section header to solutions
        # Find "SECTION 1" for this exam - they repeat
        # Use line numbers from earlier grep: solutions at 5319, 6291, 7048, 7839
        # Heuristic: from previous solutions end to this solutions
        prev = None
        for prev_n, prev_pat in [
            (0, r"Part\s*3|4\s*Practice Exams"),
            (1, r"Practice Exam 1 solutions"),
            (2, r"Practice Exam 2 solutions"),
            (3, r"Practice Exam 3 solutions"),
        ]:
            if prev_n == exam_n - 1:
                prev = re.search(prev_pat, text, re.I)
                break
        q_start = prev.end() if prev else 0
        q_block = text[q_start: sol_m.start()]
        # solutions until next practice exam solutions or EOF
        next_sol = re.search(r"Practice Exam \d solutions", text[sol_m.end():], re.I)
        a_block = text[sol_m.start(): sol_m.end() + (next_sol.start() if next_sol else 2500)]
        keys = parse_answer_block(a_block)
        qs = parse_mcqs(q_block)
        matched = 0
        for qn, q in sorted(qs.items()):
            if qn not in keys:
                continue
            letter = keys[qn]
            ans = "ABCD".index(letter)
            t, sub, kind, diff = pe.classify(q["stem"] + " " + " ".join(q["options"]))
            all_items.append(
                {
                    "id": f"WPE{exam_n}-{qn:03d}",
                    "topic": t,
                    "subtopic": sub,
                    "kind": kind,
                    "difficulty": diff,
                    "question": q["stem"],
                    "options": q["options"],
                    "answer": ans,
                    "explanation": pe.build_explanation(t, letter, q["options"][ans], kind, q["stem"]),
                    "source": f"Workshop Practice Exam {exam_n} Q{qn}",
                    "source_key": letter,
                    "key_corrected": False,
                    "correction_note": None,
                }
            )
            matched += 1
        print(f"WPE{exam_n}: qs={len(qs)} keys={len(keys)} matched={matched}")

    # Deduplicate by id
    by_id = {}
    for item in all_items:
        by_id[item["id"]] = item
    items = list(by_id.values())
    path = OUT / "WB.questions.json"
    path.write_text(json.dumps(items, indent=2, ensure_ascii=False))
    print(f"Wrote {len(items)} -> {path}")


# monkeypatch helper referenced above
def _safe(t):
    return True


pe.SUBTOPICS_SAFE = lambda t: True  # type: ignore

if __name__ == "__main__":
    main()
