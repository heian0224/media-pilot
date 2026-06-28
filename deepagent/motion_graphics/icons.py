"""Stroke icon library (viewBox 0 0 24 24, stroke=currentColor) for the motion-
graphics components. Add icons here as the video subagent needs new ones."""
from __future__ import annotations

P = {
    "reactor": '<path d="M8 21V11l1.5-6h5L16 11v10"/><path d="M6.5 21h11"/><path d="M11 11h2"/>',
    "datacenter": '<rect x="3" y="3" width="18" height="18" rx="1.5"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><circle cx="6.5" cy="6" r=".8" fill="currentColor"/><circle cx="6.5" cy="12" r=".8" fill="currentColor"/><circle cx="6.5" cy="18" r=".8" fill="currentColor"/>',
    "sign": '<path d="M4 5h12v7H4z"/><path d="M10 12v9"/><path d="M6.5 21h7"/>',
    "gavel": '<path d="M14.5 3.5l6 6-3 3-6-6z"/><path d="M11 7l6 6"/><path d="M9.5 12.5l-6 6 2.5 2.5 6-6"/><path d="M3.5 21h6"/>',
    "megaphone": '<path d="M4 9v6l13 6V3z"/><path d="M17 10a3.5 3.5 0 010 4"/><path d="M4 12H2.5"/>',
    "bolt": '<path d="M13 2L4 14h6l-1 8 10-13h-6z"/>',
    "droplet": '<path d="M12 3s6 6.5 6 11a6 6 0 01-12 0c0-4.5 6-11 6-11z"/>',
    "land": '<path d="M3 9l3-5h12l3 5"/><rect x="3" y="9" width="18" height="11"/><line x1="9" y1="9" x2="9" y2="20"/><line x1="15" y1="9" x2="15" y2="20"/>',
    "money": '<circle cx="12" cy="12" r="9"/><path d="M12 7v10"/><path d="M15 9.5c0-1.3-1.4-2-3-2s-3 .7-3 2 1.5 1.8 3 2.1 3 .8 3 2.1-1.4 2-3 2-3-.7-3-2"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14.7c2.9.1 5.2 2.3 5.2 5.3"/>',
    "pin": '<path d="M12 22s7-6.5 7-12a7 7 0 10-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "ban": '<circle cx="12" cy="12" r="9"/><line x1="5.6" y1="5.6" x2="18.4" y2="18.4"/>',
    "robot": '<rect x="5" y="8" width="14" height="11" rx="2.5"/><path d="M12 4v4"/><circle cx="12" cy="3.2" r="1.1" fill="currentColor"/><circle cx="9.3" cy="12.5" r="1.2"/><circle cx="14.7" cy="12.5" r="1.2"/><path d="M9.5 16h5"/>',
    "newspaper": '<rect x="3" y="5" width="18" height="14" rx="1"/><line x1="6" y1="9" x2="18" y2="9"/><line x1="6" y1="12.5" x2="18" y2="12.5"/><line x1="6" y1="16" x2="13" y2="16"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="1.5"/><path d="M8 11V7.5a4 4 0 018 0V11"/><circle cx="12" cy="15.5" r="1.3"/>',
    "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>',
    "heart": '<path d="M12 21s-7-4.3-9-9.2C1.4 7.7 3.6 4.5 6.8 4.5c1.9 0 3.4 1.1 4.2 2.3.8-1.2 2.3-2.3 4.2-2.3 3.2 0 5.4 3.2 3.8 7.3-2 4.9-9 9.2-9 9.2z"/>',
    "prism": '<polygon points="12,3 21,20 3,20"/><line x1="12" y1="3" x2="12" y2="20"/><line x1="7.5" y1="11.5" x2="16.5" y2="11.5"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
    "down": '<path d="M12 4v15M6 13l6 6 6-6"/>',
    "up": '<path d="M12 20V5M6 11l6-6 6 6"/>',
    "alert": '<path d="M12 3l9 16H3z"/><line x1="12" y1="10" x2="12" y2="14"/><circle cx="12" cy="17" r=".9" fill="currentColor"/>',
    "code": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 6l-3 12"/>',
    "chart": '<path d="M4 20V4M4 20h16M8 16v-4M13 16V8M18 16v-7"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>',
}


def icon(name: str, size: int) -> str:
    svg = P.get(name) or P["sparkle"]  # fallback to sparkle if unknown
    return (
        f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{svg}</svg>'
    )
