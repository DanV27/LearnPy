"""
Tests for search_index.build_index() and search_index.search().

Six scenarios:
  1. Exact-word search returns the right lesson
  2. Title matches rank above body matches
  3. No match returns an empty list, not a crash
  4. Special characters / near-injection input don't crash the query
  5. Porter stemming works (stems map to indexed words)
  6. build_index() actually reads the markdown files correctly
"""
import sqlite3
from pathlib import Path

import pytest

import search_index


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FTS_DDL = (
    "CREATE VIRTUAL TABLE lessons_fts USING "
    "fts5(slug UNINDEXED, name, description, body, "
    "tokenize='porter unicode61')"
)

# Minimal rows covering every test scenario.
SEED_ROWS = [
    # slug, name, description, body
    ("binary-search",  "Binary Search",
     "Find an item fast in a sorted list.",
     "Binary search halves the search range each step. O(log n)."),
    ("bubble-sort",    "Bubble Sort",
     "A simple comparison-based sorting algorithm.",
     "Bubble sort repeatedly steps through the list comparing adjacent elements."),
    ("recursion",      "Recursion",
     "A function that calls itself.",
     "Recursion is used in tree traversal and dynamic programming."),
    ("title-only",     "Magnificent Walrus",
     "Short description.",
     "This body text mentions neither walrus nor magnificent explicitly at all."),
    ("body-only",      "Ordinary Lesson",
     "Short description.",
     "This body text mentions the magnificent walrus many times. "
     "Walrus walrus walrus."),
]


@pytest.fixture()
def search_db(tmp_path, monkeypatch):
    """
    Create a fresh FTS5 DB in a temp directory, seed it with SEED_ROWS, and
    redirect search_index.DB_PATH so both build_index() and search() use it.

    Also patches topics.get_topic so that our test-only slugs ("title-only",
    "body-only") return fake topic dicts instead of None — search() skips any
    slug that isn't in the catalog, which would silently drop test rows.
    """
    import topics as _topics

    db_file = tmp_path / "test_search.db"
    con = sqlite3.connect(db_file)
    con.execute(FTS_DDL)
    con.executemany(
        "INSERT INTO lessons_fts VALUES (?, ?, ?, ?)", SEED_ROWS
    )
    con.commit()
    con.close()

    monkeypatch.setattr(search_index, "DB_PATH", db_file)

    # Build a lookup from our seed data so fake slugs resolve correctly.
    fake_catalog = {
        slug: {"slug": slug, "name": name, "description": desc,
               "icon": "search", "level": "BEGINNER",
               "hide_from_sidebar": False}
        for slug, name, desc, _ in SEED_ROWS
    }
    real_get_topic = _topics.get_topic

    def patched_get_topic(slug):
        return fake_catalog.get(slug) or real_get_topic(slug)

    monkeypatch.setattr(search_index.topics, "get_topic", patched_get_topic)
    return db_file


# ---------------------------------------------------------------------------
# 1. Exact-word search returns the right lesson
# ---------------------------------------------------------------------------

class TestExactSearch:
    def test_exact_word_finds_lesson(self, search_db):
        results = search_index.search("recursion")
        slugs = [r["slug"] for r in results]
        assert "recursion" in slugs

    def test_result_has_expected_fields(self, search_db):
        results = search_index.search("recursion")
        r = next(r for r in results if r["slug"] == "recursion")
        assert r["name"] == "Recursion"
        assert r["url"] == "/lesson/recursion"
        assert "description" in r
        assert "icon" in r

    def test_unrelated_slug_not_returned(self, search_db):
        results = search_index.search("recursion")
        slugs = [r["slug"] for r in results]
        assert "bubble-sort" not in slugs


# ---------------------------------------------------------------------------
# 2. Title matches rank above body matches
# ---------------------------------------------------------------------------

class TestTitleRanksHigher:
    """
    'magnificent walrus' appears only in the *title* of 'title-only' but
    appears several times in the *body* of 'body-only'.  BM25 weights
    (10.0 for name vs 1.0 for body) mean 'title-only' should rank first.
    """

    def test_title_match_outranks_body_match(self, search_db):
        results = search_index.search("magnificent walrus")
        assert len(results) >= 2
        slugs = [r["slug"] for r in results]
        assert slugs.index("title-only") < slugs.index("body-only")


# ---------------------------------------------------------------------------
# 3. No match returns an empty list, not a crash
# ---------------------------------------------------------------------------

