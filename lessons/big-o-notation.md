---
title: Big O Notation
summary: How to talk about how fast or slow code is — without timing it.
related: recursion, linear-search, binary-search
---

Big O notation is how programmers describe the *worst-case* growth rate of an algorithm as its input size grows. It's not about clock time on your machine — it's about how the number of operations scales when `n` doubles, or grows a million-fold.

## The common growth rates

| Notation       | Name                | What doubles n does                   |
|----------------|---------------------|---------------------------------------|
| **O(1)**       | constant            | nothing — same number of steps        |
| **O(log n)**   | logarithmic         | one more step                         |
| **O(n)**       | linear              | doubles the work                      |
| **O(n log n)** | linearithmic        | a bit more than doubles               |
| **O(n²)**      | quadratic           | quadruples the work                   |
| **O(2ⁿ)**      | exponential         | doubles the work *again*, on top of n |

```python
# O(1) — looking up a dict key
prices = {"apple": 1.2, "bread": 3.5}
prices["apple"]                       # constant time

# O(n) — scanning a list
def contains(items, target):
    for x in items:
        if x == target:
            return True
    return False

# O(n²) — nested loops over the same list
def has_duplicate(items):
    for i, a in enumerate(items):
        for j, b in enumerate(items):
            if i != j and a == b:
                return True
    return False
```

## Rules of thumb

- Drop constants. `O(2n)` is just `O(n)`. We care about *growth*, not exact step count.
- Drop the smaller term. `O(n² + n)` is `O(n²)` — the n² eats the n once n is big.
- Loops over the input → at least `O(n)`. Nested loops → at least `O(n²)`. Halving the search → `O(log n)`.

Big O tells you when an algorithm will get unusable as data grows. A bubble sort on 10 items is fine. On a million items it will time out forever. Knowing the difference up front is half the skill.
