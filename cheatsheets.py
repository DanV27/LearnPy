from pathlib import Path
import json

CHEATSHEETS_DIR = Path(__file__).parent / "cheatsheets"

def load_cheatsheet(slug: str):
    """Return the cheatsheet dict for slug, or None if missing."""
    path = CHEATSHEETS_DIR / f"{slug}.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def list_cheatsheets():
    """Return [{slug, title, icon}] for every cheatsheet on disk.
    Used by the sidebar."""
    out = []
    for p in sorted(CHEATSHEETS_DIR.glob("*.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        out.append({
            "slug": p.stem,
            "title": data.get("title", p.stem),
            "icon": data.get("icon", "description"),
        })
    return out

def lesson_to_cheatsheet():
    """Reverse lookup: {lesson_slug: cheatsheet_slug}.
    Built fresh on each call — at ~10 sheets total this is fine.
    Used to render the 'Cheat sheet for this topic' link on lesson pages."""
    out = {}
    for p in CHEATSHEETS_DIR.glob("*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        related = data.get("related_lesson")
        if related:
            out[related] = p.stem
    return out