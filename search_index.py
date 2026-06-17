"""Smarter search autocomplete
The problem today: typing into the search bar does nothing until you submit. If you typed "binary tree", you don't know your site has a Binary Search Tree page until you've already paid for an AI generation.
With RAG: as the user types, do a quick retrieval over the 59 lessons and show the top 3 matches as suggestions below the input. Click one → instant nav to the canonical page. Skip the AI when there's a direct hit. Saves Claude calls and is way faster.


two functions
build_index() — called at app startup. Reads every lessons/*.md, parses out title + summary + body, populates the FTS5 table. Drops and recreates the table on each startup so edits to lesson files always show up.
search(query, limit=5) — takes a partial query string, returns a list of {slug, name, icon, description, score} dicts.

"""

import sqlite3

import re
from pathlib import Path
from lessons import load_lesson


LESSONS_DIR = Path(__file__).parent / "lessons"

def _build_index():
    """called at app startup. Reads every lessons/*.md, parses out title + summary + body, populates the FTS5 table.
    Drops and recreates the table on each startup so edits to lesson files always show up.
    """
    con = sqlite3.connect(":memory:")
    con.execute("CREATE VIRTUAL TABLE docs USING fts5(slug UNINDEXED, name, body)")

    for lesson in LESSONS_DIR:
        load_lesson(lesson)


        con.execute(
        "INSERT INTO docs (slug, name, body) VALUES (?, ?, ?)",
        ('related_slugs', 'title', 'summary')
        )


    con.commit()
    print(con.execute("SELECT slug FROM docs WHERE docs MATCH 'decorator*'").fetchone())



    return



def search(query, limit=5):
    return

_build_index()