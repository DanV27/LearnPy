# LearnPy

A focused Python learning site — a curated catalog of short, hand-authored lessons, an in-browser coding challenge on every page, and an AI tutor for anything off-catalog. No ad walls, no SEO sludge, just the lesson, the code, and the challenge.

![Project Demo](./assets/LearnPyGIF.gif)


## TRY NOW
https://ai-code-generator--danv27.replit.app/

## What it is

LearnPy bundles three things into one site:

1. **A curated lesson catalog.** 14 top-level topics in the sidebar, broken into 55+ focused lesson pages. Every lesson is short (~300 words), has at least one working Python code example, and links to related concepts.
2. **A coding challenge on every lesson.** Write Python in an editor on the page, click Run Tests, and your code is executed in the browser via Pyodide. Per-test pass/fail results show inline, and a `✓ CHALLENGE COMPLETE` badge lights up when every test passes.
3. **An AI tutor for everything else.** If your topic isn't in the catalog, type a question into the home-page search bar and Claude writes you a custom mini-lesson. Each lesson page also has follow-up buttons ("Explain more", "Why do I need this?", etc.) that summon the AI for a deeper take on the current topic.

## How a Lesson Works

1. **Browse the sidebar (or search.)** Click the **Topics** drawer in the header, pick a topic. Or, from the home page, type a question into the search bar.
2. **Read the lesson.** Short explanation, working code example, links to related topics.
3. **Try the challenge.** Scroll to the Challenge section, write Python in the editor, click **Run Tests**. Your code runs locally in the browser — nothing leaves your machine.
4. **Keep exploring.** Each page ends with related-topic chips and four follow-up question buttons that invoke the AI tutor for more depth.

## What's in the Catalog

- **Basics** — 31 sub-topics: variables, types, strings, control flow, functions, modules, virtual environments, and more.
- **Data Structures** — 14 sub-topics: stack, queue, deque, linked list, doubly linked list, heap (priority queue), trie, graph, Counter, defaultdict, namedtuple, frozenset, plus the existing hash-map and BST pages.
- **Algorithms** — bubble / merge / quicksort, binary search.
- **Pythonic Power Tools** — decorators, generators, context managers, asyncio.
- **Standard Library highlights** — JSON, regex, file I/O, email validation.

Every entry has its own permanent URL and its own coding challenge.

## How Challenges Work

Challenges run **in your browser** — no server-side code execution, so the project can stay simple and your code stays private.

- Each challenge is `{prompt, starter_code, tests}`, defined in `challenges_data.py`.
- The UI shows the prompt, a monospace editor pre-filled with starter code, and a Run Tests button.
- Clicking Run lazy-loads [Pyodide](https://pyodide.org/) (~10 MB, one-time, cached afterward), then runs each test in a fresh Python globals dict so tests can't contaminate each other.
- Results render as a list of green checks / red crosses with the failing assertion message when something's off.
- Cmd / Ctrl + Enter inside the editor also triggers a run. Reset rolls back to starter code.

## The AI Fallback

Two places Claude gets called, both gated behind login:

1. **Home page search bar.** Type a question, get a custom Markdown lesson with a primary code snippet and 3-4 related-topic suggestions.
2. **Follow-up buttons + bottom search on lesson pages.** The four default follow-ups ("Explain more", "Why do I need this?", "Show a real example", "Common pitfalls") are pre-baked prompts that include the topic name. The "Ask anything else..." input lets the user phrase their own follow-up. Answers append below the lesson as stacked cards so the conversation history stays visible.

## Tech Stack

- **Backend:** Python 3.9+, Flask, Flask-Login, Flask-SQLAlchemy (SQLite by default).
- **AI:** Anthropic Claude API via the `anthropic` Python SDK.
- **In-browser code execution:** [Pyodide](https://pyodide.org/) loaded from jsDelivr.
- **Frontend:** Jinja templates + Tailwind CSS via CDN, Space Grotesk + JetBrains Mono fonts, Material Symbols icons, [marked.js](https://marked.js.org/) for rendering AI-generated Markdown.
- **Auth:** username / password with pbkdf2:sha256 hashing (`werkzeug.security`).

## Project Layout

```
aiCodeGenerator/
├── flask_app.py             # Routes, auth, app setup
├── models.py                # SQLAlchemy User + Generation tables
├── generator.py             # The only place Claude is called from
├── topics.py                # Catalog of canonical topics + sidebar visibility
├── lessons.py               # Markdown loader for lessons/*.md
├── challenges.py            # Loader for challenges_data.py
├── challenges_data.py       # All challenges keyed by lesson slug
├── lessons/                 # 43 hand-authored .md lesson files
│   └── <slug>.md
├── templates/
│   ├── main.html            # Home / lesson page
│   ├── about.html
│   ├── login.html
│   └── signup.html
├── static/
│   └── logo.png             # Pixel-art snake mascot
└── README.md
```

## Running Locally

```bash
# 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate     # macOS / Linux
# .venv\Scripts\activate       # Windows

# 2. Install dependencies
pip install flask flask-sqlalchemy flask-login anthropic werkzeug

# 3. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 4. Run the app
python flask_app.py
# Open http://localhost:5000
```

The first time you run it, an `instance/codegen.db` SQLite file is created automatically. If you ever change the schema in `models.py`, delete that file so SQLAlchemy can rebuild it.

## Adding a New Topic

1. Append an entry to the `TOPICS` list in `topics.py` with a stable slug, name, icon (Material Symbols), level, and description.
2. Create `lessons/<slug>.md` with the lesson body and YAML-ish frontmatter (title, summary, related).
3. (Optional) Add a challenge to `challenges_data.py` under the same slug.
4. (Optional) For sub-topics, add `parent: "<parent-slug>"` and `hide_from_sidebar: True`, then append the slug to the parent topic's `children` list.

That's the whole flow. No backend changes required.

## Status

In active development. The lesson catalog and challenges are stable; the AI tutor and follow-up flows are polished but still being refined.

---

*Created by Daniel Valenzuela | 2026*
