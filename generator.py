"""
LearnPy's only AI entry point.

`generate_lesson(spec)` is called by the `/generate` Flask endpoint whenever
a user types into the free-form search bar. It sends one request to Claude
asking for a short Python lesson and returns it as a structured dict.

This module is now RAG-augmented: before calling Claude we retrieve the top
canonical lesson matches from the FTS index (see search_index.py). Those
matches get folded into the prompt as context AND merged into the result's
`related_topics` as real navigation links, so AI-generated lessons stay
coherent with the hand-authored catalog.

Hand-authored canonical lessons (the ones in the sidebar) live in
`lessons/*.md` and are loaded by `lessons.py` — they never hit this module.
"""

import json
import re
import anthropic

from search_index import search as _search_catalog


# Claude model used for lesson generation. Bump this when a newer model
# is released and you want users to benefit from it.
MODEL = "claude-opus-4-6"
MAX_TOKENS = 2048

# How many canonical matches to pull from the FTS index and feed into
# Claude's context. Three is enough to ground without overwhelming.
RAG_TOP_K = 3


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

    Some entries in `related_topics` will have a `url` field when they
    correspond to canonical lessons — those render as direct navigation
    links instead of "ask AI again" buttons.

    If Claude returns malformed JSON, the whole response is exposed as
    `lesson_markdown` and the other fields get sensible defaults so the UI
    can still render something useful.
    """
    client = anthropic.Anthropic()

    # ---- Retrieval step: pull canonical matches from the FTS index. ----
    # The autocomplete uses the raw query because users type short
    # fragments. Free-form questions ("How do hash maps work?") need their
    # question words stripped so the AND-semantics of FTS doesn't reject
    # everything. _retrieval_query() does that.
    try:
        retrieval_q = _retrieval_query(spec)
        canonical_matches = _search_catalog(retrieval_q, limit=RAG_TOP_K) or []
    except Exception:
        canonical_matches = []

    context_block = _build_context_block(canonical_matches)

    # ---- Augmented prompt. ----
    prompt = f"""You are a friendly Python tutor writing a SHORT lesson on a single topic.

Topic: {spec}
{context_block}

Write a focused, beginner-friendly Python lesson. Your output MUST be a single
valid JSON object — no prose before or after — with EXACTLY these fields:

{{
  "title": "Short topic title, max ~60 chars",
  "summary": "One or two plain-text sentences introducing the topic.",
  "lesson_markdown": "Full lesson body in GitHub-flavored markdown. Should include: a short explanation, a working Python code example in a ```python fenced block, and a few bullet points about how it works. Keep the whole lesson under ~400 words. When relevant, reference the existing LearnPy lessons listed above by name AND use their URLs as inline markdown links — like [Binary Search](/lesson/binary-search). This makes the lesson feel coherent with the rest of the site.",
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
- If any of the LearnPy lessons listed above are directly relevant, prefer linking to them in the body over inventing your own concepts.
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
            # Even on JSON failure we still expose the canonical matches
            # so the user has somewhere useful to click.
            "related_topics": _canonical_as_related(canonical_matches),
        }

    # Defensive normalization — guarantee the shape regardless of model drift.
    # Each field is coerced to the right type and clamped to a reasonable size.
    ai_related = [
        {
            "label": str(t.get("label", ""))[:80],
            "prompt": str(t.get("prompt", ""))[:300],
        }
        for t in (data.get("related_topics") or [])
        if isinstance(t, dict) and t.get("label")
    ]

    # Merge canonical matches (with real URLs) FIRST, then dedupe by lowercased
    # label so we don't show "Binary Search" twice. Canonical matches always
    # win because they have direct URLs — the AI's invented topics fall in
    # behind them as "ask AI" buttons.
    merged_related = _merge_related(_canonical_as_related(canonical_matches), ai_related)

    return {
        "title": (data.get("title") or spec)[:120],
        "summary": data.get("summary") or "",
        "lesson_markdown": data.get("lesson_markdown") or "",
        "code": data.get("code") or _extract_first_python_block(data.get("lesson_markdown") or ""),
        "related_topics": merged_related[:6],
    }


# ---------------------------------------------------------------------------
# RAG helpers
# ---------------------------------------------------------------------------

# Very small stopword list — just question words and connectors that show
# up in "how do I" / "what is" style prompts. We deliberately keep this
# tight so we don't strip real Python topic words.
_QUESTION_STOPWORDS = {
    "how", "do", "does", "did", "what", "why", "when", "where", "which",
    "is", "are", "was", "were", "be", "been",
    "the", "a", "an", "of", "in", "on", "for", "with", "and", "or", "to",
    "me", "my", "i", "you", "your", "this", "that",
    "about", "can", "could", "should", "would", "will",
}


def _retrieval_query(spec: str) -> str:
    """Trim question/connector words from a free-form prompt so the FTS
    AND-semantics has a chance of hitting. Returns the original spec if
    the strip leaves nothing useful behind.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", " ", spec).lower()
    kept = [w for w in cleaned.split() if w not in _QUESTION_STOPWORDS and len(w) > 1]
    return " ".join(kept) if kept else spec


def _build_context_block(matches: list) -> str:
    """Format the retrieved canonical matches as a markdown bullet list that
    Claude can lean on. Empty string when nothing matched.
    """
    if not matches:
        return ""
    lines = ["", "## Existing LearnPy lessons relevant to this query:"]
    for m in matches:
        name = m.get("name", "")
        url = m.get("url", "")
        desc = m.get("description", "")
        lines.append(f"- [{name}]({url}) — {desc}")
    lines.append("")
    return "\n".join(lines)


def _canonical_as_related(matches: list) -> list:
    """Turn search hits into related_topics shaped for the frontend.

    Each entry has both `label` and `url` — the frontend recognizes the
    `url` field and renders these as real <a> chips instead of "ask the
    AI again" buttons.
    """
    return [
        {"label": m.get("name", ""), "url": m.get("url", "")}
        for m in matches
        if m.get("name") and m.get("url")
    ]


def _merge_related(canonical: list, ai_generated: list) -> list:
    """Combine the two related-topics lists, deduping by lowercased label.

    Canonical entries come first so URL-backed chips always win over the
    AI's invented "search again" buttons when they refer to the same topic.
    """
    seen = set()
    merged = []
    for t in canonical + ai_generated:
        label = (t.get("label") or "").strip().lower()
        if not label or label in seen:
            continue
        seen.add(label)
        merged.append(t)
    return merged


def _extract_first_python_block(markdown: str) -> str:
    """Pull the first ```python ...``` fenced block out of a markdown body.

    Used as a fallback when Claude forgets to populate the `code` field
    separately — we just lift the code out of the lesson body instead.
    """
    m = re.search(r"```python\s*\n(.*?)\n```", markdown, re.DOTALL)
    return m.group(1).strip() if m else ""
