"""Sidebar navigation registry.

The sidebar is data-driven: edit ``NAV_ITEMS`` (or import and extend it
from your application) to add/remove links. Each item is a small dict so
templates stay decoupled from any specific framework helper.

Schema:
    {
        "label": str,             # text shown in sidebar
        "url": str,               # absolute path
        "icon": str,              # SVG snippet name (see partials/icons.html)
        "section": str | None,    # optional group label
        "match": list[str],       # url prefixes that mark item active
    }
"""

from __future__ import annotations

from typing import Iterable


NAV_ITEMS: list[dict] = [
    {
        "label": "Dashboard",
        "url": "/",
        "icon": "home",
        "section": "Main",
        "match": ["/"],
    },
    {
        "label": "Profile",
        "url": "/profile",
        "icon": "user",
        "section": "Main",
        "match": ["/profile"],
    },
    {
        "label": "Settings",
        "url": "/settings",
        "icon": "cog",
        "section": "Main",
        "match": ["/settings"],
    },
]


def is_active(item: dict, current_path: str) -> bool:
    matches: Iterable[str] = item.get("match") or [item["url"]]
    # Exact match for root, prefix match otherwise.
    for m in matches:
        if m == "/":
            if current_path == "/":
                return True
        elif current_path == m or current_path.startswith(m.rstrip("/") + "/"):
            return True
    return False


def grouped_items() -> list[tuple[str, list[dict]]]:
    """Return items grouped by section, preserving insertion order."""
    groups: dict[str, list[dict]] = {}
    for item in NAV_ITEMS:
        section = item.get("section") or ""
        groups.setdefault(section, []).append(item)
    return list(groups.items())
