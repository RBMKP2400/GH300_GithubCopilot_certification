import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


DOMAIN_ATTR_RE = re.compile(r'data-domain="([^"]*)"', re.IGNORECASE)
QUESTION_NUM_RE = re.compile(r'Question\s+(\d+)', re.IGNORECASE)


@dataclass
class QuestionItem:
    number: int
    domain: str
    text: str
    options: List[str]


@dataclass
class ExplanationItem:
    number: int
    domain: str
    explanation_md: str


def clean_html_text(raw_html: str) -> str:
    if not raw_html:
        return ""
    # Remove HTML tags
    cleantext = re.sub(re.compile(r"<.*?>", re.DOTALL), "", raw_html)
    cleantext = html.unescape(cleantext)
    cleantext = re.sub(r"\s+", " ", cleantext).strip()
    return cleantext


def clean_inline_html(s: str) -> str:
    s = html.unescape(s or "")
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _strip_outer_whitespace_lines(text: str) -> str:
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def html_fragment_to_markdown(fragment: str) -> str:
    if not fragment:
        return ""

    s = html.unescape(fragment)

    # Images -> markdown image
    s = re.sub(
        r'<img[^>]*?src="([^"]+)"[^>]*?>',
        lambda m: f"![]({m.group(1)})",
        s,
        flags=re.IGNORECASE,
    )

    # Links -> markdown links
    s = re.sub(
        r'<a\s+[^>]*?href="([^"]+)"[^>]*>(.*?)</a>',
        lambda m: f"[{clean_inline_html(m.group(2))}]({m.group(1)})",
        s,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Basic block structure
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</p\s*>", "\n\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<p\b[^>]*>", "", s, flags=re.IGNORECASE)

    # Lists
    s = re.sub(r"<li\b[^>]*>", "- ", s, flags=re.IGNORECASE)
    s = re.sub(r"</li\s*>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</?(ul|ol)\b[^>]*>", "\n", s, flags=re.IGNORECASE)

    # Bold
    s = re.sub(r"</?strong\b[^>]*>", "**", s, flags=re.IGNORECASE)

    # Drop any remaining tags
    s = re.sub(r"<[^>]+>", "", s)

    # Normalize whitespace while preserving newlines
    lines: List[str] = []
    for line in s.splitlines():
        normalized = re.sub(r"\s+", " ", line).strip()
        if normalized in {"**", "****"}:
            continue
        lines.append(normalized)

    # Collapse excessive blank lines
    out_lines: List[str] = []
    blank_run = 0
    for line in lines:
        if not line:
            blank_run += 1
        else:
            blank_run = 0
        if blank_run <= 1:
            out_lines.append(line)

    text = _strip_outer_whitespace_lines("\n".join(out_lines))
    text = re.sub(r"\*\*\s*References\s*:\s*\*\*", "**References:**", text, flags=re.IGNORECASE)
    text = re.sub(r"\*\*\s*Reference\s*:\s*\*\*", "**Reference:**", text, flags=re.IGNORECASE)
    return text


def iter_review_answer_blocks(html_text: str) -> List[Tuple[str, str]]:
    parts = re.split(
        r'(<div\s+class="white-box\s+review-answer"[^>]*?>)',
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    blocks: List[Tuple[str, str]] = []
    for i in range(1, len(parts), 2):
        tag = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        blocks.append((tag, body))
    return blocks


def extract_question_number(body: str, fallback: int) -> int:
    m = QUESTION_NUM_RE.search(body)
    return int(m.group(1)) if m else fallback


def extract_domain(tag: str) -> str:
    m = DOMAIN_ATTR_RE.search(tag)
    domain = (m.group(1) if m else "Unknown Domain").strip()
    return domain or "Unknown Domain"


def extract_question_text(body: str) -> str:
    que_block_match = re.search(r'<div\s+class="que"[^>]*>(.*?)</div>', body, re.DOTALL | re.IGNORECASE)
    if not que_block_match:
        return "No question text found"

    raw_que = que_block_match.group(1)
    raw_que = re.sub(r'<span\s+class="que-category"[^>]*>.*?</span>', '', raw_que, flags=re.DOTALL | re.IGNORECASE)
    return clean_html_text(raw_que) or "No question text found"


def extract_options(body: str) -> List[str]:
    options: List[str] = []

    # Match answer blocks with any extra classes (e.g., "answer ", "answer withCheckbox")
    ans_block_match = re.search(r'<div\s+class="answer[^\"]*"[^>]*>(.*?)</div>', body, re.DOTALL | re.IGNORECASE)
    if not ans_block_match:
        return options

    li_matches = re.findall(r'<li.*?>(.*?)</li>', ans_block_match.group(1), re.DOTALL | re.IGNORECASE)
    for li_content in li_matches:
        li_content = re.sub(r'<span>(right|correct)</span>', '', li_content, flags=re.IGNORECASE)
        li_content = re.sub(r'<span.*?>.*?</span>', '', li_content, flags=re.DOTALL | re.IGNORECASE)
        opt_text = clean_html_text(li_content)
        if opt_text:
            options.append(opt_text)

    return options


def extract_explanation_html(body: str) -> str:
    # Anchor the capture to the solution-block that follows explanation-block.
    m = re.search(
        r'<div\s+class="explanation-block"[^>]*>(.*?)<div\s+class="solution-block"',
        body,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not m:
        return ""

    explanation_html = m.group(1)

    inner = re.search(
        r'<div\s+id="explanation_block__id"[^>]*>(.*?)</div>',
        explanation_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return inner.group(1) if inner else explanation_html


def extract_answer_key_from_explanation(body: str) -> List[str]:
    explanation_html = extract_explanation_html(body)
    if not explanation_html:
        return []

    # Examples we want to handle:
    # "Correct Answer: B"
    # "Correct Answers: A, B and E"
    # "Correct Answers: A, B, E"
    text = clean_html_text(explanation_html).upper()

    # Only capture the short list right after the colon.
    # This intentionally stops before words like "OPTION" that follow in the explanation.
    m = re.search(
        r'CORRECT\s+ANSWERS?\s*:\s*([A-Z](?:\s*(?:,|AND)\s*[A-Z])*)',
        text,
        flags=re.IGNORECASE,
    )
    if not m:
        return []

    rhs = m.group(1).upper()
    parts = re.split(r'\s*(?:,|AND)\s*', rhs)
    letters = [p.strip() for p in parts if re.fullmatch(r'[A-Z]', p.strip())]
    return sorted(set(letters))


def extract_answer_key_from_answer_list(body: str) -> List[str]:
    ans_block_match = re.search(r'<div\s+class="answer[^\"]*"[^>]*>(.*?)</div>', body, re.DOTALL | re.IGNORECASE)
    if not ans_block_match:
        return []

    li_matches = re.findall(r'<li(.*?)>(.*?)</li>', ans_block_match.group(1), re.DOTALL | re.IGNORECASE)
    correct: Set[str] = set()

    for attrs, content in li_matches:
        attrs_lower = (attrs or "").lower()
        content_lower = (content or "").lower()

        is_correct = False
        if "right" in attrs_lower:
            is_correct = True
        if re.search(r'<span>\s*(right|correct)\s*</span>', content, re.IGNORECASE):
            is_correct = True

        if not is_correct:
            continue

        clean_content = clean_html_text(content)
        m = re.match(r'^([A-Z])\.', clean_content)
        if m:
            correct.add(m.group(1).upper())

    return sorted(correct)


def extract_questions(html_text: str) -> List[QuestionItem]:
    questions: List[QuestionItem] = []

    for idx, (tag, body) in enumerate(iter_review_answer_blocks(html_text), start=1):
        domain = extract_domain(tag)
        qnum = extract_question_number(body, idx)
        qtext = extract_question_text(body)
        options = extract_options(body)
        questions.append(QuestionItem(number=qnum, domain=domain, text=qtext, options=options))

    questions.sort(key=lambda q: q.number)
    return questions


def extract_answers(html_text: str) -> Dict[int, List[str]]:
    answers: Dict[int, List[str]] = {}

    for idx, (_tag, body) in enumerate(iter_review_answer_blocks(html_text), start=1):
        qnum = extract_question_number(body, idx)

        correct = extract_answer_key_from_explanation(body)
        if not correct:
            correct = extract_answer_key_from_answer_list(body)

        answers[qnum] = correct

    return dict(sorted(answers.items(), key=lambda kv: kv[0]))


def extract_explanations(html_text: str) -> List[ExplanationItem]:
    items: List[ExplanationItem] = []

    for idx, (tag, body) in enumerate(iter_review_answer_blocks(html_text), start=1):
        domain = extract_domain(tag)
        qnum = extract_question_number(body, idx)
        explanation_html = extract_explanation_html(body)
        explanation_md = html_fragment_to_markdown(explanation_html)
        items.append(ExplanationItem(number=qnum, domain=domain, explanation_md=explanation_md))

    items.sort(key=lambda i: i.number)
    return items


def render_questions_md(questions: List[QuestionItem]) -> str:
    out: List[str] = []
    for q in questions:
        out.append(f"### Domain: {q.domain}")
        out.append(f"### Question {q.number}: {q.text}")
        for opt in q.options:
            out.append(f"#### [ ] {opt}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_answers_md(answers: Dict[int, List[str]]) -> str:
    out: List[str] = []
    for qnum in sorted(answers.keys()):
        choices = ", ".join(answers[qnum]) if answers[qnum] else ""
        out.append(f"{qnum}. {choices}".rstrip())
    return "\n".join(out).rstrip() + "\n"


def render_explanations_md(items: List[ExplanationItem]) -> str:
    out: List[str] = []
    for item in items:
        out.append(f"### Domain: {item.domain}")
        out.append(f"### Question {item.number}")
        out.append(item.explanation_md if item.explanation_md else "(No explanation found.)")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract questions, answers, and explanations from a Whizlabs-style HTML review page."
    )
    parser.add_argument(
        "input_html",
        help="Path to the input HTML file (e.g., test_1.html)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    input_path = Path(args.input_html)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}")
        return 1

    if input_path.suffix.lower() not in {".html", ".htm"}:
        print(f"Error: input must be an .html/.htm file: {input_path}")
        return 1

    html_text = input_path.read_text(encoding="utf-8")

    base = input_path.stem

    # Prefer <repo_root> when this script lives in <repo_root>/src.
    repo_root = Path(__file__).resolve().parent.parent

    # Write questions into the repo root (not alongside the input HTML).
    questions_out = repo_root / f"{base}_questions.md"

    # Write answers + explanations into the repo's docs/ folder.
    docs_dir = repo_root / "docs"
    if not docs_dir.exists():
        # Fallback to CWD to support running from a different layout
        docs_dir = Path.cwd() / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    answers_out = docs_dir / f"{base}_answers.md"
    explanations_out = docs_dir / f"{base}_explanations.md"

    questions = extract_questions(html_text)
    answers = extract_answers(html_text)
    explanations = extract_explanations(html_text)

    questions_out.write_text(render_questions_md(questions), encoding="utf-8")
    answers_out.write_text(render_answers_md(answers), encoding="utf-8")
    explanations_out.write_text(render_explanations_md(explanations), encoding="utf-8")

    print(f"Wrote {questions_out}")
    print(f"Wrote {answers_out}")
    print(f"Wrote {explanations_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
