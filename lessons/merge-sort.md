---
title: Merge Sort
summary: Split the list in half, sort each half recursively, merge them back together — guaranteed O(n log n).
related: quicksort, recursion, big-o-notation
---

Merge sort is the canonical "divide and conquer" algorithm. Split the list in two, sort each half (recursively), then merge the two sorted halves into one sorted list. Always `O(n log n)`, always stable, predictable to the millisecond.

```python
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(a: list[int], b: list[int]) -> list[int]:
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out
```

## Complexity

- **Time: O(n log n)** always — best, worst, average.
- **Space: O(n)** — needs an auxiliary list for the merges.
- **Stable** — equal elements keep their original order, which matters when sorting by multiple keys.

## Merge sort vs. quicksort

[Quicksort](/lesson/quicksort) has better cache behavior and is usually faster in practice on random data. But it can degrade to `O(n²)` on pathological inputs. Merge sort is slower on average but never gets surprised.

Python's `sorted()` uses Timsort, which is essentially a hybrid of merge sort + insertion sort tuned for real-world data (which is rarely random — it's usually partially sorted).

## When you'd reach for merge sort by hand

- You're sorting linked lists (no random access → quicksort's pivot logic is awkward, merge sort is natural).
- You need a stable sort and your language doesn't give you one.
- You're sorting data that doesn't fit in memory — merge sort generalizes to external sorting on disk.
