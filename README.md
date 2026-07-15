[![Test](https://github.com/DanV27/LearnPy/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/DanV27/LearnPy/actions/workflows/ci-cd.yml)
# LearnPy

A focused Python learning site — a curated catalog of short, hand-authored lessons, an in-browser coding challenge on every page, and an AI tutor for anything off-catalog. No ad walls, no SEO sludge, just the lesson, the code, and the challenge.

<img src="./assets/LearnPy_newGIF.gif" alt="Project Demo" width="900" />

## TRY NOW
https://ai-code-generator--danv27.replit.app/

---

## Engineering Highlights

The interesting bits a reviewer might want to see, with a one-line "why":

- **RAG with SQLite FTS5** — full-text retrieval grounds the AI tutor in 58 hand-authored lessons. No vector DB, no embedding model — zero new dependencies on top of stdlib SQLite.
- **In-browser Python execution via Pyodide (WASM)** — every coding challenge runs locally in the user's browser. No server-side sandbox to maintain, no untrusted-code risk, no rate limits to enforce. Each test runs in a fresh globals dict so state can't leak between cases.
- **Single-file template doing triple duty** — the same Jinja template renders the home page, every static lesson, and the AI-search-result view, controlled by `active_topic` / `active_lesson` context flags. One source of truth for the layout.
- **Static catalog over dynamic generation** — earlier iterations generated every lesson via Claude on first visit and cached in the DB. Pulled away from that because deterministic, hand-curated content beats AI drift. AI is now only invoked when a user genuinely searches off-catalog.
- **Per-user progress tracking + GitHub-style heatmap** — every lesson view and challenge completion gets a timestamp. The profile page renders a calendar-month heatmap of "days you beat a challenge" plus current/longest streaks, all computed in a pure-data module that's trivially testable.
- **Live autocomplete with debounced fetches + keyboard nav** — the search bar runs an FTS query against the catalog on every 150ms pause, shows ranked matches with the matched substring **bolded**, supports `↑ ↓ Enter Esc`, and gracefully falls through to the AI tutor when there's no catalog hit.
- **Defensive defaults at every API boundary** — JSON error handler converts any uncaught exception into JSON for `fetch()` callers (no HTML 500 pages breaking `r.json()`). Stale `fetch` responses are discarded if the user kept typing. Cursor-row tuples and dict accesses fall back to `or` defaults so a missing field never crashes a render.
- **Zero npm, zero build step** — Tailwind, marked.js, Pyodide all load from CDN. The entire frontend is plain Jinja + vanilla JS. One `python flask_app.py` and you have the whole product.

---

## What it is

LearnPy bundles four things into one site:

1. **A curated lesson catalog.** Three top-level sections — Basics (31 sub-topics), Data Structures (14 sub-topics), Algorithms (12 sub-topics) — broken into 58 focused lesson pages. Every lesson is short (~300 words), has at least one working Python code example, and links to related concepts.
2. **A coding challenge on every lesson.** Write Python in an editor on the page, click **Run Tests**, and your code is executed in your browser via Pyodide. Per-test pass/fail results show inline, and a `✓ CHALLENGE COMPLETE` badge lights up when every test passes.
3. **An AI tutor for everything else.** If your topic isn't in the catalog, type a question into the home-page search bar. Claude writes a custom mini-lesson grounded in the most-similar canonical lessons (RAG), and the related-topics chips become real links back into the catalog.
4. **Smart catalog search with live autocomplete.** As you type, an FTS5 index is queried in real time and matches appear in a dropdown — skip the AI entirely for direct catalog hits.

Plus per-user progress tracking and a profile heatmap that shows your activity over time.

---

## How a Lesson Works

1. **Browse the sidebar or search.** Click the **Topics** drawer in the header, or just start typing in the search bar — matches appear instantly as you type. If nothing matches, press Enter and the AI tutor takes over.
2. **Read the lesson.** Short explanation, working code example, related-topic chips, and a "Continue exploring" section with follow-up question buttons.
3. **Try the challenge.** Scroll to the Challenge section, write Python in the editor, click **Run Tests**. Your code runs locally in the browser — nothing leaves your machine.
4. **See progress accumulate.** Eyeball icons mark lessons you've viewed; green checks mark challenges you've passed. Your profile renders a heatmap of which days you beat a challenge.

---

## Feature Tour

### Curated catalog (3 sections, 58 lessons)

- **Basics** — 31 sub-topics: variables, types, casting, strings, control flow, functions, modules, virtualenvs, plus shared topics like JSON and regex.
- **Data Structures** — 14 sub-topics: stack, queue, deque, linked list, doubly linked list, heap (priority queue), trie, graph, hash map, Counter, defaultdict, namedtuple, frozenset.
- **Algorithms** — 12 sub-topics: Big O, recursion, linear & binary search, the five classic sorts, two pointers, sliding window, memoization.

Every entry has its own permanent URL (`/lesson/<slug>`) and its own coding challenge. Sub-topics are reached by clicking the parent in the sidebar — the parent page shows a clean grid of children that mirrors how docs sites organize content.

### In-browser coding challenges (47 of them)

- Each challenge is `{prompt, starter_code, tests}`, defined in `challenges_data.py`.
- The UI shows the prompt, a monospace editor pre-filled with starter code, and a Run Tests button.
- Clicking Run lazy-loads [Pyodide](https://pyodide.org/) (~10 MB, one-time, cached afterward), then runs each test in a fresh Python globals dict so tests can't contaminate each other.
- Results render as a list of green checks / red crosses with the failing assertion message when something's off.
- `Cmd / Ctrl + Enter` inside the editor triggers a run. Reset rolls back to starter code.

### Smart catalog search with autocomplete

- Powered by SQLite **FTS5** (full-text search v5) built into Python's stdlib `sqlite3` — no vector DB, no extra packages.
- Index is rebuilt at app startup from `lessons/*.md` so edits to lesson content show up after a restart.
- Search is fired client-side with a 150ms debounce so typing "decorators" sends one request, not eight.
- Stale-response guard: if a fetch returns after the user kept typing, the result is discarded.
- Results show with **matched substring bolded**, ranked by BM25 with column weights tuned to favor title matches over body matches.
- Full keyboard navigation: `↑` `↓` to highlight, `Enter` to navigate, `Esc` to close.
- Empty-state row reads "No catalog match — press Enter to ask the AI tutor", bridging cleanly to the AI fallback.

### AI tutor — now retrieval-augmented

Two places Claude gets called, both gated behind login:

1. **Home page search bar.** Type a question, get a custom Markdown lesson with a primary code snippet and 3-4 related-topic suggestions.
2. **Follow-up buttons + bottom search on lesson pages.** Four default follow-ups ("Explain more", "Why do I need this?", "Show a real example", "Common pitfalls") are pre-baked prompts that include the topic name. The "Ask anything else..." input lets the user phrase their own. Answers stack as cards below the lesson so the conversation history stays visible.

**Both paths are now RAG-grounded.** Before each Claude call, the same FTS index that powers autocomplete retrieves the top 3 most-similar canonical lessons. Those are injected into the prompt as context ("Here are existing LearnPy lessons relevant to this query"), and they're also merged into the response's `related_topics` as **URL-backed chips** — so AI-generated lessons stay coherent with the hand-authored catalog instead of confabulating in isolation.

### Per-user progress tracking

- Every lesson view writes (or upserts) a row in `lesson_progress` with `viewed_at`.
- Beating every test in a challenge fires `POST /api/progress/complete` which sets `completed_at`.
- Topic grids on the home page and parent-topic pages light up an **eyeball icon** for viewed lessons and a **green check** for completed ones.
- Lesson pages remember completion across sessions — the `✓ CHALLENGE COMPLETE` badge defaults to visible if you've already beaten it.

### Profile with monthly heatmap

- `/profile` renders a GitHub-style calendar heatmap of "days you beat at least one challenge this month".
- All math lives in `profile_data.py` as a pure data function — no Flask imports, trivially testable in isolation.
- Function returns weeks of cells, plus stats: total completions, active days, current streak, longest streak.
- Designed to extend cleanly to `?year=...&month=...` for past-month browsing without backend changes.

### Authentication

- Username + password with `pbkdf2:sha256` hashing via `werkzeug.security`.
- Sessions managed by Flask-Login.
- Sign-up and login POST JSON; errors come back as JSON (never an HTML debug page that breaks `fetch().then(r.json())`).
- Anonymous visitors see `/about` only; everything else is `@login_required`.

---

## Tech Stack

- **Backend:** Python 3.9+, Flask, Flask-Login, Flask-SQLAlchemy, Flask-Migrate (Alembic). Postgres (Neon) in production; SQLite locally and in CI.
- **AI:** Anthropic Claude API via the official `anthropic` Python SDK. Single entry point in `generator.py`.
- **Retrieval:** SQLite FTS5 with `porter unicode61` tokenization and BM25 ranking. Indexes ~58 lesson bodies in under 100ms at startup.
- **In-browser code execution:** [Pyodide](https://pyodide.org/) (CPython compiled to WebAssembly), loaded lazily from jsDelivr on the first Run Tests click.
- **Frontend:** Jinja2 templates, Tailwind CSS via CDN, Space Grotesk + JetBrains Mono fonts, Material Symbols icons, [marked.js](https://marked.js.org/) for rendering AI-generated Markdown.
- **Auth + security:** `pbkdf2:sha256` password hashing, parameter placeholders on every SQL query (no string concatenation), HTML-escape on every dynamic insertion.
- **Build / deploy:** zero npm, zero build step. `python flask_app.py` runs the whole product. Deployed live on Replit.

---

## Architecture

Modular by responsibility — every module has one job and is loaded by name from `flask_app.py`.

```
aiCodeGenerator/
├── flask_app.py           # Routes, auth, app setup, error handling
├── models.py              # SQLAlchemy: User, Generation, LessonProgress
│
├── topics.py              # Canonical catalog: 3 parents + 58 sub-topics
├── lessons.py             # Markdown loader for lessons/*.md
├── lessons/<slug>.md      # 58 hand-authored lesson files
│
├── challenges.py          # Thin loader exposing get_challenge(slug)
├── challenges_data.py     # All 47 challenges keyed by lesson slug
│
├── search_index.py        # SQLite FTS5: build_index() + search()
├── generator.py           # Only place Claude is called (now RAG-grounded)
│
├── profile_data.py        # Pure-data heatmap + stats calculation
│
├── templates/
│   ├── main.html          # Home / lesson page / AI-result view
│   ├── about.html         # Public marketing page
│   ├── profile.html       # Heatmap + progress stats
│   ├── login.html
│   └── signup.html
│
├── static/
│   └── logo.png           # Pixel-art snake mascot
│
├── migrations/            # Alembic migration files (flask db upgrade)
│   └── versions/
│       └── 0001_initial_schema.py
│
├── instance/
│   └── codegen.db         # SQLite: FTS5 search index (local dev also holds auth/progress)
│
└── README.md
```

**Request flow for `/lesson/<slug>`:**

```
@login_required → topics.get_topic(slug) → lessons.load_lesson(slug)
   → _resolve_related(...) → _resolve_children(...)
   → challenges.get_challenge(slug)
   → LessonProgress upsert (viewed_at)
   → render_template("main.html", active_topic=..., active_lesson=...)
```

**Request flow for `/generate` (AI tutor):**

```
@login_required → search_index.search(spec)  ← RAG retrieval
   → generator.generate_lesson(spec)
       → build context block from retrieved canonical lessons
       → POST to Claude API with augmented prompt
       → parse JSON, merge canonical URLs into related_topics
   → persist Generation row (history)
   → jsonify(result)
```

---

## Running Locally

```bash
# 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate     # macOS / Linux
# .venv\Scripts\activate       # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
#    Copy the example below into a file named .env at the project root.
#    .env is gitignored — never commit it.
cat > .env <<'EOF'
ANTHROPIC_API_KEY=sk-ant-...        # required for the AI tutor
SECRET_KEY=change-me-in-production  # Flask session signing key

# Optional — omit to use local SQLite (instance/codegen.db).
# Set to your Neon (or any Postgres) connection string for a hosted DB:
# DATABASE_URL=postgresql://user:pass@host/dbname
EOF

# 4. Run database migrations
#    First run only — or after any schema change in models.py:
flask db upgrade

# 5. Run the app
python flask_app.py
# Open http://localhost:5000
```

**Database notes:**
- Without `DATABASE_URL` set, the app creates `instance/codegen.db` (SQLite) automatically on startup. No setup required for local dev.
- With `DATABASE_URL` pointing to Postgres, the app skips the SQLite auto-create. Run `flask db upgrade` to apply the schema via Flask-Migrate before the first start.
- The FTS5 search index is always stored in a separate SQLite file (`instance/codegen.db`) even in production, rebuilt at startup from `lessons/*.md`.
- Schema migrations live in `migrations/versions/`. To generate a new migration after changing `models.py`:
  ```bash
  flask db migrate -m "describe your change"
  flask db upgrade
  ```

---

## Adding a New Topic

1. Append an entry to the `TOPICS` list in `topics.py` with a stable slug, name, icon (Material Symbols), level, and description.
2. Create `lessons/<slug>.md` with the lesson body and YAML-ish frontmatter (`title`, `summary`, `related`).
3. (Optional) Add a challenge to `challenges_data.py` under the same slug.
4. (Optional) For sub-topics, set `hide_from_sidebar: True` and append the slug to the parent topic's `children` list.

That's the whole flow. No backend changes required — the route, sidebar, topic grid, search index, and challenge wiring all pick the new entry up automatically on the next restart.

---

## Status

In active development. The lesson catalog, in-browser challenges, search-with-autocomplete, RAG-grounded AI tutor, progress tracking, and profile heatmap are all shipped. Next on the roadmap: per-section progress bars on the profile page, an "all topics" view, and an admin route for invalidating cached generations.

---

*Created by Daniel Valenzuela | 2026*
