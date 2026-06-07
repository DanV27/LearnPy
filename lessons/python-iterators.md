---
title: Python Iterators
summary: The protocol behind every for-loop — iter() and next().
related: python-for-loops, generators, python-range
---

An iterator is an object that produces values one at a time on demand. Anything you can put in a `for` loop is **iterable**. The iterator itself is what `for` walks through.

```python
nums = [10, 20, 30]
it = iter(nums)         # get an iterator from the list
next(it)                # 10
next(it)                # 20
next(it)                # 30
next(it)                # raises StopIteration
```

A `for` loop is just sugar around this:

```python
for n in nums:
    print(n)

# is equivalent to:
it = iter(nums)
while True:
    try:
        n = next(it)
    except StopIteration:
        break
    print(n)
```

**Writing your own iterator**:

```python
class CountDown:
    def __init__(self, start: int):
        self.n = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

for x in CountDown(3):
    print(x)            # 3, 2, 1
```

- For most cases, a [generator](/lesson/generators) (`yield`) is much cleaner than a class.
- Iterators are single-use: once exhausted, you have to make a new one.
- `iter()`, `next()`, `StopIteration` are the three pieces of the iterator protocol.
