---
title: Python Basics
summary: Variables, types, control flow, and functions — the foundation everything else builds on.
related: data-structures, file-io, json
---

Python is a high-level, dynamically typed language designed to be easy to read. Before you can build anything interesting, you need to be comfortable with variables, types, conditionals, loops, and functions. This page walks through all five in one place.

## Variables and Types

You don't declare types in Python — you just assign:

```python
name = "Alice"        # str
age = 30              # int
height = 5.7          # float
is_member = True      # bool
items = ["a", "b"]    # list
```

You can inspect a value's type with `type(x)`, and convert between types with `int("42")`, `str(3.14)`, `float("1.5")`, etc.

## Control Flow

`if` / `elif` / `else` work the way you'd expect:

```python
def grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"
```

Loops come in two flavors. `for` iterates over anything sequence-like; `while` runs until a condition becomes false:

```python
for n in range(5):
    print(n)          # 0 1 2 3 4

count = 0
while count < 3:
    count += 1
```

## Functions

Functions use `def`. Type hints are optional but recommended — they document intent and play nicely with editors:

```python
def greet(name: str, excited: bool = False) -> str:
    suffix = "!" if excited else "."
    return f"Hello, {name}{suffix}"

print(greet("World", excited=True))
```

Default arguments (`excited=False`) and keyword arguments are first-class — you don't need to overload functions like you might in other languages.

## What to learn next

Once these click, move on to [Data Structures](/lesson/data-structures) to see how `list`, `dict`, `set`, and `tuple` differ, or try [File I/O](/lesson/file-io) to read and write files.
