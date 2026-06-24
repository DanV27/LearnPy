---
title: Python Data Types
summary: Python's built-in types at a glance — what they are and how to spot them.
related: python-casting, python-numbers, data-structures
---

Every value in Python has a type. You can check it with `type()`:

```python
type("hello")      # <class 'str'>
type(42)           # <class 'int'>
type(3.14)         # <class 'float'>
type(True)         # <class 'bool'>
type(None)         # <class 'NoneType'>
type([1, 2])       # <class 'list'>
type((1, 2))       # <class 'tuple'>
type({1, 2})       # <class 'set'>
type({"a": 1})     # <class 'dict'>
```

**Categories**:

- **Numeric**: `int`, `float`, `complex`.
- **Text**: `str`.
- **Boolean**: `bool` (a subclass of `int` — `True == 1` and `False == 0`).
- **Sequence**: `list`, `tuple`, `range`.
- **Mapping**: `dict`.
- **Set**: `set`, `frozenset`.
- **None**: `NoneType`, with a single value `None`.

Mutable types (`list`, `dict`, `set`) can be modified in place. Immutable types (`str`, `tuple`, `int`, `float`, `bool`) cannot — every "modification" returns a new value.

```python
x = "hello"
x.upper()          # returns "HELLO" — x is unchanged
```

- `isinstance(value, type)` is the right way to check types in conditional code.
- Numbers and strings are immutable: this is what makes them safe to use as dict keys.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — `isinstance(value, type)` whenever your function's behavior depends on the type.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — `type(value) == SomeType` — it fails on subclasses and is usually a sign of over-specific code.</p>
</div>

