"""
Hand-authored coding challenges, keyed by lesson slug.

Each challenge is a dict with three fields:

  prompt        Short description of what the user should write.
  starter_code  Code that pre-fills the editor.
  tests         List of {"name", "code"} test cases. Each test's `code` is
                Python that runs AFTER the user's code, in a fresh globals
                dict. Any AssertionError or other exception fails the test.

The challenge content for each lesson lives in lessons/_challenges/<slug>.py
(populated by scripts/write_challenges.py) but is loaded into this module
at import time so the rest of the app can stay simple.

To author a new challenge:
  - Pick a focused, single-concept task that the lesson has prepared
    the user to solve.
  - Write 2-4 tests. The first is usually "does the thing exist", the
    rest verify behavior.
  - Each test's `assert` should include a short message so users know
    what went wrong when they click Run.
"""

# Importing the dict from challenges_data keeps this file's logic clean
# even when CHALLENGES grows to hundreds of entries.
from challenges_data import CHALLENGES


def get_challenge(slug: str):
    """Return the challenge dict for `slug`, or None if no challenge exists."""
    return CHALLENGES.get(slug)
