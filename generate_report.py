import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


@dataclass
class QuestionSelections:
    number: int
    domain: str
    selected: Set[str]


_MARK_RE = re.compile(r"^####\s*\[\s*([^\]]*)\]\s*([A-Za-z])\.")
_DOMAIN_RE = re.compile(r"^###\s*Domain:\s*(.*)\s*$")
_QUESTION_RE = re.compile(r"^###\s*Question\s+(\d+)\s*:\s*(.*)$")


def _is_marked(bracket_content: str) -> bool:
    # Accept: [x], [x ], [ x], [ x ], [X], [ X ], etc.
    return re.search(r"[xX]", bracket_content or "") is not None


def parse_questions_md(path: Path) -> Dict[int, QuestionSelections]:
    current_domain = "Unknown Domain"
    current_qnum: Optional[int] = None

    selections: Dict[int, QuestionSelections] = {}

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")

        domain_match = _DOMAIN_RE.match(line)
        if domain_match:
            domain_value = (domain_match.group(1) or "").strip()
            current_domain = domain_value if domain_value else "Unknown Domain"
            continue

        question_match = _QUESTION_RE.match(line)
        if question_match:
            current_qnum = int(question_match.group(1))
            selections[current_qnum] = QuestionSelections(
                number=current_qnum,
                domain=current_domain,
                selected=set(),
            )
            continue

        mark_match = _MARK_RE.match(line)
        if mark_match and current_qnum is not None:
            bracket_content = mark_match.group(1)
            option_letter = mark_match.group(2).upper()
            if _is_marked(bracket_content):
                selections[current_qnum].selected.add(option_letter)

    return selections


def parse_answers_md(path: Path) -> Dict[int, Set[str]]:
    answers: Dict[int, Set[str]] = {}

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # Example formats:
        # 1. B
        # 5. A, B, E
        m = re.match(r"^(\d+)\s*\.\s*(.*)$", line)
        if not m:
            continue

        qnum = int(m.group(1))
        rhs = (m.group(2) or "").strip()
        letters = [p.strip().upper() for p in rhs.split(",") if p.strip()]
        # Keep only single-letter A-Z tokens
        answers[qnum] = {l for l in letters if re.fullmatch(r"[A-Z]", l)}

    return answers


def _fmt_list(nums: List[int]) -> str:
    return ", ".join(str(n) for n in nums) if nums else "-"


def compute_stats(
    selections: Dict[int, QuestionSelections],
    answer_key: Dict[int, Set[str]],
) -> Tuple[Dict[str, dict], dict]:
    # Per-domain stats + overall stats
    domains: Dict[str, dict] = {}

    all_question_numbers = sorted(set(answer_key.keys()) | set(selections.keys()))

    overall = {
        "total": 0,
        "answered": 0,
        "unanswered": 0,
        "correct": 0,
        "incorrect": 0,
        "missing_in_questions_md": [],  # in key but not in questions.md
        "missing_in_answers_md": [],  # in questions.md but not in key
    }

    for qnum in all_question_numbers:
        overall["total"] += 1

        q = selections.get(qnum)
        correct_set = answer_key.get(qnum)

        if q is None:
            overall["missing_in_questions_md"].append(qnum)
            # If it doesn't exist in questions.md, we can’t grade it.
            continue

        if correct_set is None:
            overall["missing_in_answers_md"].append(qnum)
            # If it doesn't exist in answers.md, we can’t grade it.
            continue

        domain = q.domain or "Unknown Domain"
        if domain not in domains:
            domains[domain] = {
                "total": 0,
                "correct": 0,
                "incorrect_questions": [],
                "unanswered_questions": [],
            }

        domains[domain]["total"] += 1

        if not q.selected:
            overall["unanswered"] += 1
            domains[domain]["unanswered_questions"].append(qnum)
            continue

        overall["answered"] += 1

        if q.selected == correct_set:
            overall["correct"] += 1
            domains[domain]["correct"] += 1
        else:
            overall["incorrect"] += 1
            domains[domain]["incorrect_questions"].append(qnum)

    return domains, overall


