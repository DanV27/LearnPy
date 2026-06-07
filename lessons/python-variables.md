---
title: Python Variables
summary: Names that refer to values. No type declarations needed — assignment creates the variable.
related: python-data-types, python-casting, python-operators
---

A variable is a name bound to a value. Python doesn't require you to declare types up front; the assignment itself creates the variable.

```python
name = "Alice"
age = 30
is_admin = False
```

You can reassign variables freely, including to a value of a different type:

```python
result = 10
result = "ten"      # totally fine
```

**Naming rules**: start with a letter or underscore, then any mix of letters, digits, or underscores. Names are case-sensitive (`total` and `Total` are different). Convention is `snake_case` for variables and functions.

```python
user_count = 5       # idiomatic
UserCount = 5        # works but reads as a class name
2nd_player = "Bob"   # SyntaxError — can't start with a digit
```

- Use descriptive names. `n` is fine for a small loop counter; `num_retries` is better elsewhere.
- Constants are written in `UPPER_SNAKE_CASE` (`MAX_RETRIES = 3`) — a convention, not enforced.
- Variables defined inside a function are local to that function. See [Functions](/lesson/python-functions) for scope details.
