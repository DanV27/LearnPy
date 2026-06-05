"""
Curated catalog of canonical Python topics for LearnPy.

Each topic in this list shows up in the sidebar drawer and has its own
permanent URL at `/lesson/<slug>`. The actual lesson content lives in
`lessons/<slug>.md` — this file is just the registry.

To add a new topic:
  1. Append a dict here with a stable `slug`.
  2. Create `lessons/<slug>.md` with the lesson body and frontmatter.
That's it — the sidebar and the route will pick it up automatically.

Fields:
  slug         URL-safe identifier (used in /lesson/<slug>).
  name         Display name shown in the sidebar.
  icon         Material Symbols icon name — see fonts.google.com/icons.
  level        Difficulty tag — BEGINNER / INTERMEDIATE / ADVANCED.
  description  One-line summary shown on cards.
"""

TOPICS = [
    {
        "slug": "basics",
        "name": "Basics",
        "icon": "terminal",
        "level": "BEGINNER",
        "description": "Variables, types, control flow, and functions.",
    },
    {
        "slug": "data-structures",
        "name": "Data Structures",
        "icon": "database",
        "level": "INTERMEDIATE",
        "description": "List, dict, set, tuple — when to use each.",
    },
    {
        "slug": "binary-search-tree",
        "name": "Binary Search Tree",
        "icon": "account_tree",
        "level": "ADVANCED",
        "description": "Build a BST with insert, search, traversal.",
    },
    {
        "slug": "hash-map",
        "name": "Hash Map",
        "icon": "key",
        "level": "INTERMEDIATE",
        "description": "Build a hash map from scratch.",
    },
    {
        "slug": "sorting",
        "name": "Sorting Algorithms",
        "icon": "sort",
        "level": "INTERMEDIATE",
        "description": "Bubble, merge, and quicksort.",
    },
    {
        "slug": "binary-search",
        "name": "Binary Search",
        "icon": "search",
        "level": "BEGINNER",
        "description": "Find an item in a sorted list quickly.",
    },
    {
        "slug": "decorators",
        "name": "Decorators",
        "icon": "bolt",
        "level": "ADVANCED",
        "description": "Wrap functions with extra behavior.",
    },
    {
        "slug": "generators",
        "name": "Generators",
        "icon": "all_inclusive",
        "level": "ADVANCED",
        "description": "Lazy iteration with yield.",
    },
    {
        "slug": "context-managers",
        "name": "Context Managers",
        "icon": "lock",
        "level": "ADVANCED",
        "description": "Using with-statements safely.",
    },
    {
        "slug": "json",
        "name": "JSON",
        "icon": "data_object",
        "level": "BEGINNER",
        "description": "Parse and emit JSON.",
    },
    {
        "slug": "regex",
        "name": "Regular Expressions",
        "icon": "find_in_page",
        "level": "INTERMEDIATE",
        "description": "Pattern matching with the re module.",
    },
    {
        "slug": "asyncio",
        "name": "AsyncIO",
        "icon": "sync",
        "level": "ADVANCED",
        "description": "Concurrency with async/await.",
    },
    {
        "slug": "validate-email",
        "name": "Validate Email",
        "icon": "alternate_email",
        "level": "BEGINNER",
        "description": "Check email addresses safely.",
    },
    {
        "slug": "file-io",
        "name": "File I/O",
        "icon": "description",
        "level": "BEGINNER",
        "description": "Reading and writing files.",
    },
]


def get_topic(slug: str):
    """Return the topic dict for `slug`, or None if no such topic exists.

    Used by `flask_app.py` to validate URLs and to resolve related-topic
    slugs into display names + URLs for the related-topics chip strip.
    """
    for t in TOPICS:
        if t["slug"] == slug:
            return t
    return None
