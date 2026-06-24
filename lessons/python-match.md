---
title: Python Match
summary: Structural pattern matching — like a switch statement, but smarter (Python 3.10+).
related: python-if-else, python-dictionaries, python-tuples
---

Introduced in Python 3.10, `match` matches a value against a series of *patterns*. It's much more than a switch — patterns can destructure tuples, lists, and dicts.

```python
def http_status(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 301 | 302:
            return "Redirect"
        case 404:
            return "Not Found"
        case 500 | 502 | 503:
            return "Server Error"
        case _:
            return "Unknown"
```

The `_` is a wildcard — it matches anything and binds to nothing. Use it as your fallback.

**Destructuring patterns**:

```python
def describe(point):
    match point:
        case (0, 0):
            return "origin"
        case (0, y):
            return f"y-axis at {y}"
        case (x, 0):
            return f"x-axis at {x}"
        case (x, y):
            return f"point at ({x}, {y})"
```

You can also match dictionaries and class instances:

```python
match user:
    case {"role": "admin", "name": name}:
        print(f"admin: {name}")
    case {"role": "guest"}:
        print("guest")
```

- Match is best when you're branching based on the **shape** of data, not just its value.
- For simple value checks, plain [if/elif/else](/lesson/python-if-else) is often clearer.
- Patterns can include guards: `case x if x > 0: ...`.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Branching on the *shape* of structured data — destructuring while matching is its superpower.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Simple equality checks where `if/elif/else` reads cleaner. Don't reach for `match` just because it's new.</p>
</div>

