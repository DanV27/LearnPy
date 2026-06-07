---
title: Python For Loops
summary: Iterate over anything sequence-like — lists, strings, dicts, files, ranges.
related: python-while-loops, python-range, python-iterators
---

`for` walks over the items of an iterable. The iterable can be a list, tuple, string, dict, set, range, file, generator — anything that supports iteration.

```python
for color in ["red", "green", "blue"]:
    print(color)

for ch in "Hi":
    print(ch)               # 'H' then 'i'

for key, value in {"a": 1, "b": 2}.items():
    print(key, value)
```

**`range` for counting**:

```python
for i in range(5):          # 0, 1, 2, 3, 4
    ...

for i in range(2, 10, 2):   # 2, 4, 6, 8 — start, stop, step
    ...
```

**`enumerate` for index + value**:

```python
for i, item in enumerate(items):
    print(i, item)
```

**`zip` for parallel iteration**:

```python
names = ["Alice", "Bob"]
ages  = [30, 25]
for name, age in zip(names, ages):
    print(f"{name} is {age}")
```

- Use [`break`](/lesson/python-while-loops) to exit early, `continue` to skip an iteration.
- Modifying a list while you iterate it is a classic bug — make a copy with `list(items)` first, or use a [list comprehension](/lesson/python-lists).
- See [Python Range](/lesson/python-range) for the full range() signature.
