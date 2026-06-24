---
title: Trie
summary: A tree where each edge is a character — built for fast prefix lookups.
related: hash-map, graph, data-structures
---

A **trie** (pronounced "try") is a tree-shaped data structure where each path from the root spells out a string. It's the workhorse behind autocomplete, spell-check, and dictionary apps because prefix lookups are O(length-of-prefix) regardless of how many words you've stored.

```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def contains(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def _walk(self, s: str) -> TrieNode | None:
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node
```

```python
t = Trie()
for w in ["apple", "app", "apricot", "banana"]:
    t.insert(w)

t.contains("app")        # True
t.contains("ap")         # False  (a prefix, not a stored word)
t.starts_with("ap")      # True
t.starts_with("ban")     # True
```

**When to use a trie**:

- Autocomplete suggestions.
- Spell-check / nearest-word lookups.
- Routing tables that match URL prefixes.
- IP routing (a binary trie over bits).

**Trade-offs**: tries use more memory than a plain set of strings because each node holds a dict. For a fixed dictionary with no prefix queries, a [hash map](/lesson/hash-map) or set is simpler.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — Autocomplete, spell-check, longest-prefix matching (IP routing, dictionary lookups).</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Exact-match lookup or general key/value storage — a `dict` is simpler, faster, and uses less memory.</p>
</div>

