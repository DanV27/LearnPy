---
title: frozenset
summary: An immutable set — same operations as a set, but hashable and safe to use as a dict key.
related: hash-map, counter, defaultdict
---

A regular [set](/lesson/python-sets) is mutable: you can add and remove items. A `frozenset` is the immutable version. Once created, you can't change it — and that's the whole point.

```python
fs = frozenset([1, 2, 3])
fs.add(4)                # AttributeError — frozensets have no .add
```

You can still use all the read-only set operations:

```python
a = frozenset([1, 2, 3])
b = frozenset([2, 3, 4])

a | b                    # frozenset({1, 2, 3, 4})
a & b                    # frozenset({2, 3})
a - b                    # frozenset({1})
2 in a                   # True
```

**Why immutability matters**:

Because a `frozenset` is immutable, it's **hashable**, which means you can:

- Use one as a **dict key**:

  ```python
  cache: dict[frozenset, str] = {}
  cache[frozenset({"alice", "bob"})] = "engineering"
  cache[frozenset({"carol"})] = "sales"
  ```

  A regular set won't work — Python raises `TypeError: unhashable type: 'set'`.

- Put one inside another set: a "set of sets" needs the inner sets to be hashable.

  ```python
  groups = {frozenset({1, 2}), frozenset({3, 4})}
  ```

**Real-world uses**:

- Cache keys based on a *set* of inputs (e.g. "users in a chat room").
- Representing equivalence classes that you compare for equality.
- Any "this collection of things won't change" record.

For mutable, growable sets, stick with `set`. Reach for `frozenset` when hashability or "guaranteed not to change" is a feature, not a limitation.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — As a dict key or set element when you need a 'set of things that won't change.'</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — For mutable working data — you can't add or remove. Use a regular set for that.</p>
</div>

