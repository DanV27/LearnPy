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
            "trie",
            "graph",
            "counter",
            "defaultdict",
            "namedtuple",
            "frozenset",
        ],
    },

    {
        "slug": "algorithms",
        "name": "Algorithms",
        "icon": "sort",
        "level": "INTERMEDIATE",
        "description": "Big O, searching, sorting, and the patterns that show up in every interview.",
        "children": [
            "big-o-notation",
            "recursion",
            "linear-search",
            "binary-search",
            "bubble-sort",
            "selection-sort",
            "insertion-sort",
            "merge-sort",
            "quicksort",
            "two-pointers",
            "sliding-window",
            "memoization",
        ],
    },


    # =========================================================================
    # Basics sub-topics — hidden from the sidebar; reached via /lesson/basics.
    # =========================================================================
    {"slug": "python-comments",          "name": "Python Comments",          "icon": "comment",         "level": "BEGINNER", "description": "Single-line and multi-line comments.", "hide_from_sidebar": True,},
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

    # =========================================================================
    # Algorithms sub-topics — hidden from sidebar; reached via
    # /lesson/algorithms.
    # =========================================================================
    {"slug": "big-o-notation",   "name": "Big O Notation",  "icon": "trending_up",     "level": "BEGINNER",     "description": "How to talk about how fast or slow code is.",   "hide_from_sidebar": True},
    {"slug": "recursion",        "name": "Recursion",       "icon": "autorenew",       "level": "BEGINNER",     "description": "Functions that call themselves.",                "hide_from_sidebar": True},
    {"slug": "linear-search",    "name": "Linear Search",   "icon": "search",          "level": "BEGINNER",     "description": "Walk the list, return the first match.",         "hide_from_sidebar": True},
    {"slug": "binary-search",    "name": "Binary Search",   "icon": "manage_search",   "level": "BEGINNER",     "description": "Halve the range each step — O(log n).",          "hide_from_sidebar": True},
    {"slug": "bubble-sort",      "name": "Bubble Sort",     "icon": "bubble_chart",    "level": "BEGINNER",     "description": "Swap adjacent pairs until sorted.",              "hide_from_sidebar": True},
    {"slug": "selection-sort",   "name": "Selection Sort",  "icon": "check_box",       "level": "BEGINNER",     "description": "Repeatedly pick the smallest remaining item.",   "hide_from_sidebar": True},
    {"slug": "insertion-sort",   "name": "Insertion Sort",  "icon": "input",           "level": "BEGINNER",     "description": "Build the sorted list one element at a time.",   "hide_from_sidebar": True},
    {"slug": "merge-sort",       "name": "Merge Sort",      "icon": "merge",           "level": "INTERMEDIATE", "description": "Split, sort each half, merge — O(n log n).",     "hide_from_sidebar": True},
    {"slug": "quicksort",        "name": "Quicksort",       "icon": "bolt",            "level": "INTERMEDIATE", "description": "Pick a pivot, partition, recurse.",              "hide_from_sidebar": True},
    {"slug": "two-pointers",     "name": "Two Pointers",    "icon": "compare_arrows",  "level": "INTERMEDIATE", "description": "Walk a sequence from both ends.",                "hide_from_sidebar": True},
    {"slug": "sliding-window",   "name": "Sliding Window",  "icon": "swipe_right",     "level": "INTERMEDIATE", "description": "A moving range over a sequence.",                "hide_from_sidebar": True},
    {"slug": "memoization",      "name": "Memoization",     "icon": "memory",          "level": "INTERMEDIATE", "description": "Cache results to skip repeat work.",             "hide_from_sidebar": True},

    # =========================================================================
    # Shared / cross-section sub-topics — referenced from more than one
    # parent's `children` list. Kept hidden from the sidebar so they don't
    # clutter top-level navigation.
    # =========================================================================
    {"slug": "json",               "name": "JSON",                "icon": "data_object",      "level": "BEGINNER",     "description": "Parse and emit JSON.",                              "hide_from_sidebar": True},
    {"slug": "regex",              "name": "Regular Expressions", "icon": "find_in_page",     "level": "INTERMEDIATE", "description": "Pattern matching with the re module.",              "hide_from_sidebar": True},
    {"slug": "hash-map",           "name": "Hash Map",            "icon": "key",              "level": "INTERMEDIATE", "description": "Build a hash map from scratch.",                    "hide_from_sidebar": True},
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

def get_parent(slug: str):
    """Return the parent topic, if none, return None"""
    for t in TOPICS:
        if slug in (t.get("children") or []):
            return t
    return None
