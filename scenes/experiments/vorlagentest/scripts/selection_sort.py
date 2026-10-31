# scripts/selection_sort.py
SCRIPT = {
    "subject": "Selection Sort",
    "progress": "bar",
    "theme": {
        "font": "Inter",
        "default_hold": 0.8,
    },
    "intro": {
        "title": "What we'll do",
        "body": "• Find the smallest element\n• Swap it to the front\n• Repeat for the rest",
    },
    "steps": [
        {
            "title": "Initial array",
            "body": "• We start with an unsorted list\n• We'll scan for the minimum",
            "action": "show_array",
        },
        {
            "title": "Scan for minimum",
            "body": "• Compare each element\n• Keep the smallest seen so far",
            "action": "scan",
            "args": {"start": 0},
        },
        {
            "title": "Swap into place",
            "body": "• Put the found minimum at the front\n• First position is now sorted",
            "action": "swap",
            "args": {"i": 0, "j": 1},
        },
        {
            "title": "Repeat",
            "body": "• Move to the next position\n• Apply the same logic",
            "action": "repeat_hint",
        },
    ],
}
