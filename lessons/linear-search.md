---
title: Linear Search
summary: Walk the list one item at a time. Simple, slow, works on anything.
related: binary-search, big-o-notation, two-pointers
---

Linear search is the simplest search there is — walk through the list checking each element until you find what you're looking for (or run out). It works on any iterable, sorted or not.

```python
def linear_search(arr: list, target) -> int:
    """Return the index of target in arr, or -1 if not found."""
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1

linear_search([5, 2, 9, 1, 7], 9)    # 2
linear_search([5, 2, 9, 1, 7], 4)    # -1
```

## Complexity

- **Time: O(n)** — worst case you scan every element.
- **Space: O(1)** — just the loop counter.

## When to use it

- The list is unsorted (sort it first only if you'll search it many times).
- The list is short — for fewer than ~50 items, linear scan beats clever algorithms because there's no setup cost.
- You're searching for a complex condition, not equality: `next(x for x in items if x.score > 90)`.

For sorted lists with many lookups, [Binary Search](/lesson/binary-search) is dramatically faster. For repeated lookups by key, a [hash map](/lesson/hash-map) or `dict` is O(1).

Python's `in` operator on a list is exactly linear search under the hood. So is `list.index()`. Knowing that tells you why `5 in big_list` can be slow — and why `5 in big_set` isn't.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Small lists (< 50 items), unsorted data, or when you only search once.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Repeated searches on large data — sort once and binary-search, or build a dict/set for O(1) lookups.</p>
</div>

