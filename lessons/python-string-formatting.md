---
title: Python String Formatting
summary: Interpolate values into strings — f-strings are the modern, preferred way.
related: python-strings, python-numbers, python-dates
---

Python has three string-formatting styles. Use **f-strings** for new code.

**f-strings** (Python 3.6+) — the preferred way:

```python
name = "Alice"
age = 30
print(f"{name} is {age} years old.")
```

You can embed any Python expression:

```python
print(f"{name.upper()} turns {age + 1} next year.")
print(f"Total: ${price * 1.07:.2f}")
```

**Format specifiers** go after a colon:

```python
f"{3.14159:.2f}"          # '3.14'   — 2 decimal places
f"{1000000:,}"            # '1,000,000' — thousands separator
f"{42:05d}"               # '00042'  — pad with zeros to width 5
f"{0.85:.0%}"             # '85%'    — percentage
f"{'hi':>10}"             # '        hi' — right-align in 10 cols
f"{'hi':^10}"             # '    hi    ' — center
```

**.format() method** — older, still common:

```python
"{} is {}".format(name, age)
"{name} is {age}".format(name=name, age=age)
```

**Printf-style %** — the oldest, mostly legacy now:

```python
"%s is %d" % (name, age)
```

- f-strings can include the variable name *and* value with `=` (3.8+): `f"{x=}"` → `"x=42"`. Great for debugging.
- Multi-line f-strings work fine with triple quotes.
- For complex template generation (emails, HTML), reach for a real template engine like Jinja2.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — f-strings for every new piece of code — they're fastest, clearest, and most flexible.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — `.format()` or `%`-formatting in new code (legacy). Exception: logging libraries that defer formatting expect `%`-style.</p>
</div>

