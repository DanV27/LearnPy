---
title: JSON
summary: Parse and emit JSON with Python's built-in json module.
related: file-io, basics, regex
---

JSON is the lingua franca of web APIs and config files. Python's standard library has a `json` module that handles both directions — turning JSON text into Python objects and vice versa.

## The two functions you'll use 90% of the time

```python
import json

text = '{"name": "Alice", "tags": ["python", "flask"], "active": true}'

# JSON string -> Python object
data = json.loads(text)
print(data["name"])             # Alice
print(data["tags"][0])          # python
print(data["active"])           # True

# Python object -> JSON string
out = json.dumps(data, indent=2)
print(out)
```

`json.loads` reads from a string. `json.load` reads from a file object. Same for `dumps` / `dump`. The trailing `s` always means "string".

## Reading and writing files

```python
# Read a JSON file
with open("config.json") as f:
    config = json.load(f)

# Write one out, pretty-printed
with open("out.json", "w") as f:
    json.dump(config, f, indent=2, sort_keys=True)
```

## Type mapping

JSON's types map cleanly to Python's:

- `"string"` ↔ `str`
- `42` / `3.14` ↔ `int` / `float`
- `true` / `false` ↔ `True` / `False`
- `null` ↔ `None`
- `[ ... ]` ↔ `list`
- `{ ... }` ↔ `dict`

Things that won't round-trip out of the box: `datetime`, `set`, `bytes`, custom classes. For those, pass a `default=...` function to `dumps`:

```python
from datetime import datetime

def serialize(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Cannot serialize {type(o).__name__}")

json.dumps({"created": datetime.now()}, default=serialize)
```

## Handling bad input

`json.loads` raises `json.JSONDecodeError` on malformed input. Always wrap user-supplied JSON in a try/except — never trust that data from outside your program is valid.

```python
try:
    data = json.loads(payload)
except json.JSONDecodeError as e:
    print(f"Bad JSON at line {e.lineno}: {e.msg}")
```

For working with the underlying files, see [File I/O](/lesson/file-io). For more strict parsing patterns, see [Regular Expressions](/lesson/regex).
