---
title: Bubble Sort
summary: Walk the list comparing adjacent pairs and swapping when out of order. Simple, slow, instructive.
related: selection-sort, insertion-sort, big-o-notation
---

Bubble sort is the textbook starter sort. The idea: compare each pair of adjacent elements, swap if they're out of order, repeat until no swaps happen. Each pass "bubbles" the largest unsorted element to the end.

```python
def bubble_sort(arr: list[int]) -> list[int]:
    arr = arr[:]                          # don't mutate the caller's list
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:                   # early exit on already-sorted
            break
    return arr
```

## Complexity

- **Time: O(n²)** — nested loops over the input.
- **Best case: O(n)** with the early-exit check above, on already-sorted input.
- **Space: O(1)** — sorts in place.

## When to use it

Honestly? Almost never in production. Python's built-in `sorted()` is Timsort, which is `O(n log n)` and dramatically faster on real data. Bubble sort is here because:

- It's the easiest sort to understand and implement.
- It teaches you how to think about loops, swaps, and stopping early.
- It's a warm-up before tackling [Merge Sort](/lesson/merge-sort) and [Quicksort](/lesson/quicksort), which are actually fast.

```python
sorted([3, 1, 4, 1, 5, 9, 2, 6])    # [1, 1, 2, 3, 4, 5, 6, 9] — the real answer
```

For other simple `O(n²)` alternatives that are slightly smarter, see [Selection Sort](/lesson/selection-sort) and [Insertion Sort](/lesson/insertion-sort). All three are educational; none are what you'd actually ship.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Teaching, interview practice, sorting truly tiny lists.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Production code — Python's built-in `sorted()` (Timsort) is 100x+ faster on real data.</p>
</div>

