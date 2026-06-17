---
title: Binary Search
summary: Find an item in a sorted list in O(log n) by halving the range each step.
related: linear-search, big-o-notation, merge-sort
---

Binary search is the textbook O(log n) algorithm. The setup: you have a **sorted** list and you want to know whether a value is in it (or where it is). Instead of scanning left to right, you peek at the middle. Too small? Discard the left half. Too big? Discard the right. You can do this 30 times on a list of a billion items.

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
binary_search(nums, 25)    # 4
binary_search(nums, 26)    # -1
```

## Two things to remember

1. **The list MUST be sorted.** Otherwise binary search will silently return wrong answers. Either sort it once (see [Merge Sort](/lesson/merge-sort) or [Quicksort](/lesson/quicksort)) or keep it sorted as you go.
2. **Mind the loop condition.** `low <= high` includes the case where the range has one element left. Using `<` instead is a classic off-by-one bug.

## Where it shows up

Python's `bisect` module gives you battle-tested binary search: `bisect.bisect_left`, `bisect_right`, `insort`. Reach for those before writing your own in real code.

Binary search also appears in unexpected places: "find the smallest x where condition(x) is true" can often be cast as a binary search over the answer space. Once you see the pattern, you'll find it everywhere.
