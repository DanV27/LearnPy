"""
Loader for hand-authored lesson Markdown files in `lessons/`.

Each lesson is a Markdown file named `<slug>.md` with a tiny YAML-style
frontmatter block at the top:

    ---
    title: Python Basics
    summary: Variables, types, control flow.
    related: data-structures, file-io
    ---

    ## Variables
    ...rest of the markdown body...

The body can contain any GitHub-flavored markdown. The first ```python ...```
fenced block is automatically extracted as the lesson's primary code snippet
(used for Copy / Export buttons).

To add a new lesson: drop a new `.md` file in `lessons/` and add a matching
entry to `topics.py` so it appears in the sidebar.
"""

import re
from pathlib import Path

LESSONS_DIR = Path(__file__).parent / "lessons"


def _parse_frontmatter(text: str):
    """Split a markdown file into (metadata dict, body str). Returns (None, text) if no frontmatter."""
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    fm_text, body = parts[1], parts[2]
    meta = {}
    for raw in fm_text.splitlines():
        line = raw.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip().lower()] = value.strip()
    return meta, body.lstrip("\n")


def _extract_code(body: str) -> str:
    """Pull the first ```python ...``` fenced block out of the body."""
    m = re.search(r"```python\s*\n(.*?)\n```", body, re.DOTALL)
    return m.group(1).strip() if m else ""


def load_lesson(slug: str):
    """Return the lesson dict for a slug, or None if no file exists."""
    path = LESSONS_DIR / f"{slug}.md"
    if not path.is_file():
        return None

    text = path.read_text(encoding="utf-8")
    meta, body = _parse_frontmatter(text)
    meta = meta or {}

    related_slugs = [
        s.strip() for s in (meta.get("related") or "").split(",") if s.strip()
    ]

    return {
        "title": meta.get("title", slug.replace("-", " ").title()),
        "summary": meta.get("summary", ""),
        "lesson_markdown": body.strip(),
        "code": _extract_code(body),
        # Resolved (label + url) by the route handler using the topics catalog.
        "related_slugs": related_slugs,
    }
