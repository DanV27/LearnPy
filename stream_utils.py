"""
Pure streaming helpers — no Flask, no Claude imports.

Factored out so they can be unit-tested without external dependencies.
The only stateful piece is DelimiterSplitter; the rest are pure functions.
"""

DELIMITER = "<<<META>>>"
_TAIL = len(DELIMITER) - 1  # max prefix of the delimiter that could straddle a chunk boundary


class DelimiterSplitter:
    """Feed raw text chunks in; get back text-to-flush until the delimiter appears.

    Usage::

        splitter = DelimiterSplitter()
        for chunk in raw_chunks:
            text, _ = splitter.feed(chunk)
            if text:
                yield_text_event(text)
        remaining_text, meta_str = splitter.finish()

    While the delimiter has not yet been seen:
    - feed() returns ``(text_to_flush, None)`` where ``text_to_flush`` is everything
      except the last ``len(DELIMITER)-1`` chars (which might be the start of a split
      delimiter and must be held back until the next chunk confirms they are not).

    Once the delimiter is found:
    - feed() returns ``("", None)`` and accumulates subsequent text internally as meta.

    finish() drains the internal buffers at end-of-stream:
    - Returns ``(remaining_text, meta_string_or_None)``.
    - If the stream ended without the delimiter, ``remaining_text`` is whatever was
      held back and ``meta_string_or_None`` is ``None``.
    """

    def __init__(self):
        self._pre_buf = ""   # text received before the delimiter
        self._meta_buf = ""  # text received after the delimiter
        self._found = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def feed(self, chunk: str):
        """Process one chunk. Returns ``(text_to_flush, None)``."""
        if self._found:
            self._meta_buf += chunk
            return "", None

        self._pre_buf += chunk
        idx = self._pre_buf.find(DELIMITER)

        if idx != -1:
            self._found = True
            text_before = self._pre_buf[:idx]
            after = self._pre_buf[idx + len(DELIMITER):]
            self._meta_buf = after.lstrip("\n")
            self._pre_buf = ""
            return text_before, None

        # Haven't seen the delimiter yet. Safe to flush everything except the last
        # _TAIL chars, which could be the opening of the delimiter split across chunks.
        safe_len = max(0, len(self._pre_buf) - _TAIL)
        to_flush = self._pre_buf[:safe_len]
        self._pre_buf = self._pre_buf[safe_len:]
        return to_flush, None

    def finish(self):
        """Drain all buffers at end of stream.

        Returns ``(remaining_text, meta_string_or_None)``.
        """
        if self._found:
            meta = self._meta_buf.strip() or None
            self._meta_buf = ""
            return "", meta

        # Stream ended without the delimiter — all held-back text is just lesson body.
        text = self._pre_buf
        self._pre_buf = ""
        return text, None

    @property
    def delimiter_found(self) -> bool:
        return self._found
