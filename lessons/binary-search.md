---
title: Binary Search
summary: Find an item in a sorted list in O(log n) by halving the search range each step.
related: sorting, binary-search-tree, hash-map
---

Binary search is the textbook example of an O(log n) algorithm. The setup: you have a **sorted** list and you want to know whether a value is in it (or where it is). Instead of scanning from left to right, you peek at the middle. If it's too small, you discard the left half. If it's too large, you discard the right half. You can do this 30 times on a list of a billion items.

## Iterative implementation

```python
def binary_search(arr: list[int], target: int) -> int:
    """Return the index of target in arr, or -1 if missing."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

## Try it

```python
nums = [1, 3, 7, 14, 25, 31, 42, 56, 78, 99]
print(binary_search(nums, 25))   # 4
print(binary_search(nums, 26))   # -1
```

## Two things to remember

1. **The list MUST be sorted.** If it isn't, binary search will silently return wrong answers. Sort it first with [`sorted()`](/lesson/sorting), or use a data structure that keeps things sorted.
2. **Mind the loop condition.** `low <= high` includes the case where the range has one element left. Using `<` instead is a classic off-by-one bug.

## When to use it

If you'll search a static list many times, sort once and binary-search each time. If the data is changing constantly, a [Hash Map](/lesson/hash-map) gives you O(1) lookups without needing the data to be sorted — usually a better fit. If you need sorted iteration AND fast lookups, a [Binary Search Tree](/lesson/binary-search-tree) is the right shape.

Python's `bisect` module also gives you `bisect_left` and `bisect_right`, which are battle-tested implementations of this same idea.
