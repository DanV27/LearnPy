---
title: Python Math
summary: The math module — sqrt, floor, ceil, pi, sin, and friends.
related: python-numbers, python-operators, python-modules
---

For anything beyond basic arithmetic, the `math` module has you covered. Import and call:

```python
import math

math.sqrt(16)        # 4.0
math.floor(3.7)      # 3
math.ceil(3.2)       # 4
math.pi              # 3.141592653589793
math.e               # 2.718281828459045
```

**Powers and logs**:

```python
math.pow(2, 10)      # 1024.0  — returns float
2 ** 10              # 1024    — returns int (built-in operator)
math.log(100, 10)    # 2.0     — log base 10
math.log(math.e)     # 1.0     — natural log (ln)
math.exp(1)          # 2.718...  — e^x
```

**Trig** (in radians):

```python
math.sin(math.pi / 2)        # 1.0
math.cos(0)                  # 1.0
math.degrees(math.pi)        # 180.0
math.radians(180)            # 3.141...
```

**Useful odds and ends**:

```python
math.gcd(12, 18)             # 6   — greatest common divisor
math.factorial(5)            # 120
math.isnan(float("nan"))     # True
math.inf                     # ∞   — float
```

- Numbers larger than a float can hold? Use `decimal` for exact decimal arithmetic.
- For statistics (mean, median, stdev), the `statistics` module is built-in.
- For vectorized math on arrays, jump to numpy.
