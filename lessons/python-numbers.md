---
title: Python Numbers
summary: int, float, complex — Python's three numeric types and how they interact.
related: python-math, python-casting, python-operators
---

Python ships with three numeric types:

```python
a = 7              # int — arbitrary precision
b = 3.14           # float — 64-bit floating point
c = 2 + 3j         # complex — real + imaginary
```

Integers in Python have unlimited size (subject to memory). Floats follow IEEE 754 double-precision, so they suffer the usual rounding quirks:

```python
0.1 + 0.2          # 0.30000000000000004
```

For exact decimal math (money), use the `decimal` module.

**Common operations**:

```python
7 / 2              # 3.5    — true division (always float)
7 // 2             # 3      — floor division
7 % 2              # 1      — remainder
2 ** 10            # 1024   — exponent
abs(-5)            # 5
round(3.7)         # 4
```

- Mixing `int` and `float` produces a `float`.
- The `math` module ([Python Math](/lesson/python-math)) has `sqrt`, `floor`, `ceil`, `pi`, and friends.
- Bit operators (`&`, `|`, `^`, `<<`, `>>`) work on ints for low-level tasks.
