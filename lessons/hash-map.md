---
title: Hash Map
summary: A dictionary built from scratch — hashing, buckets, and how collisions get handled.
related: data-structures, python-dictionaries
---

Python's `dict` is the most-used data structure in the language, and under the hood it's a **hash map**. The idea: convert a key into an integer with a hash function, take that integer modulo the size of an array, and store the value at that index. Lookups become O(1) on average.

The trick is what to do when two different keys hash to the same bucket. The most common fix is **chaining**: each bucket holds a small list of `(key, value)` pairs, and we linear-scan that list.

## A minimal hash map

```python
class HashMap:
    def __init__(self, capacity: int = 16):
        self._capacity = capacity
        self._buckets: list[list[tuple]] = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key) -> list[tuple]:
        return self._buckets[hash(key) % self._capacity]

    def put(self, key, value) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)   # update existing
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def __contains__(self, key) -> bool:
        return any(k == key for k, _ in self._bucket(key))

    def __len__(self) -> int:
        return self._size
```

## Try it

```python
h = HashMap()
h.put("apple", 1.20)
h.put("bread", 3.50)
print(h.get("apple"))   # 1.20
print("milk" in h)      # False
```

## What we left out

A real hash map (like Python's `dict`) also:

- **Resizes** automatically once the load factor gets high (usually around 0.66) to keep operations O(1).
- Handles collisions with **open addressing** instead of chaining in CPython, which is more cache-friendly.
- Computes hashes once and stores them inside each entry to skip recomputing on resize.

For a deeper look at how built-in containers compare, see [Data Structures](/lesson/data-structures).

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Whenever you need O(1) lookup by key. Python's built-in `dict` already IS a great hash map.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Building your own from scratch for production — the stdlib `dict` is faster, more memory-efficient, and handles edge cases you'd miss.</p>
</div>

