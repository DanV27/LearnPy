"""
Tests for topic_resolver.resolve_topic() and resolve_topic_strict().

All tests are pure: no Flask, no Claude, no network.
resolve_topic() uses sqlite3 for the FTS fallback, which requires the
search index to exist (build_index() is called in conftest via flask_app
startup).  The lookup-table path (steps 1–2) needs no DB at all.
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from topic_resolver import resolve_topic, resolve_topic_strict, _normalize, _singular


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

class TestNormalize:
    def test_strips_leading_python(self):
        assert _normalize("Python Comments") == "comments"

    def test_strips_hyphen_python_prefix(self):
        assert _normalize("python-variables") == "variables"

    def test_lowercases(self):
        assert _normalize("BINARY SEARCH") == "binary search"

    def test_collapses_hyphens_to_spaces(self):
        assert _normalize("linked-list") == "linked list"

    def test_strips_trailing_python(self):
        # Not a real catalog name but tests the rule
        assert _normalize("comments python") == "comments"

    def test_strips_punctuation(self):
        assert _normalize("hash map!") == "hash map"


class TestSingular:
    def test_strips_trailing_s(self):
        assert _singular("lists") == "list"

    def test_leaves_short_words(self):
        assert _singular("is") == "is"

    def test_leaves_no_trailing_s(self):
        assert _singular("stack") == "stack"


# ---------------------------------------------------------------------------
# Exact slug match
# ---------------------------------------------------------------------------

class TestExactSlug:
    def test_exact_slug(self):
        assert resolve_topic("python-comments") == "python-comments"

    def test_exact_slug_case_insensitive(self):
        assert resolve_topic("Python-Comments") == "python-comments"

    def test_linked_list_slug(self):
        assert resolve_topic("linked-list") == "linked-list"

    def test_hash_map_slug(self):
        assert resolve_topic("hash-map") == "hash-map"

    def test_binary_search_slug(self):
        assert resolve_topic("binary-search") == "binary-search"


# ---------------------------------------------------------------------------
# Normalised name / slug lookup (no FTS needed)
# ---------------------------------------------------------------------------

class TestNormalisedLookup:
    def test_display_name(self):
        assert resolve_topic("Python Comments") == "python-comments"

    def test_display_name_lowercase(self):
        assert resolve_topic("python comments") == "python-comments"

    def test_strip_python_prefix(self):
        # "Comments" → normalize strips nothing ("python" not present),
        # lookup maps "comments" → "python-comments" via the name normalization
        assert resolve_topic("Comments") == "python-comments"

    def test_hyphen_vs_space(self):
        assert resolve_topic("linked list") == "linked-list"

    def test_hyphen_vs_space_capitalized(self):
        assert resolve_topic("Linked List") == "linked-list"

    def test_plural_name(self):
        # "Python Lists" → normalize → "lists" → singular "list"
        # lookup has "lists" mapped from "Python Lists"
        assert resolve_topic("Python Lists") == "python-lists"

    def test_hash_map_spaced(self):
        assert resolve_topic("hash map") == "hash-map"

    def test_hash_map_display_name(self):
        assert resolve_topic("Hash Map") == "hash-map"

    def test_big_o_notation(self):
        assert resolve_topic("Big O Notation") == "big-o-notation"

    def test_regular_expressions(self):
        assert resolve_topic("Regular Expressions") == "regex"

    def test_binary_search_spaced(self):
        assert resolve_topic("binary search") == "binary-search"

    def test_recursion(self):
        assert resolve_topic("recursion") == "recursion"

    def test_memoization(self):
        assert resolve_topic("Memoization") == "memoization"


# ---------------------------------------------------------------------------
# FTS fallback (requires search index — built by conftest via flask_app)
# ---------------------------------------------------------------------------

class TestFTSFallback:
    def test_binary_search_via_fts(self):
        # Should match via name even if exact lookup somehow missed
        result = resolve_topic("binary search algorithm")
        assert result == "binary-search"

    def test_off_catalog_returns_none(self):
        # "asyncio" doesn't appear in any lesson name/description
        assert resolve_topic("asyncio coroutines") is None

    def test_machine_learning_returns_none(self):
        assert resolve_topic("machine learning neural networks") is None

    def test_empty_string_returns_none(self):
        assert resolve_topic("") is None

    def test_whitespace_returns_none(self):
        assert resolve_topic("   ") is None


# ---------------------------------------------------------------------------
# resolve_topic_strict — exact / near-exact only, no FTS
# ---------------------------------------------------------------------------

class TestStrict:
    def test_exact_slug(self):
        assert resolve_topic_strict("python-comments") == "python-comments"

    def test_display_name(self):
        assert resolve_topic_strict("Python Comments") == "python-comments"

    def test_strip_python_prefix(self):
        assert resolve_topic_strict("Comments") == "python-comments"

    def test_linked_list(self):
        assert resolve_topic_strict("linked list") == "linked-list"

    def test_vague_question_returns_none(self):
        # A real question shouldn't redirect
        assert resolve_topic_strict("how do I use variables in Python?") is None

    def test_off_catalog_returns_none(self):
        assert resolve_topic_strict("asyncio") is None

    def test_empty_returns_none(self):
        assert resolve_topic_strict("") is None
