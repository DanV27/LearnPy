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
from stream_utils import DelimiterSplitter
from topic_resolver import resolve_topic, get_canonical_name


# Claude model used for lesson generation. Bump this when a newer model
# is released and you want users to benefit from it.
MODEL = "claude-opus-4-6"
MAX_TOKENS = 2048

# How many canonical matches to pull from the FTS index and feed into
# Claude's context. Three is enough to ground without overwhelming.
RAG_TOP_K = 3


def _build_catalog_listing() -> str:
    """One-time compact listing of all catalog lessons for the Claude prompt."""
    from topics import TOPICS
    lines = ["", "## Full LearnPy catalog (use these slugs in related_topics):"]
    for t in TOPICS:
        lines.append(f"- {t['name']} (slug: {t['slug']})")
    lines.append("")
    return "\n".join(lines)


# Built once at import — referenced in both prompt builders below.
_CATALOG_LISTING = _build_catalog_listing()


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
{context_block}{_CATALOG_LISTING}
Write a focused, beginner-friendly Python lesson. Your output MUST be a single
valid JSON object — no prose before or after — with EXACTLY these fields:

{{
  "title": "Short topic title, max ~60 chars",
  "summary": "One or two plain-text sentences introducing the topic.",
  "lesson_markdown": "Full lesson body in GitHub-flavored markdown. Include: a short explanation, a working Python code example in a ```python fenced block, and bullet points about how it works. Keep under ~400 words. Link to relevant catalog lessons using their URLs: [Binary Search](/lesson/binary-search).",
  "code": "The primary Python code example as PLAIN Python (no markdown fencing). Same code as in lesson_markdown.",
  "related_topics": [
    {{"title": "Exact catalog lesson name OR invented title", "slug": "exact-catalog-slug-or-null"}},
    {{"title": "Exact catalog lesson name OR invented title", "slug": "exact-catalog-slug-or-null"}},
    {{"title": "Exact catalog lesson name OR invented title", "slug": "exact-catalog-slug-or-null"}}
  ]
}}

