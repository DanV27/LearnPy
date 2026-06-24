---
title: Python Casting
summary: Convert a value from one type to another using int(), float(), str(), bool(), etc.
related: python-data-types, python-numbers, python-strings
---

Python's type-conversion functions are named after the target type:

```python
int("42")          # 42
float("3.14")      # 3.14
str(99)            # "99"
bool(0)            # False
bool("anything")   # True
list("abc")        # ['a', 'b', 'c']
```

These are sometimes called *casts*, though they're really constructors — each one creates a new value of the target type from the input.

**Common gotchas**:

```python
int("3.14")        # ValueError — int() doesn't accept decimal strings
int(float("3.14")) # 3 — go through float first
int("  42 ")       # 42 — int() trims whitespace
bool("False")      # True — any non-empty string is truthy!
```

Falsy values in Python: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`. Everything else is truthy.

- Use `int(x, base)` to parse non-decimal: `int("ff", 16)` returns 255.
- `str(x)` always succeeds. `int(x)` and `float(x)` can raise — wrap user input in try/except.
- See [Python Booleans](/lesson/python-booleans) for the truthiness rules in detail.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Casting explicit user input or external data into the type your logic expects.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Casting blindly without try/except — `int('oops')` raises ValueError and can crash your program.</p>
</div>

