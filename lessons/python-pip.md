---
title: Python PIP
summary: pip is Python's package manager — install, list, and uninstall third-party libraries.
related: python-virtualenv, python-modules, basics
---

`pip` is the command-line tool you use to install packages from the [Python Package Index](https://pypi.org). It comes with Python.

**Install a package**:

```bash
pip install requests
pip install requests==2.31.0       # exact version
pip install "requests>=2.28,<3"    # version range
```

**See what's installed**:

```bash
pip list
pip show requests
```

**Upgrade or remove**:

```bash
pip install --upgrade requests
pip uninstall requests
```

**Freeze your dependencies into a file** — the standard way to share which versions your project uses:

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

**Tips**:

- Always install into a [virtual environment](/lesson/python-virtualenv), not your system Python. That way different projects can use different versions without conflict.
- Use `python -m pip` instead of bare `pip` to be sure you're using the pip tied to the Python you expect.
- On macOS/Linux, if you see permission errors with `pip install`, that's a sign you're installing system-wide — use a virtualenv.

```bash
python -m pip install --upgrade pip   # upgrade pip itself
```

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — `pip install -r requirements.txt` for reproducible installs inside a venv.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — System-wide installs (`sudo pip install`) — you'll break system tools. Always install into a virtual environment.</p>
</div>

