---
title: Python Operators
summary: Arithmetic, comparison, logical, assignment, identity, and membership — the symbols that do work.
related: python-numbers, python-booleans, python-if-else
---

Operators are symbols that perform an action on values. Python groups them into a few categories:

**Arithmetic**: `+`, `-`, `*`, `/`, `//` (floor), `%` (remainder), `**` (power).
**Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=`. Returns a boolean.
**Logical**: `and`, `or`, `not`. Short-circuiting.
**Assignment**: `=`, `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`.
**Identity**: `is`, `is not`. Tests *the same object*, not equality.
**Membership**: `in`, `not in`. Works on strings, lists, dicts, sets, ranges.

```python
3 + 4            # 7
10 // 3          # 3
10 % 3           # 1
2 ** 8           # 256

a = 5
a += 1           # a is now 6

"y" in "yes"     # True
3 in [1, 2, 3]   # True

a is None        # idiomatic — don't use `==` for None
```

**Operator precedence** (highest to lowest, rough):

1. `**`
2. unary `+`, `-`, `~`
3. `*`, `/`, `//`, `%`
4. `+`, `-`
5. comparisons
6. `not`
7. `and`
8. `or`

When unsure, add parentheses — readability beats cleverness.
