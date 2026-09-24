#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


EVALS_DIR = Path(__file__).parent
SKILL_DIR = EVALS_DIR.parent

SENTENCE_SPLIT_RE = re.compile(r"[.!?]+\s+|[.!?]+$")
WORD_RE = re.compile(r"[A-Za-z0-9'-]+")
PASSIVE_RE = re.compile(r"\b(is|are|was|were|be|been|being)\s+[a-zA-Z]+ed\b", re.IGNORECASE)
FENCE_RE = re.compile(r"^```")
TABLE_ROW_RE = re.compile(r"^\s*\|")
EM_DASH_RE = re.compile(r"—")
SPELLED_NUMBER_RE = re.compile(
    r"\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b", re.IGNORECASE
)
NARRATOR_PATTERNS = [
    r"\bin this section\b", r"\bit is worth noting\b", r"\bimportantly\b",
    r"\bsimply\b", r"\bjust\b", r"\beasy\b", r"\bobviously\b",
    r"\bmoreover\b", r"\bthat said\b", r"\bultimately\b",
]

# Deductions per hit. Fog costs more than a formal word because a formal word
# has a replacement and fog stands in for a fact the writer never supplied.
WEIGHTS = {
    "sentence_length": 15,
    "formal_word": 8,
    "fog_word": 12,
    "em_dash": 10,
    "passive": 5,
    "narrator": 5,
    "spelled_number": 3,
}


def parse_words_tables(path: Path) -> tuple[list[str], list[str]]:
    """Left column of every WORDS.md table, split into the formal and fog lists.

    The lists are read from WORDS.md rather than copied into a fixture, so a
    word added to the skill is scored without a second edit here.
    """
    formal, fog, in_fog = [], [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_fog = line.strip() == "## Fog"
            continue
        if not TABLE_ROW_RE.match(line) or set(line.strip()) <= set("|-: "):
            continue
        cell = line.strip().strip("|").split("|")[0].strip()
        if not cell or cell.lower() in ("formal", "fog"):
            continue
        for term in cell.split(","):
            term = re.sub(r"\s*\([^)]*\)", "", term).strip().lower()
            if term:
                (fog if in_fog else formal).append(term)
    return sorted(set(formal)), sorted(set(fog))


def split_text(text: str) -> tuple[str, str]:
    """Sentence text and vocabulary text.

    A sentence limit cannot apply to a table row, so rows stay out of the first.
    The word rules apply wherever words do, so cell contents go into the second:
    without them, moving a paragraph into a table hides every formal word in it.
    """
    sentences, vocab, in_fence = [], [], False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            continue
        if in_fence or line.strip().startswith("#"):
            continue
        if TABLE_ROW_RE.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cells):
                vocab.extend(cells)
            continue
        sentences.append(line)
        vocab.append(line)
    return "\n".join(sentences), "\n".join(vocab)


def split_sentences(text: str) -> list[str]:
    return [p.strip() for p in SENTENCE_SPLIT_RE.split(text.strip()) if p.strip()]


def count_words(sentence: str) -> int:
    return len(WORD_RE.findall(sentence))


def find_terms(text: str, terms: list[str]) -> list[str]:
    lower = text.lower()
    found = [
        term for term in terms
        if (term in lower if " " in term else re.search(rf"\b{re.escape(term)}\b", lower))
    ]
    return sorted(set(found))


def find_patterns(text: str, patterns: list[str]) -> list[str]:
    return [p for p in patterns if re.search(p, text, re.IGNORECASE)]


def evaluate_case(case: dict, output: str, formal: list[str], fog: list[str]) -> dict:
    sentence_text, vocab_text = split_text(output)
    limit = int(case["max_words_per_sentence"])

    hits = {
        "sentence_length": [
            {"words": count_words(s), "sentence": s}
            for s in split_sentences(sentence_text) if count_words(s) > limit
        ],
        "formal_word": find_terms(vocab_text, formal),
        "fog_word": find_terms(vocab_text, fog),
        "em_dash": EM_DASH_RE.findall(vocab_text),
        "passive": PASSIVE_RE.findall(vocab_text),
        "narrator": find_patterns(vocab_text, NARRATOR_PATTERNS),
        "spelled_number": SPELLED_NUMBER_RE.findall(vocab_text),
    }

    missing = [
        p for p in case.get("required_patterns", [])
        if not re.search(p, output, re.IGNORECASE)
    ]

    score = 100 - sum(WEIGHTS[k] * len(v) for k, v in hits.items())
    # A dropped fact is not a style gradient. Over-correction is the failure
    # mode this guards, so it floors the case rather than shaving the score.
    if missing:
        score = 0

    return {"score": max(score, 0), "hits": hits, "missing_required": missing}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run dry-prose evals.")
    parser.add_argument("--cases", default=EVALS_DIR / "cases" / "cases.json", type=Path)
    parser.add_argument("--words", default=SKILL_DIR / "WORDS.md", type=Path)
    parser.add_argument("--outputs", default=EVALS_DIR / "outputs", type=Path)
    args = parser.parse_args()

    formal, fog = parse_words_tables(args.words)
    cases = json.loads(args.cases.read_text(encoding="utf-8"))

    total, scored = 0, 0
    for case in cases:
        path = args.outputs / f"{case['id']}.md"
        if not path.exists():
            print(f"[MISS] {case['id']}: no output at {path}")
            continue

        result = evaluate_case(case, path.read_text(encoding="utf-8"), formal, fog)
        total += result["score"]
        scored += 1

        print(f"[CASE] {case['id']}  score: {result['score']}/100")
        for name, found in result["hits"].items():
            if not found:
                continue
            if name == "sentence_length":
                for hit in found:
                    print(f"  over {case['max_words_per_sentence']} words ({hit['words']}): {hit['sentence'][:70]}")
            else:
                print(f"  {name}: {len(found)} — {', '.join(str(f) for f in found[:6])}")
        for pattern in result["missing_required"]:
            print(f"  MISSING REQUIRED: {pattern}")

    if not scored:
        print("\nNo case was scored.")
        return 1

    print(f"\n[SUMMARY] scored {scored} case(s)")
    print(f"[SUMMARY] average score: {total / scored:.1f}/100")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
