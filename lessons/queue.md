---
title: Queue
summary: First-in-first-out (FIFO) — items leave in the same order they arrived.
related: stack, deque, priority-queue
---

A **queue** is the opposite of a stack: items leave in the order they joined. Think of a line at a coffee shop. Use a queue any time fairness matters or you're processing tasks in arrival order.

**Don't use a plain list** — `list.pop(0)` is O(n) because every other element shifts. Use `collections.deque`:

```python
from collections import deque

q = deque()
q.append("a")            # enqueue
q.append("b")
q.append("c")
print(q)                 # deque(['a', 'b', 'c'])

first = q.popleft()      # dequeue → 'a'
print(q)                 # deque(['b', 'c'])
```

Both `append` and `popleft` are O(1).

**Real-world uses**:

- Breadth-first search of trees and [graphs](/lesson/graph).
- Background job queues.
- Print spoolers, network packet buffers.
- Anywhere "first come, first served" matters.

```python
# BFS sketch using a queue
def bfs(graph, start):
    visited = {start}
    q = deque([start])
    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return visited
```

- For thread-safe queues (e.g. producer/consumer between threads), use `queue.Queue` from the standard library — it has built-in locking.
- For priority-based ordering, see [Priority Queue](/lesson/priority-queue).
