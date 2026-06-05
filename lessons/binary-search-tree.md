---
title: Binary Search Tree
summary: A tree where each left child is smaller and each right child is larger — fast lookups when balanced.
related: binary-search, hash-map, sorting
---

A **binary search tree** (BST) is a tree where every node has up to two children, and the structure obeys one rule: for any node, everything in its left subtree is smaller than it, and everything in its right subtree is larger. That rule is what makes search fast — at each step you can throw away half the remaining tree.

## Implementation

```python
class Node:
    def __init__(self, value: int):
        self.value = value
        self.left: "Node | None" = None
        self.right: "Node | None" = None


class BST:
    def __init__(self):
        self.root: Node | None = None

    def insert(self, value: int) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node: Node | None, value: int) -> Node:
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node  # duplicates ignored

    def contains(self, value: int) -> bool:
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def in_order(self) -> list[int]:
        """Return all values in ascending order."""
        out: list[int] = []
        def walk(n: Node | None) -> None:
            if n is None: return
            walk(n.left)
            out.append(n.value)
            walk(n.right)
        walk(self.root)
        return out
```

## Why it matters

- `insert` and `contains` are O(log n) **on a balanced tree**, O(n) in the worst case (a tree that degenerates into a linked list).
- An in-order traversal of a BST visits values in sorted order — handy for free.
- Real-world BSTs are usually self-balancing (AVL, red-black). Python's `dict` and `set` use [Hash Maps](/lesson/hash-map) instead; BSTs shine when you need ordered iteration.

## Try it

```python
tree = BST()
for n in [5, 2, 8, 1, 3]:
    tree.insert(n)
print(tree.contains(3))     # True
print(tree.in_order())      # [1, 2, 3, 5, 8]
```

Next up: try [Binary Search](/lesson/binary-search), which uses the same "halve the search range" idea on a flat sorted list.
