"""
Curated catalog of canonical Python topics for LearnPy.

Topics fall into two categories:

  - Top-level topics — shown in the sidebar drawer. Each has its own permanent
    URL at /lesson/<slug>. The lesson content lives in lessons/<slug>.md.
  - Sub-topics — child pages of a parent topic. Marked `hide_from_sidebar` so
    they don't clutter the sidebar; they're discovered by clicking the parent
    topic (e.g. Basics) and browsing the sub-topic grid that appears there.

To add a new topic:
  1. Append a dict here with a stable `slug`.
  2. Create `lessons/<slug>.md` with the lesson body and frontmatter.
  3. If it should appear under a parent (like Basics), also append the slug
     to that parent's `children` list.

Fields:
  slug              URL-safe identifier (used in /lesson/<slug>).
  name              Display name shown in sidebar / cards.
  icon              Material Symbols icon name — see fonts.google.com/icons.
  level             Difficulty tag — BEGINNER / INTERMEDIATE / ADVANCED.
  description       One-line summary shown on cards.
  children          (Optional) ordered list of child topic slugs that appear
                    as a sub-topic grid on this topic's page.
  hide_from_sidebar (Optional) if True, this topic is not shown in the
                    sidebar drawer. Use this for sub-topics that are
                    discovered via a parent's sub-topic grid.
  followups         (Optional) override of the default follow-up question
                    buttons. Each is {label, prompt}. If absent, defaults
                    are generated in flask_app.py.
"""

