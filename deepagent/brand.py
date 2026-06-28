"""Brand loading — the single parsed source of truth.

The repo is brand-neutral: identity is read from an external ``brand.md``
(default ``$WORKSPACE_ROOT/brand.md``; see ``brand.example.md``). Nothing is
baked in. Parsing is intentionally tolerant — missing fields fall back to
empty/default so the agent degrades gracefully instead of crashing.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import config

_DEFAULT_PALETTE = {
    "bg_start": "#0B1026",
    "bg_end": "#1E1B4B",
    "cyan": "#22D3EE",
    "magenta": "#F472B6",
    "purple": "#7C3AED",
}


@dataclass
class Brand:
    name: str = ""          # e.g. the brand's Chinese display name
    name_en: str = ""       # e.g. the brand's romanized name
    site: str = ""          # e.g. the brand's domain
    slogan: str = ""        # e.g. the brand's slogan line
    handle: str = ""        # e.g. @handle
    bio: str = ""
    palette: dict = field(default_factory=lambda: dict(_DEFAULT_PALETTE))
    sign_off: str = ""      # e.g. the brand's CTA sign-off
    raw: str = ""

    @property
    def present(self) -> bool:
        return bool(self.name)


def _hex_roles(text: str, pal: dict) -> None:
    """Classify hex colors by RGB role (bg = darkest two, cyan/magenta by hue)."""
    hexes = re.findall(r"#[0-9A-Fa-f]{6}", text)
    if not hexes:
        return
    # darkest first → background gradient
    def lum(h: str) -> int:
        r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
        return r + g + b
    dark = sorted(hexes, key=lum)[:2]
    if len(dark) == 2:
        pal["bg_start"], pal["bg_end"] = dark[0], dark[1]
    for h in hexes:
        r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
        if g > 150 and b > 150 and r < 130:
            pal["cyan"] = h
        elif r > 200 and b > 130 and g < 150:
            pal["magenta"] = h
        elif r > 100 and b > 180 and g < 120:
            pal["purple"] = h


def load_brand(path: str | Path | None = None) -> Brand:
    p = Path(path) if path else config.BRAND_MD_PATH
    if not p.is_file():
        return Brand()
    text = p.read_text(encoding="utf-8")
    b = Brand(raw=text)

    m = re.search(r"中文名[*\s:：]*\**\s*\**([^*\n：]+)\**", text)
    if m:
        b.name = m.group(1).strip()
    m = re.search(r"英文名[^：\n]*[:：][^*\n]*\**\s*\**([^*\n：]+)\**", text)
    if m:
        b.name_en = m.group(1).strip()

    m = re.search(r"网站[^：\n]*[:：][^\n]*?\((?:https?://)?([^/)\s]+)", text)
    if m:
        b.site = m.group(1).strip()

    parts = re.split(r"##\s*Slogan", text, maxsplit=1)
    if len(parts) > 1:
        m = re.search(r">\s*\**\s*\**([^*\n>+]+)\**", parts[1])
        if m:
            b.slogan = m.group(1).strip()

    m = re.search(r"@[A-Za-z][\w.]*", text)
    if m:
        b.handle = m.group(0)

    _hex_roles(text, b.palette)

    if b.name:
        b.sign_off = f"关注「{b.name}」"
    return b


if __name__ == "__main__":  # quick manual check
    b = load_brand()
    print(b)
