"""Extract text from the ACI source PDFs into source_text/ for authoring the question bank."""
import hashlib
import pathlib
import sys

import fitz

SRC = pathlib.Path.home() / "Downloads" / "ACI"
OUT = pathlib.Path(__file__).resolve().parent.parent / "source_text"
OUT.mkdir(exist_ok=True)

seen = {}
for pdf in sorted(SRC.glob("*.pdf")):
    digest = hashlib.md5(pdf.read_bytes()).hexdigest()
    if digest in seen:
        print(f"DUPLICATE {pdf.name} == {seen[digest]}")
        continue
    seen[digest] = pdf.name
    doc = fitz.open(pdf)
    parts = []
    empty = 0
    for i, page in enumerate(doc):
        t = page.get_text()
        if len(t.strip()) < 20:
            empty += 1
        parts.append(f"\n===== PAGE {i + 1} =====\n{t}")
    text = "".join(parts)
    (OUT / (pdf.stem + ".txt")).write_text(text)
    print(f"{pdf.name}: pages={len(doc)} chars={len(text)} near_empty_pages={empty}")
sys.exit(0)
