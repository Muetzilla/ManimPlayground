# scripts/template.py
SCRIPT = {
    "subject": "Your Subject",
    "progress": "dots",  # or "bar" or None
    "theme": {
        # optional overrides (see DEFAULT_THEME keys in structure.py)
        # "font": "Inter",
        # "panel_height": 2.6,
    },
    "intro": {"title": "What we'll cover", "body": "• Point 1\n• Point 2\n• Point 3"},
    "steps": [
        {"title": "Step 1", "body": "Narration text here", "action": "show_scene"},
        {"title": "Step 2", "body": "More text", "action": "do_something", "args": {"speed": 1.5}},
        # ...
    ],
}
