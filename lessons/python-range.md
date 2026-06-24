---
title: Python Range
summary: range() generates a sequence of integers — the go-to for counting in for-loops.
related: python-for-loops, python-iterators, python-lists
---

`range()` produces a sequence of integers. It comes in three forms:

```python
range(stop)              # 0, 1, ..., stop-1
range(start, stop)       # start, start+1, ..., stop-1
range(start, stop, step) # start, start+step, ..., stop (exclusive)
```

Examples:

```python
list(range(5))            # [0, 1, 2, 3, 4]
list(range(2, 7))         # [2, 3, 4, 5, 6]
list(range(0, 10, 2))     # [0, 2, 4, 6, 8]
list(range(10, 0, -1))    # [10, 9, 8, ..., 1]   — counting down
```

You'll usually use it in a `for` loop:

```python
for i in range(10):
    print(i)
```

**`range` is lazy** — it doesn't build a list in memory. It generates each number on demand, so `range(1_000_000_000)` is cheap. Wrap it in `list(...)` only when you actually need the list.

```python
import sys
sys.getsizeof(range(10**9))     # 48 bytes — same as range(10)
sys.getsizeof(list(range(10**9))) # would crash your machine
```

- `step` must be non-zero. `range(5, 0)` (no step) gives an empty range — Python won't count down for you implicitly.
- Use [`enumerate`](/lesson/python-for-loops) instead of `range(len(items))` when you need an index AND the item.
- For non-integer counting (e.g., `0.0, 0.1, 0.2, ...`), use numpy or a comprehension.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Generating integer sequences for `for` loops without building a list in memory.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — For float steps — `range(0, 1, 0.1)` raises TypeError. Use `numpy.arange` or a comprehension.</p>
</div>

