---
title: Python Modules
summary: Reuse code by splitting it into files. Each .py file is a module; folders of modules become packages.
related: python-pip, python-functions, python-virtualenv
---

A **module** is just a `.py` file. Importing it gives you access to its functions, classes, and variables.

```python
# greetings.py
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

```python
# main.py
import greetings
print(greetings.hello("World"))
```

**Import flavors**:

```python
import math
import math as m
from math import sqrt
from math import sqrt, pi
from math import *           # avoid — pollutes your namespace
```

**Packages** are folders containing modules and an `__init__.py` file:

```
mypkg/
    __init__.py
    api.py
    utils.py
```

```python
from mypkg import api
from mypkg.utils import clean
```

**The `__name__ == "__main__"` idiom** — runs only when the file is executed directly, not when it's imported:

```python
def main():
    print("running")

if __name__ == "__main__":
    main()
```

- Python's standard library is huge: `os`, `sys`, `pathlib`, `json`, `re`, `datetime`, `collections`, `itertools`, `functools` — explore it before reaching for third-party packages.
- For external packages, use [pip](/lesson/python-pip) to install and a [virtual env](/lesson/python-virtualenv) to keep projects isolated.
