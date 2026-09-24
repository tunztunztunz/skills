#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


COMMENT_LINE_RE = re.compile(r"^\s*(?://|#|/\*|\*)")
INLINE_COMMENT_RE = re.compile(r"//|(?<!\S)#")
EVALS_DIR = Path(__file__).parent


def load_cases(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def count_comment_lines(text: str) -> int:
    return sum(
        bool(INLINE_COMMENT_RE.search(line) or COMMENT_LINE_RE.match(line))
        for line in text.splitlines()
    )


def load_patterns(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def source_comment_text(output: str) -> str:
    comments = []
    for line in output.splitlines():
        if "//" in line:
            comments.append(line.split("//", 1)[1])
        elif "#" in line:
            comments.append(line.split("#", 1)[1])
        elif COMMENT_LINE_RE.match(line):
            comments.append(line)
    comments.extend(re.findall(r"/\*(.*?)\*/", output, re.DOTALL))
    return "\n".join(comments)


def evaluate_case(case: dict, output: str, banned_patterns: list[str]) -> list[str]:
    failures = []
    for pattern in case.get("required_patterns", []):
        if not re.search(pattern, output, re.IGNORECASE):
            failures.append(f"missing required pattern: {pattern}")
    for pattern in case.get("forbidden_patterns", []):
        if re.search(pattern, output, re.IGNORECASE):
            failures.append(f"found forbidden pattern: {pattern}")
    if "comment_line_limit" in case:
        count = count_comment_lines(output)
        limit = case["comment_line_limit"]
        if count > limit:
            failures.append(f"comment lines: {count}, limit: {limit}")
    if case.get("check_banned_comment_text"):
        comment_text = source_comment_text(output)
        for pattern in banned_patterns:
            if re.search(pattern, comment_text, re.IGNORECASE):
                failures.append(f"found banned comment text: {pattern}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Run code-comments evals.")
    parser.add_argument("--cases", default=EVALS_DIR / "cases" / "cases.json", type=Path)
    parser.add_argument(
        "--banned-patterns",
        default=EVALS_DIR / "fixtures" / "banned-comment-patterns.txt",
        type=Path,
    )
    parser.add_argument("--outputs", default=EVALS_DIR / "outputs", type=Path)
    args = parser.parse_args()

    cases = load_cases(args.cases)
    banned_patterns = load_patterns(args.banned_patterns)
    outputs = args.outputs
    failures = 0

    for case in cases:
        output_path = outputs / f"{case['id']}.md"
        if not output_path.exists():
            print(f"[FAIL] {case['id']}: output not found at {output_path}")
            failures += 1
            continue
        result = evaluate_case(
            case, output_path.read_text(encoding="utf-8"), banned_patterns
        )
        if result:
            print(f"[FAIL] {case['id']}")
            for failure in result:
                print(f"  - {failure}")
            failures += 1
        else:
            print(f"[PASS] {case['id']}")

    print(f"\n[SUMMARY] {len(cases) - failures}/{len(cases)} cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
