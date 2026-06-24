---
title: Python Try...Except
summary: Catch exceptions cleanly with try/except. Add else and finally for completeness.
related: python-if-else, python-functions, basics
---

When code might fail, wrap it in `try`. If something inside raises an exception, the matching `except` block handles it.

```python
try:
    age = int(input("Age? "))
except ValueError:
    print("That wasn't a number.")
```

**Multiple exception types**:

```python
try:
    risky()
except (ValueError, KeyError) as e:
    print(f"Bad input: {e}")
except ConnectionError:
    print("Network down.")
except Exception as e:        # catch-all (use sparingly)
    print(f"Unexpected: {e}")
```

**`else` and `finally`**:

```python
try:
    f = open("data.txt")
except FileNotFoundError:
    print("missing")
else:
    print("opened OK")        # runs only if no exception
    f.close()
finally:
    print("cleanup")          # always runs
```

**Raising exceptions**:

```python
def withdraw(amount):
    if amount < 0:
        raise ValueError("amount must be non-negative")
```

- Catch the most specific exception class you can. `except Exception` swallows bugs.
- The `as e` binds the exception to a name so you can read `e.args`, the message, etc.
- For automatic cleanup (files, locks, db connections), `with` blocks (context managers) are cleaner than `try/finally`.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — When an operation might legitimately fail AND you have a meaningful recovery plan.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Blanket `except:` or `except Exception:` — you'll swallow real bugs. Catch the most specific exception you can.</p>
</div>

