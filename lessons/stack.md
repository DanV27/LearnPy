---
title: Stack
summary: Last-in-first-out (LIFO) — the most recently added item is the first one out.
related: queue, deque, linked-list
---

A **stack** holds items in LIFO order. You push items onto the top and pop them off the top. Think of a stack of plates: the last plate you put down is the first one you'll grab.

Python lists already implement this:

```python
stack = []
stack.append("a")        # push
stack.append("b")
stack.append("c")
print(stack)             # ['a', 'b', 'c']

top = stack.pop()        # pop → 'c'
print(stack)             # ['a', 'b']
print(stack[-1])         # peek (look but don't remove) → 'b'
```

Both `append` and `pop` are O(1) amortized — fast and constant-time.

**Real-world uses**:

- Function call stacks (Python tracks calls this way internally).
- Undo/redo history in editors.
- Matching brackets and parsing expressions.
- Depth-first traversal of trees and [graphs](/lesson/graph).

```python
def is_balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack
```

- For thread-safe stacks, use `queue.LifoQueue`. Plain lists are not thread-safe.
- A [Deque](/lesson/deque) also works as a stack and is occasionally faster.
