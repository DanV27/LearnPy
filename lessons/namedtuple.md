---
title: namedtuple
summary: A tuple subclass with named fields — perfect for lightweight, immutable records.
related: counter, defaultdict, basics
---

`collections.namedtuple` lets you give a tuple's fields names, so you can read `point.x` instead of `point[0]`. It's a great middle ground between a tuple (too anonymous) and a full class (too heavy) for simple records.

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)

p.x                      # 3
p.y                      # 4
p[0]                     # 3  — still acts as a tuple
x, y = p                 # still unpacks like a tuple
```

You can also create one from a string of space-separated names:

```python
User = namedtuple("User", "id name email")
u = User(1, "Alice", "alice@example.com")
```

**Defaults** (3.7+):

```python
Point = namedtuple("Point", ["x", "y"], defaults=[0])
Point(3)                 # Point(x=3, y=0)
```

**Useful methods**:

```python
p = Point(3, 4)
p._asdict()              # {'x': 3, 'y': 4}
p._replace(x=99)         # Point(x=99, y=4)  — returns a new tuple
Point._fields            # ('x', 'y')
```

**Why use one**:

- **Self-documenting** — calls read `user.email` instead of `user[2]`.
- **Immutable** — like all tuples, namedtuples can't be modified, so they're safe to use as dict keys or set elements.
- **Tiny memory footprint** — almost the same as a plain tuple.

**When to use a real class instead**:

- You need methods on the record (not just data).
- You need mutability.
- For mutable records, `dataclasses.dataclass` is the modern choice. For immutable records, `typing.NamedTuple` is a class-syntax alternative with type annotations.

```python
from typing import NamedTuple
class Point(NamedTuple):
    x: int
    y: int = 0
```
