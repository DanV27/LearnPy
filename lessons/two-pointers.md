---
title: Two Pointers
summary: A pattern, not an algorithm. Walk a sequence from both ends (or the same end at different speeds) to solve in O(n).
related: sliding-window, binary-search, linear-search
---

The **two pointers** pattern uses two indices that walk a sequence together, often from opposite ends. It turns many problems that look `O(n²)` into `O(n)` — no nested loop, just one pass with two cursors.

## Classic example: pair sum on a sorted list

```python
def has_pair_with_sum(nums: list[int], target: int) -> bool:
    """True if any two distinct elements of `nums` sum to `target`."""
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return True
        elif s < target:
            left += 1            # need a bigger sum → move left up
        else:
            right -= 1           # need a smaller sum → move right down
    return False

has_pair_with_sum([1, 3, 4, 7, 11], 11)    # True (4 + 7)
```

One pass through the list — that's `O(n)`. The nested-loop version would be `O(n²)`.

## Common cases

- **Sorted input + look for a pair.** Sum, difference, or ratio — start at both ends.
- **Reverse a string in place.** Swap, move pointers toward center.

```python
def reverse_chars(s: list[str]) -> None:
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
```

- **Remove duplicates from a sorted list in place.** One pointer reads, one writes.
- **Fast/slow pointers** for cycle detection: one moves 1 step, one moves 2. If they meet, there's a cycle.

## When to recognize the pattern

Look for: a **sorted** sequence, a problem asking about pairs / sums / endpoints, or a need to compress / dedup in place. If you reach for a nested loop, ask first whether two pointers could collapse it to one pass.

For windows of varying size moving across a sequence, the sibling pattern is [Sliding Window](/lesson/sliding-window).

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Sorted-array problems involving pairs, palindromes, or in-place compaction.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Unsorted data — most two-pointer tricks assume order. Sort first or pick a different pattern.</p>
</div>

