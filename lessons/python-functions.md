---
title: Python Functions
summary: Reusable blocks of code defined with `def`. Parameters, return values, defaults, and *args/**kwargs.
related: python-variables, python-modules, decorators
---

A function packages a chunk of work so you can call it by name. Use `def`:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("World"))   # Hello, World!
```

Type hints (`name: str`, `-> str`) are optional but recommended — they help editors, linters, and the next reader.

**Default arguments** let you skip parameters when calling:

```python
def greet(name: str, excited: bool = False) -> str:
    return f"Hello, {name}{'!' if excited else '.'}"

greet("Alice")                    # "Hello, Alice."
greet("Alice", excited=True)      # "Hello, Alice!"
```

**Variable arguments**:

```python
def total(*nums):                 # any number of positional args
    return sum(nums)

def make_user(**fields):          # any number of keyword args
    return fields

total(1, 2, 3)                    # 6
make_user(name="Alice", age=30)   # {"name": "Alice", "age": 30}
```

**Scope**: variables created inside a function are local. To modify a module-level variable from inside a function, use `global` (rare) or restructure.

- Functions without an explicit `return` return `None`.
- If a default argument is a mutable type (`list`, `dict`), don't use the literal `[]` — Python evaluates it once. Use `None` and create inside the function instead.
- For one-liners, `lambda` exists: `square = lambda x: x*x`. But prefer `def` for readability.
