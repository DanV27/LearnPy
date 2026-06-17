---
title: Sliding Window
summary: A moving range over a sequence — slides one element at a time, tracking only what's inside the window.
related: two-pointers, big-o-notation, deque
---

The **sliding window** pattern maintains a "window" of consecutive elements that slides across a sequence. Instead of recomputing the answer from scratch at every position, you add the new element entering on the right and remove the one leaving on the left. That gives `O(n)` instead of `O(n × window_size)`.

## Fixed-size window

Max sum of any 3 consecutive elements:

```python
def max_window_sum(nums: list[int], k: int) -> int:
    if len(nums) < k:
        return 0
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]   # slide: add new, remove old
        best = max(best, window)
    return best

max_window_sum([1, 4, 2, 10, 23, 3, 1, 0, 20], 4)    # 39  (2+10+23+3 or 10+23+3+1...)
```

One pass, constant work per step. `O(n)`.

## Variable-size window

Longest substring without repeating characters:

```python
def longest_unique(s: str) -> int:
    seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1          # shrink window past the dup
        seen[ch] = right
        best = max(best, right - left + 1)
    return best

longest_unique("abcabcbb")    # 3 ("abc")
longest_unique("bbbbb")       # 1 ("b")
```

The window grows on the right, shrinks on the left when a duplicate forces it to. Still `O(n)` because each character is added and removed at most once.

## When to spot it

- "Longest / shortest subarray with property X."
- "Maximum / minimum sum over a window of size k."
- "Number of substrings that satisfy ..."

If you find yourself looping over every starting position and then every ending position, you probably want sliding window instead. It's the sibling pattern of [Two Pointers](/lesson/two-pointers) — same mindset, different shape.
