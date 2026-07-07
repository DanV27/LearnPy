"""
Tests for stream_utils.DelimiterSplitter.

All tests are pure (no Flask, no Claude) — DelimiterSplitter takes strings in
and returns strings out, so there's nothing to mock.
"""
import pytest
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from stream_utils import DelimiterSplitter, DELIMITER


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _run(chunks):
    """Feed all chunks through a fresh splitter and return (full_text, meta_str)."""
    splitter = DelimiterSplitter()
    text_parts = []
    for chunk in chunks:
        t, _ = splitter.feed(chunk)
        text_parts.append(t)
    remaining, meta = splitter.finish()
    text_parts.append(remaining)
    return "".join(text_parts), meta


# ---------------------------------------------------------------------------
# 1. Delimiter arrives in a single chunk
# ---------------------------------------------------------------------------

class TestDelimiterInOneChunk:
    def test_basic_split(self):
        text, meta = _run([f"lesson body\n{DELIMITER}\n{{\"title\": \"T\"}}"])
        assert text == "lesson body\n"
        assert meta == '{"title": "T"}'

    def test_no_trailing_newline_before_meta(self):
        text, meta = _run([f"body{DELIMITER}meta"])
        assert text == "body"
        assert meta == "meta"

    def test_empty_body(self):
        text, meta = _run([f"{DELIMITER}\nmeta content"])
        assert text == ""
        assert meta == "meta content"

    def test_empty_meta(self):
        text, meta = _run([f"body\n{DELIMITER}"])
        assert text == "body\n"
        assert meta is None  # finish() strips and treats "" as None


# ---------------------------------------------------------------------------
# 2. Delimiter split across two chunks
# ---------------------------------------------------------------------------

class TestDelimiterSplitAcrossChunks:
    def test_split_in_middle(self):
        half = len(DELIMITER) // 2
        prefix = DELIMITER[:half]   # e.g. "<<<ME"
        suffix = DELIMITER[half:]   # e.g. "TA>>>"
        text, meta = _run([f"before{prefix}", f"{suffix}\njson"])
        assert text == "before"
        assert meta == "json"

    def test_split_at_first_char(self):
        text, meta = _run(["body" + DELIMITER[0], DELIMITER[1:] + "\nmeta"])
        assert text == "body"
        assert meta == "meta"

    def test_split_at_last_char(self):
        text, meta = _run(["body" + DELIMITER[:-1], DELIMITER[-1] + "\nmeta"])
        assert text == "body"
        assert meta == "meta"

    def test_delimiter_spread_across_three_chunks(self):
        d = DELIMITER
        c1 = "text" + d[:3]
        c2 = d[3:7]
        c3 = d[7:] + "\nmeta"
        text, meta = _run([c1, c2, c3])
        assert text == "text"
        assert meta == "meta"


# ---------------------------------------------------------------------------
# 3. No delimiter in stream
# ---------------------------------------------------------------------------

class TestNoDelimiter:
    def test_all_text_returned(self):
        text, meta = _run(["hello ", "world"])
        assert text == "hello world"
        assert meta is None

    def test_empty_stream(self):
        text, meta = _run([])
        assert text == ""
        assert meta is None

    def test_partial_delimiter_lookalike(self):
        # "<<<" is not the full delimiter — should flush normally
        text, meta = _run(["some <<<text without closing"])
        assert "<<<text" in text
        assert meta is None


# ---------------------------------------------------------------------------
# 4. Text after delimiter is accumulated correctly
# ---------------------------------------------------------------------------

class TestMetaAccumulation:
    def test_meta_spread_across_chunks(self):
        chunks = [
            f"lesson\n{DELIMITER}\n",
            '{"title":',
            ' "Hash Map"}',
        ]
        text, meta = _run(chunks)
        assert text == "lesson\n"
        assert meta == '{"title": "Hash Map"}'

    def test_multi_chunk_text_before_delimiter(self):
        chunks = ["para one\n", "para two\n", f"{DELIMITER}\nmeta"]
        text, meta = _run(chunks)
        assert text == "para one\npara two\n"
        assert meta == "meta"


# ---------------------------------------------------------------------------
# 5. delimiter_found property
# ---------------------------------------------------------------------------

class TestDelimiterFoundProperty:
    def test_false_before_delimiter(self):
        s = DelimiterSplitter()
        s.feed("no delimiter here")
        assert s.delimiter_found is False

    def test_true_after_delimiter(self):
        s = DelimiterSplitter()
        s.feed(f"body{DELIMITER}meta")
        assert s.delimiter_found is True

    def test_true_after_split_delimiter(self):
        s = DelimiterSplitter()
        s.feed("body" + DELIMITER[:4])
        assert s.delimiter_found is False
        s.feed(DELIMITER[4:] + "meta")
        assert s.delimiter_found is True


# ---------------------------------------------------------------------------
# 6. Feed after delimiter found
# ---------------------------------------------------------------------------

class TestFeedAfterDelimiter:
    def test_text_chunks_ignored_after_delimiter(self):
        s = DelimiterSplitter()
        s.feed(f"body{DELIMITER}")
        t1, _ = s.feed("chunk1 ")
        t2, _ = s.feed("chunk2")
        assert t1 == ""
        assert t2 == ""
        _, meta = s.finish()
        assert meta == "chunk1 chunk2"
