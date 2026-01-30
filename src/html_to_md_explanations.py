import re
import html
from pathlib import Path
from typing import List, Optional, Tuple


DOMAIN_ATTR_RE = re.compile(r'data-domain="([^"]*)"', re.IGNORECASE)
QUESTION_NUM_RE = re.compile(r'Question\s+(\d+)', re.IGNORECASE)


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
    s = re.sub(r'<br\s*/?>', "\n", s, flags=re.IGNORECASE)
    s = re.sub(r'</p\s*>', "\n\n", s, flags=re.IGNORECASE)
    s = re.sub(r'<p\b[^>]*>', "", s, flags=re.IGNORECASE)

    # Lists
    s = re.sub(r'<li\b[^>]*>', "- ", s, flags=re.IGNORECASE)
    s = re.sub(r'</li\s*>', "\n", s, flags=re.IGNORECASE)
    s = re.sub(r'</?(ul|ol)\b[^>]*>', "\n", s, flags=re.IGNORECASE)

    # Bold
    s = re.sub(r'</?strong\b[^>]*>', "**", s, flags=re.IGNORECASE)

    # Drop any remaining tags
    s = re.sub(r'<[^>]+>', '', s)

    # Normalize whitespace while preserving newlines
    lines: List[str] = []
    for line in s.splitlines():
        normalized = re.sub(r'\s+', ' ', line).strip()
        # Drop lines that are only bold markers (often produced by <strong><br></strong>)
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
    # Normalize common headings
    text = re.sub(r'\*\*\s*References\s*:\s*\*\*', '**References:**', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*\s*Reference\s*:\s*\*\*', '**Reference:**', text, flags=re.IGNORECASE)
    return text


def clean_inline_html(s: str) -> str:
    # Used for link text extraction; keep it single-line
    s = html.unescape(s or "")
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def extract_explanation_block(block: str) -> str:
    # Anchor the capture to the solution-block that follows explanation-block.
    m = re.search(
        r'<div\s+class="explanation-block"[^>]*>(.*?)<div\s+class="solution-block"',
        block,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not m:
        return ""

    explanation_html = m.group(1)

    # Prefer the inner explanation content div if present.
    inner = re.search(
        r'<div\s+id="explanation_block__id"[^>]*>(.*?)</div>',
        explanation_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return inner.group(1) if inner else explanation_html


def iter_question_blocks(html_text: str) -> List[Tuple[str, str]]:
    # Split while keeping the opening tag so we can read attributes.
    parts = re.split(r'(<div\s+class="white-box\s+review-answer"[^>]*?>)', html_text, flags=re.IGNORECASE | re.DOTALL)
    blocks: List[Tuple[str, str]] = []
    for i in range(1, len(parts), 2):
        tag = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        blocks.append((tag, body))
    return blocks


def extract_explanations(input_file: Path) -> List[dict]:
    content = input_file.read_text(encoding="utf-8")

    results: List[dict] = []

    for idx, (tag, body) in enumerate(iter_question_blocks(content), start=1):
        domain_match = DOMAIN_ATTR_RE.search(tag)
        domain = (domain_match.group(1) if domain_match else "Unknown Domain").strip() or "Unknown Domain"

        qnum_match = QUESTION_NUM_RE.search(body)
        qnum = int(qnum_match.group(1)) if qnum_match else idx

        explanation_html = extract_explanation_block(body)
        explanation_md = html_fragment_to_markdown(explanation_html)

        results.append(
            {
                "number": qnum,
                "domain": domain,
                "explanation": explanation_md,
            }
        )

    # Sort by question number if they were found
    results.sort(key=lambda r: r["number"])
    return results


def to_markdown(items: List[dict]) -> str:
    out: List[str] = []
    for item in items:
        out.append(f"### Domain: {item['domain']}")
        out.append(f"### Question {item['number']}")
        if item["explanation"]:
            out.append(item["explanation"])
        else:
            out.append("(No explanation found.)")
        out.append("")
    return "\n".join(out).strip() + "\n"


def main() -> int:
    input_path = Path("questions.html")
    output_path = Path("explanations.md")

    if not input_path.exists():
        print(f"Error: File '{input_path}' not found.")
        return 1

    items = extract_explanations(input_path)
    output_path.write_text(to_markdown(items), encoding="utf-8")
    print(f"Successfully exported to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
