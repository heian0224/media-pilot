"""Render wechat.md → paste-ready inline-styled wechat.html.

M3a shells out to the workspace's scripts/wechat_render.py (which bakes the brand
theme inline). M5 will move that renderer into the package and read brand from
brand.py instead of the current hardcoded palette."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from langchain_core.tools import tool

from .. import config

# Bundled, brand-driven renderer (self-contained — no workspace scripts/ needed).
_RENDERER = Path(__file__).resolve().parent.parent / "_scripts" / "wechat_render.py"


@tool
def render_wechat_html(slug: str) -> str:
    """Render content/<slug>/wechat.md into a paste-ready, inline-styled
    wechat.html (for the 公众号 editor). Brand theme read from brand.md. Returns
    the html path, or 'FAIL: ...'."""
    md = config.MEDIA_CONTENT_DIR / slug / "wechat.md"
    if not md.is_file():
        return f"FAIL: wechat.md not found at {md}"
    if not _RENDERER.is_file():
        return f"FAIL: bundled renderer not found at {_RENDERER}"
    proc = subprocess.run(
        [sys.executable, str(_RENDERER), str(md)],
        capture_output=True, text=True, cwd=str(config.WORKSPACE_ROOT), timeout=120,
    )
    if proc.returncode != 0:
        return f"FAIL renderer exited {proc.returncode}: {proc.stderr[:400]}"
    return str(md.with_suffix(".html"))
