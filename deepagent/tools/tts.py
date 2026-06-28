"""MiniMax Mandarin narration tool. Wraps the workspace's scripts/run_tts.py
(direct curl --http1.1, proxy-off, voice male-qn-qingse). Reads the 'narration'
field of each scene in content/<slug>/video-scenes.json, one clip per scene,
writing audio/sceneN.mp3 + audio/manifest.json (durations drive the composition)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from langchain_core.tools import tool

from .. import config

# Bundled MiniMax TTS runner (self-contained — no workspace scripts/ needed).
_TTS = Path(__file__).resolve().parent.parent / "_scripts" / "run_tts.py"


@tool
def tts_narrate(slug: str, scenes_file: str = "video-scenes.json", audio_subdir: str = "audio") -> str:
    """Generate Mandarin narration (MiniMax) for content/<slug>/<scenes_file>.
    Each scene object's 'narration' string becomes one sceneN.mp3; writes
    <audio_subdir>/manifest.json with per-clip durations (the composition needs these).
    Returns 'OK: <n> scenes → <manifest>' or 'FAIL: ...'."""
    if not config.MINIMAX_API_KEY:
        return "FAIL: MINIMAX_API_KEY not set"
    base = config.MEDIA_CONTENT_DIR / slug
    scenes_path = base / scenes_file
    if not scenes_path.is_file():
        return f"FAIL: {scenes_path} not found"
    try:
        scenes = json.loads(scenes_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return f"FAIL: {scenes_file} not valid JSON ({e})"

    narrations = [s.get("narration", "").strip() for s in scenes]
    if not narrations:
        return "FAIL: no scenes"
    missing = [i + 1 for i, n in enumerate(narrations) if not n]
    if missing:
        return f"FAIL: scenes {missing} missing 'narration'"

    audio_dir = base / audio_subdir
    audio_dir.mkdir(parents=True, exist_ok=True)
    scenes_txt = base / ".tts-scenes.txt"
    scenes_txt.write_text("\n".join(narrations), encoding="utf-8")

    script = _TTS
    if not script.is_file():
        scenes_txt.unlink(missing_ok=True)
        return f"FAIL: bundled run_tts.py not found at {script}"
    proc = subprocess.run(
        [
            sys.executable, str(script),
            "--scenes", str(scenes_txt),
            "--out", str(audio_dir),
            "--voice", config.TTS_VOICE,
            "--speed", str(config.TTS_SPEED),
        ],
        capture_output=True, text=True, cwd=str(config.WORKSPACE_ROOT), timeout=1200,
    )
    scenes_txt.unlink(missing_ok=True)
    if proc.returncode != 0:
        return f"FAIL tts exited {proc.returncode}: {proc.stderr[-400:]}"
    manifest = audio_dir / "manifest.json"
    if not manifest.is_file():
        return f"FAIL: no manifest.json. tail: {proc.stdout[-300:]}"
    return f"OK: {len(narrations)} scenes narrated → {manifest}"