def render_report(domains: Dict[str, dict], overall: dict) -> str:
    tz = ZoneInfo("Europe/Madrid") if ZoneInfo else dt.timezone.utc
    timestamp = dt.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S%z")

    lines: List[str] = []
    lines.append(f"# Test Report")
    lines.append(f"")
    lines.append(f"Generated (Europe/Madrid): {timestamp}")
    lines.append(f"")

    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("| --- | ---: |")
    lines.append(f"| Total questions | {overall['total']} |")
    lines.append(f"| Answered | {overall['answered']} |")
    lines.append(f"| Unanswered | {overall['unanswered']} |")
    lines.append(f"| Total correct | {overall['correct']} |")
    lines.append(f"| Total incorrect | {overall['incorrect']} |")
    lines.append("")

    lines.append("## By Domain")
    lines.append("")
    lines.append("| Domain | Total | Correct | Incorrect questions | Unanswered questions |")
    lines.append("| --- | ---: | ---: | --- | --- |")

    for domain in sorted(domains.keys()):
        stats = domains[domain]
        incorrect = _fmt_list(sorted(stats["incorrect_questions"]))
        unanswered = _fmt_list(sorted(stats["unanswered_questions"]))
        lines.append(
            f"| {domain} | {stats['total']} | {stats['correct']} | {incorrect} | {unanswered} |"
        )

    # Optional diagnostics to catch file mismatches
    if overall["missing_in_questions_md"] or overall["missing_in_answers_md"]:
        lines.append("")
        lines.append("## Diagnostics")
        lines.append("")
        if overall["missing_in_questions_md"]:
            lines.append(
                f"- Present in answers.md but missing in questions.md: {_fmt_list(overall['missing_in_questions_md'])}"
            )
        if overall["missing_in_answers_md"]:
            lines.append(
                f"- Present in questions.md but missing in answers.md: {_fmt_list(overall['missing_in_answers_md'])}"
            )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Copilot test report by comparing marked answers in "
            "copilot_test_X_questions.md with copilot_test_X_answers.md, and append "
            "copilot_test_X_explanations.md."
        )
    )
    parser.add_argument(
        "test_number",
        type=int,
        choices=[1, 2],
        help="Which test to grade (1 or 2).",
    )

    args = parser.parse_args()
    test_number = args.test_number
    base = f"copilot_test_{test_number}"

    repo_root = Path(__file__).resolve().parent
    docs_dir = repo_root / "docs"

    def resolve_existing_file(candidates: List[Path], label: str) -> Path:
        for candidate in candidates:
            if candidate.exists():
                return candidate
        searched = "\n".join(f"- {c}" for c in candidates)
        raise SystemExit(f"{label} file not found. Looked in:\n{searched}")

    questions_path = resolve_existing_file(
        [repo_root / f"{base}_questions.md", docs_dir / f"{base}_questions.md"],
        "questions",
    )
    answers_path = resolve_existing_file(
        [docs_dir / f"{base}_answers.md", repo_root / f"{base}_answers.md"],
        "answers",
    )
    explanations_path = resolve_existing_file(
        [docs_dir / f"{base}_explanations.md", repo_root / f"{base}_explanations.md"],
        "explanations",
    )

    out_path = repo_root / f"{base}_report.md"

    selections = parse_questions_md(questions_path)
    answer_key = parse_answers_md(answers_path)

    domains, overall = compute_stats(selections, answer_key)
    report = render_report(domains, overall)

    explanations_md = explanations_path.read_text(encoding="utf-8")
    combined = (
        report.rstrip()
        + "\n\n## Explanations\n\n"
        + explanations_md.strip()
        + "\n"
    )
    out_path.write_text(combined, encoding="utf-8")

    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
