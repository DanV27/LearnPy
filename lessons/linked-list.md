---
title: Linked List
summary: Nodes pointing to nodes — flexible at the ends, O(n) in the middle.
related: doubly-linked-list, stack, queue
---

A **singly linked list** is a chain of nodes. Each node holds a value and a pointer to the next node. The last node points to `None`.

You almost never need to write one in Python — built-in lists and [deques](/lesson/deque) are usually faster — but linked lists are a classic interview topic and a good way to internalize pointer mechanics.

```python
class Node:
    def __init__(self, value, next_=None):
        self.value = value
        self.next = next_


class LinkedList:
    def __init__(self):
        self.head: Node | None = None

    def push_front(self, value) -> None:
        self.head = Node(value, self.head)

    def to_list(self) -> list:
        out, n = [], self.head
        while n is not None:
            out.append(n.value)
            n = n.next
        return out

    def find(self, value) -> bool:
        n = self.head
        while n is not None:
            if n.value == value:
                return True
            n = n.next
        return False
```

```python
ll = LinkedList()
ll.push_front(3)
ll.push_front(2)
ll.push_front(1)
print(ll.to_list())      # [1, 2, 3]
print(ll.find(2))        # True
```

**Trade-offs vs. a Python list**:

- Insertion at the front is O(1) (vs. O(n) for a list).
- Indexing is O(n) (vs. O(1) for a list).
- Memory overhead is much higher per element.

For real code in Python, a [deque](/lesson/deque) gives you O(1) at both ends without the boilerplate. Reach for a hand-written linked list when you need pointer fiddling — circular lists, custom traversal — or to learn the algorithm.

Next: see [Doubly Linked List](/lesson/doubly-linked-list) for the version with `prev` pointers, which makes deletion in the middle O(1) when you already hold the node.
