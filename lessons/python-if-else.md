---
title: Python If...Else
summary: Conditional branching with if, elif, and else — choosing what code runs.
related: python-booleans, python-operators, python-match
---

`if` runs a block when a condition is true. `elif` chains additional checks. `else` runs when nothing else matched.

```python
score = 78

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("F")
```

Indentation matters in Python — it's how blocks are defined. Use 4 spaces (the universal convention).

**Conditional expressions** (ternary) — handy for assigning:

```python
status = "passed" if score >= 60 else "failed"
```

**Short-circuiting** in `and`/`or` means Python stops evaluating as soon as the answer is known:

```python
name = ""
if name and name[0] == "A":     # safe — name[0] never evaluated if name is empty
    ...
```

- You don't need parentheses around the condition: `if score >= 90:` not `if (score >= 90):`.
- For dispatching on a value's structure (especially Python 3.10+), [Python Match](/lesson/python-match) is cleaner than a long chain of `elif`s.
- Combine conditions with `and`, `or`, `not`. Use parens for clarity in mixed expressions.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Decision trees with two to four branches.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Ten-plus branches over a single value — that's a code smell. Use a dict dispatch or a `match` statement instead.</p>
</div>

