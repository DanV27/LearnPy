---
title: Python Booleans
summary: True and False are Python's two boolean values. Everything else has a truthiness too.
related: python-if-else, python-operators, python-casting
---

Booleans represent truth values. Python has two: `True` and `False` (both capitalized — `true` is a NameError).

```python
is_open = True
done = False
```

Comparison operators return booleans:

```python
3 > 2            # True
3 == 3.0         # True   — equality across number types
3 is 3           # True   — identity (use `==` for equality, not `is`)
```

**Truthiness** — any value can be evaluated as a boolean in an `if` or `while`:

| Type   | Falsy            | Truthy        |
|--------|------------------|---------------|
| Number | `0`, `0.0`       | Everything else |
| String | `""`             | Any other string |
| List   | `[]`             | Non-empty       |
| Dict   | `{}`             | Non-empty       |
| Set    | `set()`          | Non-empty       |
| None   | `None`           | —             |

```python
if items:                # cleaner than `if len(items) > 0:`
    print("not empty")
```

- `bool` is technically a subclass of `int`: `True == 1`, `False == 0`, and `sum([True, True, False])` is `2`. That's occasionally useful for counting matches.
- `and` / `or` are short-circuiting. `0 or "default"` returns `"default"`.
- `not` flips a boolean. `not items` is True when the list is empty.
