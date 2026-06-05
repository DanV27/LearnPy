---
title: File I/O
summary: Reading and writing files with open(), context managers, and the right modes.
related: context-managers, json, basics
---

File I/O in Python is built around one function: `open()`. It returns a file object you can read from, write to, or iterate. The standard pattern wraps it in a `with` block so the file gets closed automatically — even if something raises mid-way.

## Reading a file

```python
# Whole file as one string
with open("notes.txt", encoding="utf-8") as f:
    text = f.read()

# Line by line — streams, doesn't load it all into memory
with open("big.log", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip())            # strip the trailing newline

# As a list of lines
with open("notes.txt", encoding="utf-8") as f:
    lines = f.readlines()
```

Always specify `encoding="utf-8"` unless you have a strong reason not to. The default depends on your operating system and will burn you on Windows.

## Writing a file

```python
# Overwrite (creates if missing)
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.writelines(["second\n", "third\n"])

# Append instead of overwrite
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("new entry\n")
```

## The modes

| Mode | Meaning |
|---|---|
| `"r"` | Read (default). File must exist. |
| `"w"` | Write. Truncates if the file exists, creates if not. |
| `"a"` | Append. Creates if not. Existing content is preserved. |
| `"x"` | Exclusive create. Fails if file already exists. |
| `"b"` | Binary mode. Combine with the above (`"rb"`, `"wb"`). |

Use `"rb"` / `"wb"` when reading or writing non-text files (images, pdfs, archives).

## Paths the modern way — pathlib

```python
from pathlib import Path

p = Path("data/users.json")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('{"alice": 1}', encoding="utf-8")
data = p.read_text(encoding="utf-8")
```

`pathlib.Path` handles the OS differences for you — forward slashes on Linux/Mac, backslashes on Windows. It also gives you `.exists()`, `.is_file()`, `.glob("*.txt")`, `.unlink()`, and more.

## Don't forget cleanup

The `with` statement is what guarantees `f.close()` runs even if your code raises. Skipping it leaks file handles. If `with` blocks feel new, [Context Managers](/lesson/context-managers) explains exactly what's happening behind the scenes.

For working with structured data files specifically, see [JSON](/lesson/json).