Rules for related_topics:
- PREFER existing catalog lessons. Look up the full catalog listing above.
- For catalog lessons, set slug to the EXACT slug from the catalog (e.g. "binary-search").
- For topics NOT in the catalog, set slug to null.
- Include 3–4 entries. No duplicates.
- Output ONLY the JSON. No prose, no markdown fencing around the JSON itself.
- Code must be valid Python 3.9+.
"""

    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "title": spec[:60],
            "summary": "",
            "lesson_markdown": raw,
            "code": _extract_first_python_block(raw),
            "related_topics": _canonical_as_related(canonical_matches),
        }

    ai_related = _resolve_related_topics(data.get("related_topics") or [])

    merged_related = _merge_related(_canonical_as_related(canonical_matches), ai_related)

    return {
        "title": (data.get("title") or spec)[:120],
        "summary": data.get("summary") or "",
        "lesson_markdown": data.get("lesson_markdown") or "",
        "code": data.get("code") or _extract_first_python_block(data.get("lesson_markdown") or ""),
        "related_topics": merged_related[:6],
    }


def stream_lesson_chunks(spec: str):
    """Generator that yields streaming events for a lesson on ``spec``.

    Each yielded item is a dict with a ``"type"`` key:

    * ``{"type": "text", "text": "..."}``   — markdown body token
    * ``{"type": "meta", "title": "...", "summary": "...", "related_topics": [...]}``
    * ``{"type": "error", "error": "..."}`` — on exception mid-stream

    The output format sent to Claude is different from ``generate_lesson``:
    Claude writes the full markdown lesson body first (with a ```python block
    embedded), then emits the ``<<<META>>>`` delimiter, then a compact JSON
    object with title / summary / related_topics.  This lets us stream the
    lesson body live without waiting for a complete JSON object.
    """
    client = anthropic.Anthropic()

    try:
        retrieval_q = _retrieval_query(spec)
        canonical_matches = _search_catalog(retrieval_q, limit=RAG_TOP_K) or []
    except Exception:
        canonical_matches = []

    context_block = _build_context_block(canonical_matches)

    prompt = f"""You are a friendly Python tutor writing a SHORT lesson on a single topic.

Topic: {spec}
{context_block}{_CATALOG_LISTING}
Output format — follow EXACTLY in this order, nothing else:

PART 1 — Lesson body in GitHub-flavored Markdown:
  - Start with a level-1 heading: # Topic Name
  - One- or two-sentence introduction
  - A working Python code example in a ```python fenced block
  - A few bullet points explaining how it works
  - Keep the whole lesson under ~400 words
  - Link to relevant catalog lessons using their URLs, e.g. [Binary Search](/lesson/binary-search)

PART 2 — This exact delimiter on its own line:
<<<META>>>

PART 3 — Immediately after the delimiter, a single JSON object (no fencing, no prose):
{{
  "title": "Short topic title, max ~60 chars",
  "summary": "One or two plain-text sentences introducing the topic.",
  "related_topics": [
    {{"title": "Exact catalog lesson name OR invented title", "slug": "exact-catalog-slug-or-null"}},
    {{"title": "Exact catalog lesson name OR invented title", "slug": "exact-catalog-slug-or-null"}},
    {{"title": "Exact catalog lesson name OR invented title", "slug": "exact-catalog-slug-or-null"}}
  ]
}}

Rules for related_topics:
- PREFER existing catalog lessons from the listing above.
- For catalog lessons, set slug to the EXACT slug (e.g. "binary-search").
- For topics not in the catalog, set slug to null.
- Include 3–4 entries. No duplicates. Nothing may appear after the JSON.
"""

    splitter = DelimiterSplitter()

    try:
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for chunk in stream.text_stream:
                text_out, _ = splitter.feed(chunk)
                if text_out:
                    yield {"type": "text", "text": text_out}

        remaining_text, meta_str = splitter.finish()
        if remaining_text:
            yield {"type": "text", "text": remaining_text}

        meta_data = {}
        if meta_str:
            # Strip accidental markdown fencing Claude occasionally adds
            clean = re.sub(r"^```[a-zA-Z]*\s*", "", meta_str.strip())
            clean = re.sub(r"\s*```$", "", clean)
            try:
                meta_data = json.loads(clean)
            except json.JSONDecodeError:
                pass

        ai_related = _resolve_related_topics(meta_data.get("related_topics") or [])
        merged_related = _merge_related(_canonical_as_related(canonical_matches), ai_related)

        yield {
            "type": "meta",
            "title": (meta_data.get("title") or spec)[:120],
            "summary": meta_data.get("summary") or "",
            "related_topics": merged_related[:6],
        }

    except Exception as exc:
        yield {"type": "error", "error": str(exc)}


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


def _resolve_related_topics(raw_list: list) -> list:
    """Convert the new {title, slug} schema from Claude into frontend-ready dicts.

    For each entry:
    - If Claude gave a valid catalog slug → chip with url.
    - Else run title through resolve_topic() → chip with url when found.
    - Otherwise → chip with prompt (AI-ask button).

    Dedupes by resolved slug so two entries pointing to the same lesson collapse.
    """
    seen_slugs: set = set()
    result = []

    for t in raw_list:
        if not isinstance(t, dict):
            continue
        title = str(t.get("title") or "").strip()[:80]
        if not title:
            continue

        claude_slug = (t.get("slug") or "").strip().lower() or None

        # Prefer the slug Claude explicitly provided if it's valid.
        from topics import TOPICS as _TOPICS
        valid_slugs = {_t["slug"] for _t in _TOPICS}

        resolved_slug = None
        if claude_slug and claude_slug in valid_slugs:
            resolved_slug = claude_slug
        else:
            resolved_slug = resolve_topic(title)

        if resolved_slug:
            if resolved_slug in seen_slugs:
                continue
            seen_slugs.add(resolved_slug)
            canonical = get_canonical_name(resolved_slug)
            result.append({"label": canonical, "url": f"/lesson/{resolved_slug}"})
        else:
            result.append({"label": title, "prompt": title[:300]})

    return result


def _extract_first_python_block(markdown: str) -> str:
    """Pull the first ```python ...``` fenced block out of a markdown body.

    Used as a fallback when Claude forgets to populate the `code` field
    separately — we just lift the code out of the lesson body instead.
    """
    m = re.search(r"```python\s*\n(.*?)\n```", markdown, re.DOTALL)
    return m.group(1).strip() if m else ""
