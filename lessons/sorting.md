---
title: Sorting Algorithms
summary: Bubble, merge, and quicksort — three classic ways to put a list in order.
related: binary-search, data-structures, binary-search-tree
---

Python's built-in `sorted()` is Timsort and is what you should reach for in real code — but writing a few sort algorithms by hand is the clearest way to internalize Big-O.

## Bubble sort — O(n²)

Walk the list comparing adjacent pairs and swapping them if they're out of order. Repeat until no swaps happen.

```python
def bubble_sort(arr: list[int]) -> list[int]:
    arr = arr[:]                       # don't mutate caller's list
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
```

Simple, never use it on anything bigger than ~100 elements.

## Merge sort — O(n log n)

Recursively split the list in half, sort each half, then merge the two sorted halves.

```python
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(a: list[int], b: list[int]) -> list[int]:
    out: list[int] = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out
```

Guaranteed O(n log n) and stable (equal items keep their original order).

## Quicksort — O(n log n) average, O(n²) worst

Pick a pivot, partition the rest into "less than pivot" and "greater than pivot", recurse.

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

In practice quicksort is faster than merge sort because of cache locality, even though merge sort has a better worst case.

## When to write your own

Almost never — use `sorted(arr)` or `arr.sort()`. But once your list is sorted, [Binary Search](/lesson/binary-search) gives you O(log n) lookups, which is the next thing to learn.
