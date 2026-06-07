---
title: Python Strings
summary: Text in Python — immutable, indexable, and full of built-in methods.
related: python-string-formatting, python-casting, regex
---

Strings hold text. They're created with single, double, or triple quotes:

```python
a = 'hello'
b = "hello"
c = '''multi
line'''
```

Strings are **immutable** — every operation returns a new string. They're also **indexable**:

```python
s = "Python"
s[0]         # 'P'
s[-1]        # 'n'
s[0:3]       # 'Pyt'   — slicing
s[::-1]      # 'nohtyP' — reversed
len(s)       # 6
```

**Common methods**:

```python
"  hi  ".strip()           # 'hi'
"hello".upper()            # 'HELLO'
"Hello, World".lower()     # 'hello, world'
"a,b,c".split(",")         # ['a', 'b', 'c']
",".join(["a", "b", "c"])  # 'a,b,c'
"hello".replace("l", "L")  # 'heLLo'
"name".startswith("na")    # True
```

- Use **f-strings** for interpolation: `f"Hello, {name}!"`. See [String Formatting](/lesson/python-string-formatting).
- `+` concatenates strings: `"foo" + "bar"`. For many concatenations in a loop, use `"".join(parts)` — it's much faster.
- For pattern matching beyond simple `in`, use [Regular Expressions](/lesson/regex).
