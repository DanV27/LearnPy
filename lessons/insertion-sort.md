---
title: Insertion Sort
summary: Build the sorted result one element at a time, like sorting a hand of cards.
related: bubble-sort, selection-sort, merge-sort
---

Insertion sort is how most people sort playing cards by hand. You walk through the list and, for each element, slide it left until it's in the right spot relative to the elements before it.

```python
def insertion_sort(arr: list[int]) -> list[int]:
    arr = arr[:]
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        # Shift larger elements one position right
        while j >= 0 and arr[j] > current:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr
```

## Walk-through

`[5, 2, 4, 6, 1, 3]`:

- i=1: take 2, shift past 5 → `[2, 5, 4, 6, 1, 3]`
- i=2: take 4, shift past 5 → `[2, 4, 5, 6, 1, 3]`
- i=3: take 6, already in place → `[2, 4, 5, 6, 1, 3]`
- i=4: take 1, shift past 6, 5, 4, 2 → `[1, 2, 4, 5, 6, 3]`
- i=5: take 3, shift past 6, 5, 4 → `[1, 2, 3, 4, 5, 6]`

## Complexity

- **Time: O(n²)** worst case, **O(n)** on already-sorted input.
- **Space: O(1)** — sorts in place.

## Where it shines

Of the three `O(n²)` sorts ([bubble](/lesson/bubble-sort), [selection](/lesson/selection-sort), insertion), insertion is usually the fastest on:

- Small lists (under ~50 elements).
- Lists that are already mostly sorted.

Python's Timsort actually *uses* insertion sort as a sub-routine — it switches to insertion sort for small chunks because the constant factors are tiny. This is the only one of the three you'd ever see inside production code.