TOPICS = [
    # =========================================================================
    # Top-level topics (visible in the sidebar)
    # =========================================================================
    {
        "slug": "basics",
        "name": "Basics",
        "icon": "terminal",
        "level": "BEGINNER",
        "description": "Python's fundamentals — variables, types, control flow, functions, and more.",
        # Ordered list of sub-topic slugs shown as a grid on /lesson/basics.
        # Includes references to two existing top-level topics (json, regex)
        # which naturally fit under the Basics umbrella as well.
        "children": [
            "python-comments",
            "python-variables",
            "python-data-types",
            "python-numbers",
            "python-casting",
            "python-strings",
            "python-booleans",
            "python-operators",
            "python-lists",
            "python-tuples",
            "python-sets",
            "python-dictionaries",
            "python-if-else",
            "python-match",
            "python-while-loops",
            "python-for-loops",
            "python-functions",
            "python-range",
            "python-arrays",
            "python-iterators",
            "python-modules",
            "python-dates",
            "python-math",
            "json",                 # reuses existing top-level lesson
            "regex",                # reuses existing top-level lesson
            "python-pip",
            "python-try-except",
            "python-string-formatting",
            "python-none",
            "python-user-input",
            "python-virtualenv",
        ],
    },
    {
        "slug": "data-structures",
        "name": "Data Structures",
        "icon": "database",
        "level": "INTERMEDIATE",
        "description": "Advanced data structures — stacks, queues, heaps, tries, and more.",
        # Reuses the existing `hash-map` and `binary-search-tree` top-level
        # topics — they naturally fit under Data Structures too.
        "children": [
            "stack",
            "queue",
            "deque",
            "linked-list",
            "doubly-linked-list",
            "priority-queue",
            "hash-map",
            "binary-search-tree",
            "trie",
            "graph",
            "counter",
            "defaultdict",
            "namedtuple",
            "frozenset",
        ],
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

    # =========================================================================
    # Basics sub-topics — hidden from the sidebar; reached via /lesson/basics.
    # =========================================================================
    {"slug": "python-comments",          "name": "Python Comments",          "icon": "comment",         "level": "BEGINNER", "description": "Single-line and multi-line comments.", "hide_from_sidebar": True},
    {"slug": "python-variables",         "name": "Python Variables",         "icon": "label",           "level": "BEGINNER", "description": "Assignment, naming, and scope.", "hide_from_sidebar": True},
    {"slug": "python-data-types",        "name": "Python Data Types",        "icon": "category",        "level": "BEGINNER", "description": "Built-in types at a glance.", "hide_from_sidebar": True},
    {"slug": "python-numbers",           "name": "Python Numbers",           "icon": "pin",             "level": "BEGINNER", "description": "int, float, complex.", "hide_from_sidebar": True},
    {"slug": "python-casting",           "name": "Python Casting",           "icon": "swap_horiz",      "level": "BEGINNER", "description": "Converting between types.", "hide_from_sidebar": True},
    {"slug": "python-strings",           "name": "Python Strings",           "icon": "text_fields",     "level": "BEGINNER", "description": "Creating, slicing, formatting.", "hide_from_sidebar": True},
    {"slug": "python-booleans",          "name": "Python Booleans",          "icon": "toggle_on",       "level": "BEGINNER", "description": "True, False, and truthiness.", "hide_from_sidebar": True},
    {"slug": "python-operators",         "name": "Python Operators",         "icon": "calculate",       "level": "BEGINNER", "description": "Arithmetic, comparison, logical.", "hide_from_sidebar": True},
    {"slug": "python-lists",             "name": "Python Lists",             "icon": "list",            "level": "BEGINNER", "description": "Ordered, mutable collections.", "hide_from_sidebar": True},
    {"slug": "python-tuples",            "name": "Python Tuples",            "icon": "ballot",          "level": "BEGINNER", "description": "Immutable sequences.", "hide_from_sidebar": True},
    {"slug": "python-sets",              "name": "Python Sets",              "icon": "ad_group",        "level": "BEGINNER", "description": "Unique, unordered collections.", "hide_from_sidebar": True},
    {"slug": "python-dictionaries",      "name": "Python Dictionaries",      "icon": "menu_book",       "level": "BEGINNER", "description": "Key-value mappings.", "hide_from_sidebar": True},
    {"slug": "python-if-else",           "name": "Python If...Else",         "icon": "fork_right",      "level": "BEGINNER", "description": "Conditional branching.", "hide_from_sidebar": True},
    {"slug": "python-match",             "name": "Python Match",             "icon": "rule",            "level": "INTERMEDIATE", "description": "Structural pattern matching.", "hide_from_sidebar": True},
    {"slug": "python-while-loops",       "name": "Python While Loops",       "icon": "loop",            "level": "BEGINNER", "description": "Repeat while a condition holds.", "hide_from_sidebar": True},
    {"slug": "python-for-loops",         "name": "Python For Loops",         "icon": "repeat",          "level": "BEGINNER", "description": "Iterate over sequences.", "hide_from_sidebar": True},
    {"slug": "python-functions",         "name": "Python Functions",         "icon": "functions",       "level": "BEGINNER", "description": "Defining and calling functions.", "hide_from_sidebar": True},
    {"slug": "python-range",             "name": "Python Range",             "icon": "linear_scale",    "level": "BEGINNER", "description": "Generating number sequences.", "hide_from_sidebar": True},
    {"slug": "python-arrays",            "name": "Python Arrays",            "icon": "grid_view",       "level": "BEGINNER", "description": "Lists vs. arrays vs. numpy.", "hide_from_sidebar": True},
    {"slug": "python-iterators",         "name": "Python Iterators",         "icon": "skip_next",       "level": "INTERMEDIATE", "description": "iter() and next().", "hide_from_sidebar": True},
    {"slug": "python-modules",           "name": "Python Modules",           "icon": "extension",       "level": "BEGINNER", "description": "import and your own modules.", "hide_from_sidebar": True},
    {"slug": "python-dates",             "name": "Python Dates",             "icon": "schedule",        "level": "BEGINNER", "description": "The datetime module.", "hide_from_sidebar": True},
    {"slug": "python-math",              "name": "Python Math",              "icon": "calculate",       "level": "BEGINNER", "description": "Functions in the math module.", "hide_from_sidebar": True},
    {"slug": "python-pip",               "name": "Python PIP",               "icon": "inventory_2",     "level": "BEGINNER", "description": "Install and manage packages.", "hide_from_sidebar": True},
    {"slug": "python-try-except",        "name": "Python Try...Except",      "icon": "emergency",       "level": "BEGINNER", "description": "Handling exceptions.", "hide_from_sidebar": True},
    {"slug": "python-string-formatting", "name": "Python String Formatting", "icon": "format_paint",    "level": "BEGINNER", "description": "f-strings and .format().", "hide_from_sidebar": True},
    {"slug": "python-none",              "name": "Python None",              "icon": "block",           "level": "BEGINNER", "description": "Python's null value.", "hide_from_sidebar": True},
    {"slug": "python-user-input",        "name": "Python User Input",        "icon": "keyboard",        "level": "BEGINNER", "description": "Reading input() from users.", "hide_from_sidebar": True},
    {"slug": "python-virtualenv",        "name": "Python VirtualEnv",        "icon": "folder_managed",  "level": "BEGINNER", "description": "Isolated dependency environments.", "hide_from_sidebar": True},

    # =========================================================================
    # Data Structures sub-topics — hidden from sidebar; reached via
    # /lesson/data-structures.
    # =========================================================================
    {"slug": "stack",              "name": "Stack",              "icon": "table_rows",       "level": "INTERMEDIATE", "description": "Last-in-first-out — push and pop.",                 "hide_from_sidebar": True},
    {"slug": "queue",              "name": "Queue",              "icon": "linear_scale",     "level": "INTERMEDIATE", "description": "First-in-first-out — enqueue and dequeue.",        "hide_from_sidebar": True},
    {"slug": "deque",              "name": "Deque",              "icon": "swap_horiz",       "level": "INTERMEDIATE", "description": "Double-ended queue from collections.",             "hide_from_sidebar": True},
    {"slug": "linked-list",        "name": "Linked List",        "icon": "link",             "level": "INTERMEDIATE", "description": "Nodes pointing to nodes.",                         "hide_from_sidebar": True},
    {"slug": "doubly-linked-list", "name": "Doubly Linked List", "icon": "compare_arrows",   "level": "ADVANCED",     "description": "Linked list with prev pointers too.",              "hide_from_sidebar": True},
    {"slug": "priority-queue",     "name": "Priority Queue",     "icon": "priority_high",    "level": "INTERMEDIATE", "description": "Heap-backed queue with the heapq module.",         "hide_from_sidebar": True},
    {"slug": "trie",               "name": "Trie",               "icon": "schema",           "level": "ADVANCED",     "description": "Prefix tree — fast string lookups.",               "hide_from_sidebar": True},
    {"slug": "graph",              "name": "Graph",              "icon": "polyline",         "level": "ADVANCED",     "description": "Nodes and edges with an adjacency list.",          "hide_from_sidebar": True},
    {"slug": "counter",            "name": "Counter",            "icon": "tag",              "level": "BEGINNER",     "description": "Count occurrences — collections.Counter.",         "hide_from_sidebar": True},
    {"slug": "defaultdict",        "name": "defaultdict",        "icon": "folder_special",   "level": "BEGINNER",     "description": "Auto-default dict — collections.defaultdict.",     "hide_from_sidebar": True},
    {"slug": "namedtuple",         "name": "namedtuple",         "icon": "label_important",  "level": "BEGINNER",     "description": "Tuples with named fields — collections.namedtuple.","hide_from_sidebar": True},
    {"slug": "frozenset",          "name": "frozenset",          "icon": "ac_unit",          "level": "INTERMEDIATE", "description": "Immutable, hashable sets.",                        "hide_from_sidebar": True},
]


def get_topic(slug: str):
    """Return the topic dict for `slug`, or None if no such topic exists."""
    for t in TOPICS:
        if t["slug"] == slug:
            return t
    return None


def visible_in_sidebar():
    """Return the topics that should appear in the sidebar drawer (i.e.
    everything that isn't marked `hide_from_sidebar`)."""
    return [t for t in TOPICS if not t.get("hide_from_sidebar")]
