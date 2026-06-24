---
title: Python Lists
summary: Ordered, mutable collections — Python's workhorse data structure.
related: python-tuples, python-dictionaries, python-for-loops
---

A list holds an ordered sequence of items. Lists are mutable: you can add to them, remove from them, and change items in place.

```python
fruits = ["apple", "banana", "cherry"]
fruits[0]                # 'apple'
fruits[-1]               # 'cherry'
fruits[1:3]              # ['banana', 'cherry']  — slicing
len(fruits)              # 3
```

**Modifying lists**:

```python
fruits.append("date")          # add to end
fruits.insert(0, "apricot")    # insert at index
fruits.remove("banana")        # remove first match
last = fruits.pop()            # remove + return last
fruits[1] = "blueberry"        # replace by index
fruits.sort()                  # in-place sort
sorted_copy = sorted(fruits)   # returns a new sorted list
```

**Iterating**:

```python
for fruit in fruits:
    print(fruit)

# with the index too
for i, fruit in enumerate(fruits):
    print(i, fruit)
```

**List comprehensions** — a compact way to build a new list from an iterable:

```python
squares = [n * n for n in range(10)]
evens   = [n for n in range(20) if n % 2 == 0]
```

- Lists can hold mixed types: `[1, "hi", None, [3, 4]]` is valid.
- For fixed-size data that won't change, use a [tuple](/lesson/python-tuples) instead — it's immutable and slightly faster.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Ordered, mutable data where you'll add or remove items frequently.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Fast membership checks — `x in list` is O(n). Use a `set` or `dict` for O(1) lookups.</p>
</div>