class TestNoMatch:
    def test_unknown_word_returns_empty_list(self, search_db):
        results = search_index.search("xyzzyplugh")
        assert results == []

    def test_empty_string_returns_empty_list(self, search_db):
        results = search_index.search("")
        assert results == []

    def test_whitespace_only_returns_empty_list(self, search_db):
        results = search_index.search("   ")
        assert results == []

    def test_return_type_is_always_list(self, search_db):
        assert isinstance(search_index.search("no match here ever"), list)


# ---------------------------------------------------------------------------
# 4. Special characters / near-injection input don't crash the query
# ---------------------------------------------------------------------------

class TestSpecialCharacters:
    @pytest.mark.parametrize("query", [
        '"binary"',           # FTS5 phrase syntax
        "binary*",            # prefix operator
        "binary OR sort",     # FTS5 boolean
        "binary AND sort",
        "binary NOT sort",
        "(binary)",           # grouping
        "^binary",            # column filter prefix
        "'; DROP TABLE lessons_fts; --",   # SQL injection attempt
        "🐍🔍",               # emoji / non-ASCII
        "a" * 300,            # very long input
    ])
    def test_does_not_raise(self, search_db, query):
        try:
            result = search_index.search(query)
            assert isinstance(result, list)
        except Exception as exc:
            pytest.fail(f"search({query!r}) raised {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# 5. Porter stemming works
# ---------------------------------------------------------------------------

class TestPorterStemming:
    """
    The index is built with tokenize='porter unicode61', so stems should
    match across different word forms.

    'sorting' → stem 'sort' → should find 'Bubble Sort' (name contains 'Sort')
    'comparing' → stem 'compar' → should find bubble-sort (body: 'comparing')
    'recursive' → stem 'recurs' → should find recursion (name: 'Recursion')
    """

    def test_inflected_verb_finds_noun(self, search_db):
        # "sorting" stems to "sort", which matches "Bubble Sort"
        results = search_index.search("sorting")
        slugs = [r["slug"] for r in results]
        assert "bubble-sort" in slugs

    def test_adjective_form_finds_noun(self, search_db):
        # "recursive" stems to "recurs", matching "Recursion"
        results = search_index.search("recursive")
        slugs = [r["slug"] for r in results]
        assert "recursion" in slugs

    def test_gerund_matches_body(self, search_db):
        # "comparing" stems to "compar", matching "comparing" in bubble-sort body
        results = search_index.search("comparing")
        slugs = [r["slug"] for r in results]
        assert "bubble-sort" in slugs


# ---------------------------------------------------------------------------
# 6. build_index() actually reads the markdown files correctly
# ---------------------------------------------------------------------------

class TestBuildIndex:
    """
    Point build_index() at a temp DB and let it read the real lessons/ dir.
    Verify slugs and names round-trip correctly for a few known lessons.
    """

    @pytest.fixture()
    def built_db(self, tmp_path, monkeypatch):
        db_file = tmp_path / "built.db"
        monkeypatch.setattr(search_index, "DB_PATH", db_file)
        search_index.build_index()
        return db_file

    def test_known_slug_is_indexed(self, built_db):
        con = sqlite3.connect(built_db)
        rows = con.execute(
            "SELECT slug FROM lessons_fts WHERE lessons_fts MATCH 'binary'"
        ).fetchall()
        con.close()
        slugs = [r[0] for r in rows]
        assert "binary-search" in slugs

    def test_lesson_name_is_stored(self, built_db):
        con = sqlite3.connect(built_db)
        row = con.execute(
            "SELECT name FROM lessons_fts WHERE slug = 'binary-search'"
        ).fetchone()
        con.close()
        assert row is not None
        assert row[0] == "Binary Search"

    def test_multiple_lessons_indexed(self, built_db):
        con = sqlite3.connect(built_db)
        count = con.execute(
            "SELECT COUNT(*) FROM lessons_fts"
        ).fetchone()[0]
        con.close()
        # There are 59 lessons listed in the module docstring; be conservative.
        assert count >= 10

    def test_body_has_no_raw_markdown_fences(self, built_db):
        """Code fences (```) should be stripped before indexing."""
        con = sqlite3.connect(built_db)
        rows = con.execute("SELECT body FROM lessons_fts").fetchall()
        con.close()
        for (body,) in rows:
            assert "```" not in body, f"Raw markdown fence found in indexed body"
