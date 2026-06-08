---
title: Doubly Linked List
summary: Each node points to the next AND the previous one. Insertion and deletion anywhere is O(1) given a node reference.
related: linked-list, deque, queue
---

A doubly linked list extends the singly linked one by adding a `prev` pointer to every node. The extra link lets you walk **either direction** and lets you delete a node in O(1) when you already have a reference to it — no need to walk from the head.

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class DoublyLinkedList:
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None

    def append(self, value) -> Node:
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        return node

    def remove(self, node: Node) -> None:
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
```

```python
ll = DoublyLinkedList()
a = ll.append(1)
b = ll.append(2)
c = ll.append(3)
ll.remove(b)             # constant time — no traversal
```

**When the extra pointer pays off**:

- **LRU caches** — remove a node from the middle when it becomes "recently used".
- **Browser history** — walk back and forward.
- The internals of [`collections.deque`](/lesson/deque) use a doubly linked structure.

**Cost vs. a singly linked list**: 2× the per-node memory, slightly more bookkeeping on every insert/delete. The win is the O(1) middle deletion.

If you find yourself building one of these in Python, double-check that a deque or `OrderedDict` wouldn't do the job with less code.
