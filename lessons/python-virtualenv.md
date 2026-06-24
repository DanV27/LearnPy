---
title: Python VirtualEnv
summary: Isolated Python environments — each project gets its own packages and versions.
related: python-pip, python-modules, basics
---

A **virtual environment** is a self-contained Python installation: its own interpreter, its own `pip`, and its own folder for installed packages. Each project gets one so you can use different versions of libraries without conflict.

**Create one** (using the built-in `venv` module):

```bash
python -m venv .venv
```

This makes a `.venv/` folder in your project. Add `.venv/` to your `.gitignore` — it's local-only.

**Activate it**:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

While active, your shell prompt usually shows `(.venv)` and `pip install` puts packages into the venv, not your system Python.

**Deactivate**:

```bash
deactivate
```

**Why bother**:

- Project A needs Django 4, Project B needs Django 5 — both can have what they want.
- A typo in `pip install` won't break system tools.
- `pip freeze > requirements.txt` records the exact versions your project depends on.

```bash
pip freeze > requirements.txt
# someone else clones the repo:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Tools like Poetry, pipenv, and `uv` build on top of venvs with extra features. Plain `venv` is enough to get started.
- If you ever see `pip install` errors about "permission denied" or "externally-managed-environment", that's a strong hint you forgot to activate your venv.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Every Python project, from day one. No exceptions.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Skipping it because 'this is just a quick script.' That script becomes production faster than you think.</p>
</div>

