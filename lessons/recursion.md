---
title: Recursion
summary: A function that calls itself. Powerful for problems that break into smaller versions of themselves.
related: big-o-notation, memoization, merge-sort
---

A **recursive** function solves a problem by calling itself on a smaller version of the same problem. Every recursion needs two parts: a **base case** (when to stop) and a **recursive case** (how to shrink the problem).

```python
def factorial(n: int) -> int:
    if n <= 1:           # base case
        return 1
    return n * factorial(n - 1)   # recursive case

factorial(5)             # 120
```

Each call sits on the call stack until the base case returns, then unwinds.

## When to reach for it

- Problems that have a clear "smaller version of the same problem" structure: trees, lists, fractals, divide-and-conquer sorts.
- When iteration would require manually managing a stack (you'd just be reimplementing recursion poorly).

## When NOT to

- Python's default recursion limit is 1000. Deep recursions raise `RecursionError`.
- Every recursive call eats stack memory. Iteration is cheaper.
- A simple loop is usually clearer than equivalent recursion. Use recursion when the problem itself is recursive.

## Two classic examples

Reverse a string:

```python
def reverse(s: str) -> str:
    if not s:
        return s
    return reverse(s[1:]) + s[0]
```

Sum a nested list:

```python
def deep_sum(items):
    total = 0
    for x in items:
        if isinstance(x, list):
            total += deep_sum(x)     # recurse into sub-list
        else:
            total += x
    return total

deep_sum([1, [2, [3, 4]], 5])    # 15
```

When the same sub-problems repeat, pair recursion with [Memoization](/lesson/memoization) to avoid recomputing them.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Problems with naturally recursive structure — trees, graphs, divide-and-conquer.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — When recursion depth might exceed ~1000 — Python's default stack limit hits and you get `RecursionError`. Rewrite as iterative.</p>
</div>

