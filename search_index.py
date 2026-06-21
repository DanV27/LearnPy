"""Smarter search autocomplete
The problem today: typing into the search bar does nothing until you submit. If you typed "binary tree", you don't know your site has a Binary Search Tree page until you've already paid for an AI generation.
With RAG: as the user types, do a quick retrieval over the 59 lessons and show the top 3 matches as suggestions below the input. Click one → instant nav to the canonical page. Skip the AI when there's a direct hit. Saves Claude calls and is way faster.


two functions
build_index() — called at app startup. Reads every lessons/*.md, parses out title + summary + body, populates the FTS5 table. Drops and recreates the table on each startup so edits to lesson files always show up.
search(query, limit=5) — takes a partial query string, returns a list of {slug, name, icon, description, score} dicts.

"""

import sqlite3
import os

import re
from pathlib import Path

from flask import app
import lessons
import topics



LESSONS_DIR = Path(__file__).parent / "lessons"

def _load_all_lessons():
    """Walk lessons/*.md and return a list of dicts ready to insert.

    Each dict is {slug, name, description, body}. Orphan lesson files
    (no matching entry in topics.py) are skipped — they're not findable
    in the catalog anyway.
    """
    all_lessons = []
    
    for path in lessons.LESSONS_DIR.glob("*.md"):
        slug = path.stem

        topic = topics.get_topic(slug)
        if topic is None:                # orphan .md — no catalog entry
            continue

        lesson = lessons.load_lesson(slug)

        all_lessons.append({
            "slug": slug,
            "name": topic["name"],
            "description": topic["description"],
            "body": _strip_markdown(lesson["lesson_markdown"]),
        })

    return all_lessons

def _strip_markdown(text):
    """Remove fenced code blocks: anything between ``` lines. (A regex with re.DOTALL is the easiest way.)
    Replace inline link syntax [text](url) with just text. (Another regex.)
    Remove inline code spans backtick-text-backtick (`like this` → like this).
    Collapse runs of whitespace into single spaces.
    """
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r'\[(.*?)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def build_index():
    """
    called at app startup. Reads every lessons/*.md, parses out title + summary + body, populates the FTS5 table.
      Drops and recreates the table on each startup so edits to lesson files always show up.
    """


    DB_PATH = Path(__file__).parent / "instance" / "codegen.db"
    con =sqlite3.connect(DB_PATH)

    con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS lessons_fts USING " 
    "fts5(slug UNINDEXED, name, description, body, tokenize='porter unicode61')")

    con.execute("DELETE FROM lessons_fts")

    all_lessons = _load_all_lessons()

    for lesson in all_lessons:
        con.execute("INSERT INTO lessons_fts (slug, name, description, body) VALUES (?, ?, ?, ?)",
                    (lesson["slug"],lesson["name"], lesson["description"], lesson["body"]))
    
    con.commit()
    con.close()


    return 



def search(query, limit=5):
    """Run a prefix-matched FTS5 query and return up to `limit` results.

    Returns a list of dicts shaped like:
        {"slug": str, "name": str, "icon": str, "description": str, "url": str}
    Empty list if the query is empty, all-special-characters, or matches nothing.
    """

    # ---- Validate + clean the query BEFORE opening a DB connection. ----
    # If we bail out early, we don't want a dangling open connection.

    # 1. Strip whitespace. Strings are immutable — must reassign.
    query = query.strip()
    if not query:
        return []

    # 2. Sanitize: keep only letters, digits, spaces. Anything else becomes a
    #    space. This prevents the user from injecting FTS5 operators ( ", *,
    #    (, ^, etc.) that could crash the query with a syntax error.
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", " ", query)

    # 3. Split into individual words.
    parts = cleaned.split()

    # 4. If everything got sanitized away, there's nothing to search for.
    #    THIS CHECK GOES BEFORE we touch parts[-1] — otherwise IndexError.
    if not parts:
        return []

    # 5. Append * to the last word so we get PREFIX matching. The user is
    #    still typing — "binary se" should still find "binary search".
    parts[-1] += "*"

    # 6. Join back into one string. FTS5's MATCH takes a single string.
    #    THIS is where the str(parts) bug bit you — use join.
    fts_query = " ".join(parts)        # e.g. "binary se*"

    # ---- Now we're ready to talk to the database. ----

    DB_PATH = Path(__file__).parent / "instance" / "codegen.db"
    con = sqlite3.connect(DB_PATH)

    # 7. Run the query. The ? placeholders are filled in by SQLite from
    #    the tuple in the second argument, in order. Never f-string user
    #    input into SQL — placeholders are how you avoid injection.
    #
    #    BM25 weights map to the table columns in declaration order:
    #       slug (UNINDEXED, weight ignored), name, description, body
    #    Higher = more important. Name matches > description > body.
    cursor = con.execute(
        "SELECT slug FROM lessons_fts "
        "WHERE lessons_fts MATCH ? "
        "ORDER BY bm25(lessons_fts, 0.0, 10.0, 5.0, 1.0) "
        "LIMIT ?",
        (fts_query, limit),
    )

    # 8. Iterate the cursor. Each row is a tuple — even with one column.
    #    For each slug, look up the rest of the topic info from the
    #    catalog and build a result dict.
    results = []
    for row in cursor:
        slug = row[0]                  # SELECT slug → row is a 1-tuple
        topic = topics.get_topic(slug)
        if topic is None:
            continue                   # defensive — should never happen
        results.append({
            "slug": slug,
            "name": topic["name"],
            "icon": topic["icon"],
            "description": topic["description"],
            "url": f"/lesson/{slug}",
        })

    # 9. Close the connection. Always. Even on the happy path.
    con.close()

    return results

