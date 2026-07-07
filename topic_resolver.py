"""
Resolve a free-form topic title to a canonical catalog slug.

Two public functions:

  resolve_topic(title)        — tries hard; FTS fallback included.
                                 Use when annotating AI-suggested related topics.
  resolve_topic_strict(title) — exact / near-exact only, no FTS.
                                 Use for the front-door redirect check.

No Flask imports. Pure Python + sqlite3 (via search_index).
"""

import re
from topics import TOPICS
from search_index import search_scored

# ---------------------------------------------------------------------------
# Threshold for the FTS fallback.
# BM25 scores in SQLite FTS5 are negative; more negative = stronger match.
# -1.5 accepts clear name/description matches while rejecting weak body-only
# hits on tangential lessons.
# ---------------------------------------------------------------------------
_BM25_THRESHOLD = -1.5

# ---------------------------------------------------------------------------
# Lookup tables — built once at import, O(1) lookups per call.
# ---------------------------------------------------------------------------

def _normalize(s: str) -> str:
    """Lowercase, strip leading/trailing 'python', collapse hyphens/spaces."""
    s = s.lower().strip()
    s = re.sub(r"^python[\s\-]+", "", s)   # strip "python " or "python-" prefix
    s = re.sub(r"[\s\-]+python$", "", s)   # strip trailing " python"
    s = re.sub(r"[-_]+", " ", s)           # hyphens → spaces
    s = re.sub(r"[^\w\s]", " ", s)         # drop punctuation
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _singular(s: str) -> str:
    """Very naive de-pluralisation: strip a trailing 's' from the last word."""
    if s.endswith("s") and len(s) > 3:
        return s[:-1]
    return s


# Populated at module load — maps normalised strings → canonical slug.
_NORM_TO_SLUG: dict = {}
_SLUG_SET: set = set()
_SLUG_TO_NAME: dict = {}

for _t in TOPICS:
    _slug = _t["slug"]
    _name = _t["name"]
    _SLUG_SET.add(_slug)
    _SLUG_TO_NAME[_slug] = _name

    # 1. Exact slug as a key (e.g. "linked-list" → _normalize → "linked list")
    _slug_norm = _normalize(_slug)
    _NORM_TO_SLUG[_slug_norm] = _slug
    _NORM_TO_SLUG[_singular(_slug_norm)] = _slug

    # 2. Normalised display name (e.g. "Python Comments" → "comments")
    _name_norm = _normalize(_name)
    _NORM_TO_SLUG[_name_norm] = _slug
    _NORM_TO_SLUG[_singular(_name_norm)] = _slug

    # 3. Raw lowercase slug (e.g. "linked-list")
    _NORM_TO_SLUG[_slug.lower()] = _slug


def get_canonical_name(slug: str) -> str:
    """Return the display name for a slug, or the slug itself as fallback."""
    return _SLUG_TO_NAME.get(slug, slug)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def resolve_topic(title: str) -> "str | None":
    """Map a free-form topic title to a catalog slug, or return None.

    Resolution order:
      1. Exact slug match (e.g. "linked-list").
      2. Normalised name / slug lookup (handles "Python Comments", "Linked List",
         "linked list", "Linked Lists", "Comments", etc.).
      3. FTS5 fallback: accepts the top hit only when its BM25 score is below
         _BM25_THRESHOLD (i.e. a genuine name/description match, not a weak
         body-only coincidence).
    """
    if not title or not title.strip():
        return None

    title = title.strip()

    # 1. Exact slug.
    if title.lower() in _SLUG_SET:
        return title.lower()

    # 2. Normalised lookup (with and without trailing 's').
    norm = _normalize(title)
    if norm in _NORM_TO_SLUG:
        return _NORM_TO_SLUG[norm]
    sing = _singular(norm)
    if sing in _NORM_TO_SLUG:
        return _NORM_TO_SLUG[sing]

    # 3. FTS fallback — strip question-word noise first so AND semantics
    #    don't reject "how do hash maps work" on "how".
    fts_query = _strip_noise(title)
    if not fts_query:
        return None
    hits = search_scored(fts_query, limit=1)
    if hits:
        slug, score = hits[0]
        if score < _BM25_THRESHOLD:
            return slug

    return None


def resolve_topic_strict(title: str) -> "str | None":
    """Exact / near-exact match only — no FTS fallback.

    Used for the front-door redirect check in /generate/stream so we only
    short-circuit queries that are unambiguously asking for a catalog lesson,
    never hijacking a genuine off-catalog question.
    """
    if not title or not title.strip():
        return None

    title = title.strip()

    if title.lower() in _SLUG_SET:
        return title.lower()

    norm = _normalize(title)
    if norm in _NORM_TO_SLUG:
        return _NORM_TO_SLUG[norm]
    sing = _singular(norm)
    if sing in _NORM_TO_SLUG:
        return _NORM_TO_SLUG[sing]

    return None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_NOISE_WORDS = {
    "how", "do", "does", "did", "what", "why", "when", "where", "which",
    "is", "are", "was", "were", "be", "been",
    "the", "a", "an", "of", "in", "on", "for", "with", "and", "or", "to",
    "me", "my", "i", "you", "your", "this", "that",
    "about", "can", "could", "should", "would", "will", "use", "using",
}


def _strip_noise(title: str) -> str:
    """Remove question-words/connectors so FTS AND semantics can still find topics."""
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", " ", title).lower()
    words = [w for w in cleaned.split() if w not in _NOISE_WORDS and len(w) > 1]
    return " ".join(words)
