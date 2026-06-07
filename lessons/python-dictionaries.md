---
title: Python Dictionaries
summary: Key-value mappings with O(1) lookup — Python's most-used data structure.
related: python-sets, python-lists, hash-map
---

A dict maps **keys** to **values**. Lookups, insertions, and deletions are all O(1) on average. Keys must be hashable (strings, numbers, tuples — not lists or other dicts).

```python
prices = {"apple": 1.20, "bread": 3.50, "milk": 2.99}
prices["apple"]          # 1.20
prices["eggs"] = 4.50    # add or update
del prices["bread"]      # delete
"milk" in prices         # True
```

**Safe lookup**:

```python
prices.get("rice")              # None (no KeyError)
prices.get("rice", 0.0)         # 0.0 (default)
prices.setdefault("oats", 2.0)  # set if missing, return value
```

**Iterating**:

```python
for key in prices:                 # keys (default)
    print(key)

for key, value in prices.items():  # both at once
    print(key, "=", value)

for value in prices.values():
    print(value)
```

**Dict comprehensions** — like list comprehensions, but emit key:value pairs:

```python
squares = {n: n*n for n in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

- Dicts remember insertion order (Python 3.7+).
- Use `dict.keys()`, `.values()`, `.items()` for views that stay in sync with the dict.
- For more on how dicts work under the hood, see [Hash Map](/lesson/hash-map).
