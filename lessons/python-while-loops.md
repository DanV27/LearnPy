---
title: Python While Loops
summary: Run a block of code as long as a condition stays true.
related: python-for-loops, python-if-else, python-booleans
---

`while` repeats a block until its condition becomes false. Use it when you don't know up front how many iterations you'll need.

```python
count = 0
while count < 5:
    print(count)
    count += 1
# 0, 1, 2, 3, 4
```

**`break` and `continue`**:

```python
while True:
    answer = input("Quit? (y/n) ")
    if answer == "y":
        break          # exit the loop entirely
    if answer == "":
        continue       # skip to the next iteration
    print("you said:", answer)
```

**The `else` clause**: a `while` (and `for`) loop can have an `else` that runs if the loop ended *without* hitting `break`:

```python
while attempts > 0:
    if try_login():
        break
    attempts -= 1
else:
    print("locked out")
```

- Avoid `while True:` without a clear `break` — it's how infinite loops sneak in.
- When you're iterating over a known collection, prefer a [for loop](/lesson/python-for-loops) — it's harder to mess up.
- Watch out for off-by-one bugs: `while i < n` vs. `while i <= n` are commonly confused.
