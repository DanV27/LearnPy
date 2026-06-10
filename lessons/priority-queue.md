---
title: Priority Queue
summary: Items come out in priority order, not arrival order. Backed by a heap.
related: queue, graph, algorithms
---

A **priority queue** lets you push items in any order and always pop the highest-priority one. The standard way to implement one is a **binary heap** — and Python's `heapq` module does exactly that, treating a plain list as a min-heap.

```python
import heapq

heap: list[int] = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)

heapq.heappop(heap)      # 1  — always the smallest
heapq.heappop(heap)      # 1
heapq.heappop(heap)      # 3
heapq.heappop(heap)      # 4
```

Both `heappush` and `heappop` are O(log n).

**Tuples for priority + payload** — heapq compares whole tuples, so put the priority first:

```python
tasks = []
heapq.heappush(tasks, (2, "write report"))
heapq.heappush(tasks, (1, "fix prod bug"))
heapq.heappush(tasks, (3, "tidy desk"))

while tasks:
    priority, name = heapq.heappop(tasks)
    print(priority, name)
# 1 fix prod bug
# 2 write report
# 3 tidy desk
```

**Max-heap?** `heapq` is a min-heap. For a max-heap, negate the priority when pushing and again when reading:

```python
heapq.heappush(maxheap, (-priority, item))
```

**Real-world uses**:

- Dijkstra's shortest path algorithm on a [graph](/lesson/graph).
- A* and other search algorithms.
- Scheduling: always run the most urgent job next.
- The k smallest / k largest items in a stream: `heapq.nsmallest(k, iterable)`.

For thread-safe priority queues, use `queue.PriorityQueue`.
