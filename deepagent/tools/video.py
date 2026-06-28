"""HyperFrames video tools: compose a motion-graphics project from the article's
scenes + narration, then render it to mp4. compose uses motion_graphics.template
(12-component engine, brand palette); render shells out to `npx hyperframes render`
(heavy: headless Chrome + ffmpeg)."""
from __future__ import annotations

import json
import shutil
import subprocess

from langchain_core.tools import tool

from .. import brand, config
from ..motion_graphics import build_composition

_PLATFORM_OUT = {"douyin": "douyin.mp4", "bili": "bilibili.mp4"}


@tool
def compose_motion_graphics(slug: str, platform: str = "douyin") -> str:
    """Build a HyperFrames motion-graphics project for content/<slug>/ from its
    video-scenes.json (visual spec per scene) + audio/manifest.json (durations).
    platform: 'douyin' (9:16) or 'bili' (16:9). Brand palette applied. Returns the
    project dir, or 'FAIL: ...' (run tts_narrate first if audio/manifest.json missing)."""
    if platform not in _PLATFORM_OUT:
        return f"FAIL: platform must be 'douyin' or 'bili', got {platform!r}"
    base = config.MEDIA_CONTENT_DIR / slug
    scenes_path = base / "video-scenes.json"
    manifest = base / "audio" / "manifest.json"
    if not scenes_path.is_file():
        return f"FAIL: {scenes_path} not found"
    if not manifest.is_file():
        return "FAIL: audio/manifest.json not found — run tts_narrate first"
    try:
        scenes = json.loads(scenes_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return f"FAIL: video-scenes.json invalid ({e})"

    tuples = [
        (s.get("kind", "card"), s.get("accent", ""), s.get("head", ""),
         s.get("sub", ""), s.get("params", {}) or {})
        for s in scenes
    ]
    b = brand.load_brand()
    proj = base / f"video-{platform}"
    try:
        build_composition(
            f"{slug}-{platform}", tuples, str(manifest), str(proj),
            platform=platform, palette=b.palette,
        )
    except Exception as e:
        return f"FAIL compose: {type(e).__name__}: {e}"
    return str(proj)


@tool
def render_video(slug: str, platform: str = "douyin", timeout: int = 1200) -> str:
    """Render the HyperFrames project (from compose_motion_graphics) to an mp4 and
    place it at content/<slug>/<platform>.mp4 ('douyin'→douyin.mp4, 'bili'→bilibili.mp4).
    Slow — headless Chrome captures every frame. Returns the mp4 path or 'FAIL: ...'."""
    if platform not in _PLATFORM_OUT:
        return f"FAIL: platform must be 'douyin' or 'bili'"
    base = config.MEDIA_CONTENT_DIR / slug
    proj = base / f"video-{platform}"
    if not (proj / "index.html").is_file():
        return f"FAIL: {proj}/index.html not found (run compose_motion_graphics first)"
    proc = subprocess.run(
        ["bash", "-lc", f"cd {proj} && npm run render"],
        capture_output=True, text=True, timeout=timeout,
    )
    if proc.returncode != 0:
        return f"FAIL render exited {proc.returncode}: {proc.stderr[-400:]}"
    renders = proj / "renders"
    mps = sorted(renders.glob("*.mp4"), key=lambda p: p.stat().st_mtime) if renders.is_dir() else []
    if not mps:
        return f"FAIL: no mp4 produced in {renders}. tail: {proc.stdout[-300:]}"
    out = base / _PLATFORM_OUT[platform]
    shutil.copy(mps[-1], out)
    return f"OK: {out} (from {mps[-1].name})"
