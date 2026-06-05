---
title: Context Managers
summary: Use the with statement to guarantee setup-and-teardown — open files, acquire locks, manage resources safely.
related: file-io, decorators, generators
---

A **context manager** is an object you use with the `with` statement. It guarantees two things happen: setup runs when you enter the block, and cleanup runs when you leave — even if something raises an exception.

You've probably already used the most famous one:

```python
with open("notes.txt") as f:
    data = f.read()
# file is automatically closed here, even if read() raised
```

That `with open(...)` block calls `f.close()` for you no matter how the block ends.

## Building your own — the class form

A context manager needs two methods: `__enter__` (runs on entry) and `__exit__` (runs on exit):

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self                          # bound to "as" target

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"Block took {self.elapsed:.4f}s")
        return False                         # don't swallow exceptions

with Timer() as t:
    sum(range(1_000_000))
```

`__exit__` is called with information about any exception that occurred inside the block. Return `True` to suppress it; return `False` (or `None`) to let it propagate.

## The shortcut — `@contextmanager`

For one-off context managers, the `contextlib` module lets you write them as generators:

```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.perf_counter()
    yield                               # control passes to the with-block
    print(f"Took {time.perf_counter() - start:.4f}s")

with timer():
    sum(range(1_000_000))
```

Everything before `yield` is `__enter__`. Everything after `yield` is `__exit__`. Put cleanup inside a `try/finally` if you need it to run even on exceptions.

## When you'll use them

- Anything that opens-then-closes: [files](/lesson/file-io), database connections, sockets, GUI windows.
- Anything that acquires-then-releases: locks, semaphores, transactions.
- Anything you want timed, traced, or audited around a block.

If `with` blocks feel familiar after this, see how [Decorators](/lesson/decorators) and [Generators](/lesson/generators) compose blocks of behavior in similar ways.
