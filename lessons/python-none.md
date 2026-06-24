---
title: Python None
summary: None is Python's "no value" — used for missing data, unset defaults, and "didn't return anything".
related: python-booleans, python-functions, python-data-types
---

`None` is Python's stand-in for "no value", "unset", or "missing". It's a singleton — there's only ever one `None`. Its type is `NoneType`.

```python
result = None
print(result)         # None
type(result)          # <class 'NoneType'>
```

**Checking for None** — use `is`, not `==`:

```python
if x is None: ...        # idiomatic
if x is not None: ...
```

Why `is`? `is` checks identity (the same object), and there's only one `None`. `==` works too, but `is` is faster, clearer, and avoids edge cases with overloaded `__eq__`.

**Common uses**:

```python
# A function that returns no useful value
def log(message):
    print(message)
    # returns None implicitly

# Default for missing arguments
def connect(host, port=None):
    port = port if port is not None else 8080
    ...

# Default for missing dict keys
prices.get("rice")        # returns None if "rice" isn't there
```

**Gotchas**:

- A function with no `return` returns `None`.
- `None` is falsy: `if x:` treats `None` and `0` and `""` the same. If that distinction matters, use `if x is None:` explicitly.
- Don't use `None` as a default argument value if you mean "a mutable type" — see [Python Functions](/lesson/python-functions) for the classic mutable-default bug.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — As a sentinel for 'no value yet' or 'not applicable' — and check with `is None`.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — As a default for *mutable* arguments. `def f(items=None): items = items or []` is the safe pattern; `items=[]` is the bug.</p>
</div>

