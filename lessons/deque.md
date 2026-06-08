---
title: Deque
summary: Double-ended queue from collections — O(1) appends and pops at both ends.
related: queue, stack, linked-list
---

`collections.deque` ("deck") is a doubly-linked-list-backed sequence that supports fast appends and pops from **both ends**. It can act as a stack, a queue, or both at once.

```python
from collections import deque

d = deque([1, 2, 3])
d.append(4)              # → deque([1, 2, 3, 4])
d.appendleft(0)          # → deque([0, 1, 2, 3, 4])
d.pop()                  # → 4
d.popleft()              # → 0
```

All four end-operations are O(1). Indexing into the middle is O(n) though, so deques aren't a list replacement when you need random access.

**Bounded deques** — perfect for "last N" buffers:

```python
recent = deque(maxlen=3)
for x in [1, 2, 3, 4, 5]:
    recent.append(x)
print(recent)            # deque([3, 4, 5], maxlen=3)
```

When you exceed `maxlen`, the oldest item falls off the other end automatically.

**Rotation** — shift items around the deque:

```python
d = deque([1, 2, 3, 4, 5])
d.rotate(2)              # → deque([4, 5, 1, 2, 3])
d.rotate(-1)             # → deque([5, 1, 2, 3, 4])
```

**When to reach for it**:

- Building a [stack](/lesson/stack) or [queue](/lesson/queue).
- Sliding window algorithms (use `maxlen` to keep the last N).
- Round-robin scheduling.

For thread-safe variants, see `queue.Queue` and `queue.LifoQueue`.
