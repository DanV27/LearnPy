---
title: Selection Sort
summary: Find the smallest remaining element, swap it to the front. Repeat.
related: bubble-sort, insertion-sort, big-o-notation
---

Selection sort is the second textbook sort. Each pass, you find the smallest element in the unsorted portion and swap it into the front of the unsorted portion.

```python
def selection_sort(arr: list[int]) -> list[int]:
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        # Find the index of the smallest element in arr[i:]
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap it into position i
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

## Walk-through

Starting with `[3, 1, 4, 1, 5]`:

1. Smallest in `[3,1,4,1,5]` is `1` (index 1). Swap with position 0 → `[1, 3, 4, 1, 5]`.
2. Smallest in `[3,4,1,5]` is `1` (index 3). Swap with position 1 → `[1, 1, 4, 3, 5]`.
3. Smallest in `[4,3,5]` is `3` (index 3). Swap with position 2 → `[1, 1, 3, 4, 5]`.
4. Already sorted. Done.

## Complexity

- **Time: O(n²)** — for every position, we scan the rest of the list.
- **Space: O(1)** — sorts in place.
- **Swaps: O(n)** — exactly one swap per pass. This matters when swaps are expensive (e.g. writing to disk).

## Bubble vs. selection

Selection sort makes far fewer swaps than [bubble sort](/lesson/bubble-sort) — one per pass vs. potentially many. That doesn't make it asymptotically faster (both are `O(n²)`), but it's a real win when each swap is costly.

Neither is what you'd actually use. For that, see [Merge Sort](/lesson/merge-sort) or [Quicksort](/lesson/quicksort).
