"""
Diagram sequences for step-through animated diagram players in lessons.

To add diagrams for a new lesson:
  1. Drop image files into static/diagrams/<lesson-slug>/
  2. Append a new entry to DIAGRAM_SEQUENCES keyed by the lesson slug.
  3. The template and DiagramPlayer JS pick it up automatically — no
     backend changes needed.

Image paths are relative to the Flask static root (static/), so they
work with url_for('static', filename=step['src']).
"""

DIAGRAM_SEQUENCES = {
    "hash-map": [
        {
            "src": "diagrams/hashmap/step-1.png",
            "caption": "Empty hash table with 6 buckets, indexed 0–5.",
        },
        {
            "src": "diagrams/hashmap/step-2.png",
            "caption": "Insert ‘cat’: hash(‘cat’) % 6 = 2, goes into bucket 2.",
        },
        {
            "src": "diagrams/hashmap/step-3.png",
            "caption": "Insert ‘dog’: hash(‘dog’) % 6 = 2 as well. Collision.",
        },
        {
            "src": "diagrams/hashmap/step-4.png",
            "caption": "Both key-value pairs chained together in bucket 2.",
        },
        {
            "src": "diagrams/hashmap/step-5.png",
            "caption": "Looking up ‘dog’: jump to bucket 2, walk the chain past ‘cat’ to find it.",
        },
    ],
}


def get_diagram_sequence(slug: str):
    """Return the diagram step list for *slug*, or None if none is defined."""
    return DIAGRAM_SEQUENCES.get(slug)
