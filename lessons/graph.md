---
title: Graph
summary: Nodes connected by edges — the data structure behind maps, networks, and dependencies.
related: stack, queue, priority-queue
---

A **graph** is a collection of nodes (vertices) connected by edges. Use one any time you have things and relationships between them: friends, web pages and links, cities and roads, build dependencies.

The most common Python representation is an **adjacency list** — a dict mapping each node to its neighbors:

```python
graph: dict[str, list[str]] = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C"],
}
```

Edges going both ways = **undirected** graph. List neighbors only in one direction for a **directed** graph.

**Breadth-first search** — shortest path in an unweighted graph:

```python
from collections import deque

def bfs(g, start):
    visited = {start}
    q = deque([start])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for neighbor in g[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return order

print(bfs(graph, "A"))   # ['A', 'B', 'C', 'D']
```

**Depth-first search** — same shape, but use a [stack](/lesson/stack) (or recursion):

```python
def dfs(g, start, visited=None):
    visited = visited or set()
    visited.add(start)
    for neighbor in g[start]:
        if neighbor not in visited:
            dfs(g, neighbor, visited)
    return visited
```

**Common applications**:

- Shortest path: BFS for unweighted, Dijkstra (a [priority queue](/lesson/priority-queue)) for weighted.
- Detecting cycles in dependency graphs.
- Topological sort for build orders, task scheduling.
- Connected components, A* pathfinding.

For serious graph algorithms in Python, the **networkx** library has everything from PageRank to graph isomorphism.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Modeling relationships — social networks, dependencies, road maps, friend-of-friend queries.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — When a tree or flat list would suffice. Graphs bring real complexity (cycles, traversal choice, weighted edges).</p>
</div>

