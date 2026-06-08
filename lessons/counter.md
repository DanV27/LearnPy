---
title: Counter
summary: A dict subclass that counts occurrences. Reach for it whenever you'd write a `for x: counts[x] += 1` loop.
related: defaultdict, namedtuple, hash-map
---

`collections.Counter` is a `dict` specialized for counting. You give it an iterable and it tells you how many of each thing showed up.

```python
from collections import Counter

c = Counter("mississippi")
print(c)                 # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
c["i"]                   # 4
c["x"]                   # 0  — never raises KeyError
```

**Most common items**:

```python
words = "the quick brown fox jumps over the lazy dog the end".split()
Counter(words).most_common(3)
# [('the', 3), ('quick', 1), ('brown', 1)]
```

**Set-like math on counters**:

```python
a = Counter(a=3, b=1)
b = Counter(a=1, b=2, c=4)

a + b                    # add counts: Counter({'c': 4, 'a': 4, 'b': 3})
a - b                    # subtract:   Counter({'a': 2})        — negative counts dropped
a & b                    # min:        Counter({'a': 1, 'b': 1})
a | b                    # max:        Counter({'c': 4, 'a': 3, 'b': 2})
```

**Real-world uses**:

- Word-frequency analysis.
- Finding the most common HTTP status code in a log.
- Inventory / vote tallies.
- Detecting anagrams: `Counter("listen") == Counter("silent")`.

```python
def is_anagram(a: str, b: str) -> bool:
    return Counter(a) == Counter(b)
```

For a `dict` that auto-fills missing keys with something *other* than zero (like an empty list), see [defaultdict](/lesson/defaultdict).
