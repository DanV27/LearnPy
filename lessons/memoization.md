---
title: Memoization
summary: Cache the result of expensive function calls so you don't redo the same work twice.
related: recursion, big-o-notation, defaultdict
---

**Memoization** is a fancy word for "remember the answer". You wrap a function so that the first time it's called with a particular input, it computes the result and stores it. Every subsequent call with the same input returns the cached value instantly.

It's the foundation of dynamic programming, and it turns many exponentially slow recursive algorithms into linear-time ones.

## The naïve recursive Fibonacci is O(2ⁿ)

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

fib(35)    # works but takes seconds
fib(50)    # don't try this
```

It recomputes the same `fib(k)` values an exponential number of times. Memoization fixes it in one line:

## With `functools.lru_cache`

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

fib(100)    # instant
```

Same function, `O(n)` instead of `O(2ⁿ)`. The decorator stores `(args) → result` in a dict and intercepts repeat calls.

## Memoizing by hand

When you can't use a decorator (you want explicit control, or the cache shape is non-standard):

```python
cache = {}

def fib(n):
    if n in cache:
        return cache[n]
    if n < 2:
        cache[n] = n
    else:
        cache[n] = fib(n - 1) + fib(n - 2)
    return cache[n]
```

## When it helps

Memoization is only useful if:

- The function is **pure** (same inputs always produce same output).
- The inputs are **hashable** (so they can be dict keys).
- The same inputs **actually repeat** during execution.

If those three conditions hold and the function is slow, memoization is almost always a free speedup.

The next step up from memoization is bottom-up dynamic programming — same idea, but building the cache iteratively from the smallest sub-problem up. Reach for that when [recursion](/lesson/recursion) depth becomes a problem.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Pure functions with repeated calls on the same inputs — recursive DP, expensive computations, repeated API calls.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Functions with side effects, large unique input spaces (cache balloons), or time-dependent logic (`now()` will be wrong).</p>
</div>

