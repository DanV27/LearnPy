---
title: Python Tuples
summary: Like lists, but immutable. Lightweight, hashable, and great for fixed records.
related: python-lists, python-sets, data-structures
---

A tuple is an ordered, immutable sequence. You can't change a tuple after creation — no append, no insert, no item assignment.

```python
point = (3, 4)
colors = ("red", "green", "blue")
single = (42,)        # the trailing comma is required for a 1-tuple
empty = ()
```

Tuples support the same indexing and slicing as lists:

```python
point[0]              # 3
point[-1]             # 4
colors[1:]            # ('green', 'blue')
```

**Tuple unpacking** is one of Python's nicest features:

```python
x, y = point
first, *rest = (1, 2, 3, 4)    # first=1, rest=[2, 3, 4]

# Swap two variables with no temp:
a, b = b, a
```

Functions that conceptually return multiple values usually return a tuple:

```python
def divmod_(a, b):
    return a // b, a % b
quotient, remainder = divmod_(17, 5)
```

**When to use a tuple over a list**:

- The data won't change (coordinates, RGB colors, database rows).
- You want to use it as a dict key or set element — tuples are hashable, lists aren't.
- You want to signal "this is a fixed record" to readers.

```python
locations = {(0, 0): "origin", (1, 1): "diagonal"}    # ✓
locations = {[0, 0]: "origin"}                         # TypeError
```
