---
title: Decorators
summary: Wrap a function with extra behavior using the @ syntax.
related: generators, context-managers, basics
---

A **decorator** is a function that takes another function and returns a new one. Python has special syntax for it — the `@decorator` line above a function definition — which makes it look like a feature, but it's really just function composition.

## The @ syntax is sugar

```python
def shout(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        return result.upper()
    return wrapper

@shout
def greet(name: str) -> str:
    return f"hello, {name}"

print(greet("world"))   # HELLO, WORLD
```

The `@shout` line is exactly equivalent to writing `greet = shout(greet)` after the function definition. That's the whole magic.

## A practical example: timing

```python
import time
from functools import wraps

def timed(fn):
    @wraps(fn)                          # preserves fn's name and docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{fn.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timed
def slow_add(a: int, b: int) -> int:
    time.sleep(0.1)
    return a + b
```

`@wraps(fn)` from `functools` is important — without it, the decorated function loses its real name, docstring, and signature, which breaks tools like Sphinx and IDEs.

## Where you'll meet decorators

- `@property` turns a method into an attribute.
- `@staticmethod` / `@classmethod` change how methods are bound.
- Web frameworks like Flask use `@app.route("/path")` to register handlers.
- Test frameworks use `@pytest.fixture` and `@pytest.mark.parametrize`.

Once decorators click, [Generators](/lesson/generators) and [Context Managers](/lesson/context-managers) are the next two language features that use a similar "wrap something with behavior" pattern.
