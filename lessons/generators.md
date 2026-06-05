---
title: Generators
summary: Lazy iteration with the yield keyword — compute values one at a time, not all at once.
related: decorators, context-managers, basics
---

A **generator** is a function that produces a stream of values instead of returning one. It pauses at every `yield`, hands the value back to the caller, and resumes from where it left off on the next iteration. The whole sequence is computed lazily — values exist only when something asks for them.

## A function vs. a generator

```python
def squares_list(n: int) -> list[int]:
    return [i * i for i in range(n)]      # builds the whole list upfront

def squares_gen(n: int):
    for i in range(n):
        yield i * i                       # produces one at a time
```

`squares_list(1_000_000)` allocates a million-item list right now. `squares_gen(1_000_000)` allocates basically nothing — it just remembers where it is.

## Iterating

You can use a generator anywhere you'd use a list-like object:

```python
for x in squares_gen(5):
    print(x)            # 0 1 4 9 16

total = sum(squares_gen(1000))
```

You can also pull values one-by-one with `next()`:

```python
g = squares_gen(3)
print(next(g))          # 0
print(next(g))          # 1
print(next(g))          # 4
print(next(g))          # raises StopIteration
```

## Why it matters

- **Memory**: streaming large datasets line-by-line uses constant memory instead of loading everything.
- **Infinite sequences**: `def naturals(): n = 0; while True: yield n; n += 1`. You can't build that as a list, but a generator handles it fine.
- **Composability**: generators chain naturally — pipe one into another and you have a pipeline.

```python
def evens(stream):
    for x in stream:
        if x % 2 == 0:
            yield x
```

## Generator expressions

You can also write a generator inline, much like a list comprehension but with parens:

```python
total = sum(x * x for x in range(1_000_000))
```

That's a generator expression — no intermediate list is built.

When you're ready, see how [Decorators](/lesson/decorators) and [Context Managers](/lesson/context-managers) extend Python's idea of "code that wraps other code".
