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
    """search(query, limit=5) — takes a partial query string, 
    returns a list of {slug, name, icon, description, score} dicts."""

    DB_PATH = Path(__file__).parent / "instance" / "codegen.db"
    con =sqlite3.connect(DB_PATH)


    query = query.strip()
    if not query:
        return []

    parts = re.sub(r"[^a-zA-Z0-9 ]", " ", query)

    parts = parts.split()

    parts[-1] += "*"

    con.execute(
    "SELECT slug FROM lessons_fts WHERE lessons_fts MATCH ? ORDER BY bm25(lessons_fts, 10.0, 5.0, 2.0, 1.0) LIMIT ?",
    (query_string, limit)
)




    return

if __name__ == "__main__":
    build_index()
    print("indexed")