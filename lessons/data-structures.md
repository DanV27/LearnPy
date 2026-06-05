---
title: Data Structures
summary: List, dict, set, tuple — when to use each, and what they're good at.
related: basics, hash-map, sorting
---

Python ships with four built-in collection types, and choosing between them is mostly about whether you need order, uniqueness, or fast lookups.

## list — ordered, mutable

Use a list when order matters and you'll add or remove items.

```python
todos = ["water plants", "write tests"]
todos.append("ship it")
todos[0] = "water plants 🌱"
```

Indexing is O(1). Searching with `x in todos` is O(n). Inserting at the front is slow; appending to the end is fast.

## dict — key → value, fast lookups

A dict maps keys to values and lookups are O(1) on average. Use it whenever you'd reach for "lookup by name":

```python
prices = {"apple": 1.20, "bread": 3.50}
prices["milk"] = 2.99
print(prices.get("eggs", 0.0))  # default if missing
```

Iterating gives you keys; use `.items()` for `(key, value)` pairs.

## set — unique values, fast membership

A set is an unordered collection of unique values. Membership checks are O(1):

```python
seen = {"alice", "bob"}
seen.add("alice")            # no duplicate
print("bob" in seen)         # True
```

Sets support union (`|`), intersection (`&`), and difference (`-`).

## tuple — immutable, lightweight

Tuples are like lists but you can't change them after creation. Use them for fixed records or as dict keys.

```python
point = (3, 4)
x, y = point                 # tuple unpacking
```

Because they're immutable, tuples can be hashed — meaning they can be used as dict keys or set elements, which lists can't.

## Picking the right one

- "I need an ordered list of things I'll modify" → **list**
- "I need to look something up by a key" → **dict**
- "I just need to know if I've seen this before" → **set**
- "These belong together and won't change" → **tuple**

Once you've mastered these, look at how a [Hash Map](/lesson/hash-map) is built under the hood, or jump to [Sorting Algorithms](/lesson/sorting) for what happens when you put a list in order.
