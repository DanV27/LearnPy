"""
LearnPy's only AI entry point.

`generate_lesson(spec)` is called by the `/generate` Flask endpoint whenever
a user types into the free-form search bar. It sends one request to Claude
asking for a short Python lesson and returns it as a structured dict.

Hand-authored canonical lessons (the ones in the sidebar) live in
`lessons/*.md` and are loaded by `lessons.py` — they never hit this module.
"""

import json
import re
import anthropic


# Claude model used for lesson generation. Bump this when a newer model
# is released and you want users to benefit from it.
MODEL = "claude-opus-4-6"
MAX_TOKENS = 2048


def generate_lesson(spec: str) -> dict:
    """Ask Claude for a short Python lesson on `spec` and return it as a dict.

    Returns a dict shaped like:
        {
            "title":           "Short title",
            "summary":         "One- or two-sentence intro",
            "lesson_markdown": "Full markdown body, includes a ```python``` block",
            "code":            "The primary code snippet as plain Python",
            "related_topics":  [{"label": "...", "prompt": "..."}, ...]
        }

    If Claude returns malformed JSON, the whole response is exposed as
    `lesson_markdown` and the other fields get sensible defaults so the UI
    can still render something useful.
    """
    client = anthropic.Anthropic()

    prompt = f"""You are a friendly Python tutor writing a SHORT lesson on a single topic.

Topic: {spec}

Write a focused, beginner-friendly Python lesson. Your output MUST be a single
valid JSON object — no prose before or after — with EXACTLY these fields:

{{
  "title": "Short topic title, max ~60 chars",
  "summary": "One or two plain-text sentences introducing the topic.",
  "lesson_markdown": "Full lesson body in GitHub-flavored markdown. Should include: a short explanation, a working Python code example in a ```python fenced block, and a few bullet points about how it works. Keep the whole lesson under ~400 words. You may include inline cross-references to related Python topics using the syntax [topic name](#topic:Full prompt for that topic) — these will become clickable links in the UI.",
  "code": "The primary Python code example as PLAIN Python (no markdown fencing). Must be the same code shown in the lesson_markdown.",
  "related_topics": [
    {{"label": "Short topic name", "prompt": "Full search prompt for that topic"}},
    {{"label": "Short topic name", "prompt": "Full search prompt for that topic"}},
    {{"label": "Short topic name", "prompt": "Full search prompt for that topic"}}
  ]
}}

Rules:
- Output ONLY the JSON object. No prose, no markdown fencing around the JSON itself.
- Include 3 to 4 related_topics that flow naturally from this lesson.
- Code must be valid Python 3.9+ with type hints where useful.
"""

    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()

    # Claude sometimes wraps its JSON in a markdown code fence even when
    # asked not to. Strip those off so json.loads doesn't choke.
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: the model didn't return valid JSON. Surface whatever
        # it sent as markdown so the user still sees something useful.
        return {
            "title": spec[:60],
            "summary": "",
            "lesson_markdown": raw,
            "code": _extract_first_python_block(raw),
            "related_topics": [],
        }

    # Defensive normalization — guarantee the shape regardless of model drift.
    # Each field is coerced to the right type and clamped to a reasonable size.
    return {
        "title": (data.get("title") or spec)[:120],
        "summary": data.get("summary") or "",
        "lesson_markdown": data.get("lesson_markdown") or "",
        "code": data.get("code") or _extract_first_python_block(data.get("lesson_markdown") or ""),
        "related_topics": [
            {
                "label": str(t.get("label", ""))[:80],
                "prompt": str(t.get("prompt", ""))[:300],
            }
            for t in (data.get("related_topics") or [])
            if isinstance(t, dict) and t.get("label")
        ][:6],
    }


def _extract_first_python_block(markdown: str) -> str:
    """Pull the first ```python ...``` fenced block out of a markdown body.

    Used as a fallback when Claude forgets to populate the `code` field
    separately — we just lift the code out of the lesson body instead.
    """
    m = re.search(r"```python\s*\n(.*?)\n```", markdown, re.DOTALL)
    return m.group(1).strip() if m else ""
