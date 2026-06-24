---
title: Python User Input
summary: Read text from the terminal with input(). Always validate before trusting it.
related: python-casting, python-try-except, python-strings
---

The built-in `input()` function pauses your program and waits for the user to type a line of text. It returns whatever they typed, as a **string** — always a string.

```python
name = input("What's your name? ")
print(f"Hi, {name}!")
```

**Converting to other types** — you need a cast:

```python
age_str = input("Age? ")
age = int(age_str)        # raises ValueError on bad input
```

**Validating safely**:

```python
while True:
    raw = input("Pick a number 1-10: ")
    try:
        n = int(raw)
    except ValueError:
        print("Not a number, try again.")
        continue
    if 1 <= n <= 10:
        break
    print("Out of range, try again.")
print(f"You picked {n}")
```

**Reading several values**:

```python
parts = input("Enter x and y: ").split()
x, y = int(parts[0]), int(parts[1])
```

- `input()` always strips the trailing newline.
- For non-interactive scripts (cron jobs, pipelines), don't use `input()` — read from `sys.argv` or environment variables instead.
- For passwords, use `getpass.getpass()` from the standard library — it hides the input.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — `input()` for quick CLI scripts, prototypes, and class exercises.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — In production services or anything non-interactive — read from CLI args, files, or environment variables. `input()` hangs cron jobs forever.</p>
</div>

