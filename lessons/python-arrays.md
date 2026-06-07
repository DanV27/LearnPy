---
title: Python Arrays
summary: Lists handle most cases. For typed, homogeneous storage there's the array module — and numpy for serious work.
related: python-lists, python-iterators, data-structures
---

Python doesn't have a built-in "array" type the way C does. The thing most people call an array is just a [list](/lesson/python-lists):

```python
nums = [1, 2, 3, 4]
nums.append(5)
nums[0] = 99
```

Lists work great for almost everything. But when you have **lots of numbers of the same type** and care about memory or speed, two specialized options exist.

**The `array` module** — a thin wrapper around C arrays of one numeric type:

```python
from array import array
ages = array("i", [25, 30, 45, 60])    # 'i' = signed int
ages.append(75)
ages[0]                                  # 25
```

The first argument is a typecode: `"i"` for int, `"f"` for float, `"d"` for double, `"b"` for byte. Memory use is much smaller than a list of ints.

**numpy** — the serious option, used everywhere in data science and ML:

```python
import numpy as np
arr = np.array([1, 2, 3, 4])
arr * 2          # array([2, 4, 6, 8])  — elementwise
arr.mean()       # 2.5
arr.shape        # (4,)
```

**When to reach for each**:

- **list**: 95% of code. Mixed types, small to medium sizes, mutable.
- **array module**: tens of thousands of homogeneous numbers, no extra deps.
- **numpy**: scientific computing, large datasets, vectorized math.
