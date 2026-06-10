---
title: Regular Expressions
summary: Match patterns in text with the re module — search, capture, and replace.
related: json, basics, python-strings
---

A **regular expression** is a small language for describing patterns in text. Python's `re` module is how you use them. They're powerful and easy to overuse — when something simpler would do (like `str.startswith` or `str.split`), reach for that first.

## The four functions you'll use

```python
import re

text = "Order #1023 placed on 2026-06-03 for $42.50"

# Find the first match (returns a Match object or None)
m = re.search(r"#(\d+)", text)
print(m.group(1))                       # "1023"

# Match must start at the beginning
re.match(r"Order", text)                # match
re.match(r"placed", text)               # None

# Find every non-overlapping match
nums = re.findall(r"\d+", text)         # ['1023', '2026', '06', '03', '42', '50']

# Replace
masked = re.sub(r"\$\d+\.\d+", "$***", text)
```

## Common patterns

| Pattern | Means |
|---|---|
| `\d` | A digit |
| `\w` | Word character (letter, digit, underscore) |
| `\s` | Whitespace |
| `.` | Any character except newline |
| `*` | 0 or more |
| `+` | 1 or more |
| `?` | 0 or 1 |
| `{3,5}` | Between 3 and 5 |
| `^` / `$` | Start / end of string |
| `(...)` | Capture group |
| `(?:...)` | Non-capturing group |
| `[abc]` | Any one of a, b, c |
| `[^abc]` | Not a, b, or c |

## Always use raw strings

Use `r"..."` instead of `"..."` so backslashes don't get eaten by Python's string escaping:

```python
re.search(r"\bword\b", text)            # good
re.search("\\bword\\b", text)           # equivalent but ugly
```

## Compiling for speed

If you use the same pattern many times, compile it once:

```python
ORDER_RE = re.compile(r"#(\d+)")
for line in lines:
    m = ORDER_RE.search(line)
    ...
```

## A worked example: parsing log lines

```python
import re

log_re = re.compile(r"\[(\w+)\]\s+(\S+)\s+(.+)")

line = "[ERROR] auth.py Failed to connect"
m = log_re.match(line)
if m:
    level, source, message = m.groups()
    print(level, source, message)
```

When you're done here, revisit [Python Strings](/lesson/python-strings) if string slicing would have been enough, or read [JSON](/lesson/json) for another common parsing pattern.
