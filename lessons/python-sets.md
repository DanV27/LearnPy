---
title: Python Sets
summary: Unordered collections of unique values — fast membership tests and set algebra.
related: python-lists, python-dictionaries, hash-map
---

A set stores unique, unordered values. Duplicates are automatically removed. Membership tests (`x in s`) are O(1) on average — much faster than a list.

```python
seen = {"alice", "bob"}
seen.add("alice")        # no duplicate added
seen.add("carol")
print(seen)              # {'alice', 'bob', 'carol'}
"bob" in seen            # True
```

**Creating a set**: literal `{...}` or `set(iterable)`. The literal `{}` makes an empty *dict*, so use `set()` for an empty set.

```python
nums = {1, 2, 3}
empty = set()
from_list = set([1, 2, 2, 3])      # {1, 2, 3}
```

**Set operations**:

```python
a = {1, 2, 3}
b = {2, 3, 4}

a | b      # union          {1, 2, 3, 4}
a & b      # intersection   {2, 3}
a - b      # difference     {1}
a ^ b      # symmetric diff {1, 4}
```

**Mutation**:

```python
nums.add(4)
nums.remove(2)        # KeyError if 2 isn't there
nums.discard(99)      # quietly does nothing if missing
nums.update([5, 6])
```

- Sets are unordered: don't rely on iteration order.
- Set elements must be **hashable** — strings, numbers, and tuples are fine; lists and dicts are not.
- For immutable sets (usable as dict keys), use `frozenset`.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Unique items and fast O(1) membership tests.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — When order or duplicates matter — sets are unordered and discard repeats. Don't use `set(items)` to 'tidy' a list.</p>
</div>

