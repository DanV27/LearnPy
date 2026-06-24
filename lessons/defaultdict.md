---
title: defaultdict
summary: A dict that creates a default value for missing keys, instead of raising KeyError.
related: counter, namedtuple, hash-map
---

`collections.defaultdict` is a `dict` subclass that calls a "factory" function whenever you read a key that doesn't exist yet. It saves a ton of `if key not in d: d[key] = ...` boilerplate.

The most common pattern: grouping items.

```python
from collections import defaultdict

people = [("engineering", "alice"), ("sales", "bob"), ("engineering", "carol")]

by_team: dict[str, list[str]] = defaultdict(list)
for team, name in people:
    by_team[team].append(name)

print(dict(by_team))
# {'engineering': ['alice', 'carol'], 'sales': ['bob']}
```

The factory `list` returns an empty list whenever a new key is accessed. Compare to plain dict:

```python
by_team = {}
for team, name in people:
    if team not in by_team:
        by_team[team] = []
    by_team[team].append(name)
```

Same result, more code.

**Common factory types**:

```python
defaultdict(int)         # missing keys default to 0  — handy for counts
defaultdict(list)        # missing keys default to [] — handy for grouping
defaultdict(set)         # missing keys default to set() — for unique groupings
defaultdict(dict)        # nested dicts
```

**Counting with defaultdict(int)**:

```python
counts = defaultdict(int)
for word in "the cat sat on the mat".split():
    counts[word] += 1
```

For pure counting, prefer [Counter](/lesson/counter) — it does this plus `most_common`, arithmetic, and a friendlier repr.

**Gotcha**: just *accessing* a missing key in a `defaultdict` creates the entry. If you don't want that side effect, use plain `dict.get(key, default)` instead.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Grouping or counting where you'd otherwise write `if key not in d: d[key] = []`.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — When *reads* shouldn't auto-create keys. `d.get(key, default)` is sometimes what you actually want — defaultdict mutates on read.</p>
</div>

