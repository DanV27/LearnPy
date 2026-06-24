---
title: Python Comments
summary: Comments are notes for human readers — Python ignores them when running your code.
related: python-variables, python-strings, basics
---

Comments document what your code is doing for the next person who reads it (often future you). Python has one comment syntax: anything from `#` to the end of the line is ignored.

```python
# This is a single-line comment.
x = 42        # Comments can also follow code.

# Python has no dedicated multi-line comment syntax.
# Just stack single-line ones.
```

For docstrings — which document functions, classes, and modules — use a triple-quoted string as the first statement:

```python
def add(a: int, b: int) -> int:
    """Return the sum of a and b."""
    return a + b
```

- Write comments to explain **why**, not **what**. Clean code makes the *what* obvious; the *why* is what's worth recording.
- Don't comment out dead code — delete it. Version control remembers it for you.
- Docstrings are accessible at runtime via `help(add)` or `add.__doc__`.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — To explain WHY non-obvious code does what it does, and for module/function docstrings.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — To narrate WHAT the code does — clean code makes that obvious. Don't comment every line.</p>
</div>

