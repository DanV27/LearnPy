---
title: Quicksort
summary: Pick a pivot, partition the rest into "less than" and "greater than", recurse. Fast in practice.
related: merge-sort, recursion, big-o-notation
---

Quicksort is the workhorse sort of the production world. It's `O(n log n)` average, sorts in place, and has excellent cache behavior — usually faster than merge sort in practice. The trade-off: worst case is `O(n²)` if you pick bad pivots.

```python
def quicksort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)
```

That's the readable version — uses extra memory. A production quicksort partitions in place using the Lomuto or Hoare scheme.

## Complexity

- **Time average: O(n log n)** — balanced partitions.
- **Time worst: O(n²)** — already-sorted input with naïve pivot choice (always picking first/last).
- **Space: O(log n)** for the recursion stack (in-place version).

## How to dodge the worst case

- **Pick the middle element**, not the first or last — already-sorted input no longer breaks you.
- **Random pivot.** Most std-lib implementations do this. Pathological inputs become probabilistic instead of deterministic.
- **Median-of-three.** Take the median of the first, middle, and last elements as the pivot.

## Quicksort vs. merge sort

| Property | Quicksort | [Merge Sort](/lesson/merge-sort) |
|---|---|---|
| Avg time | O(n log n) | O(n log n) |
| Worst | O(n²) | O(n log n) |
| Space | O(log n) | O(n) |
| Stable | No | Yes |
| Cache-friendly | Yes | Less so |

Use Python's `sorted()` in real code — it's Timsort, which beats both. Knowing quicksort is interview prep, not implementation prep.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — General-purpose sorting where average performance matters more than worst-case.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — When worst-case `O(n²)` is unacceptable (real-time systems, untrusted input). Use merge sort or `sorted()` for guaranteed `O(n log n)`.</p>
</div>

