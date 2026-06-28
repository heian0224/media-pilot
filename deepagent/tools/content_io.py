"""Content-folder I/O tools: anchored to content/<slug>/, escape-proof, with
de-duplication helpers. These write REAL files into the workspace content/ dir
(the convention), not the agent's ephemeral virtual FS."""
from __future__ import annotations

from pathlib import Path

from langchain_core.tools import tool

from .. import config

_CONTENT = config.MEDIA_CONTENT_DIR


def _resolve(slug: str, filename: str) -> Path:
    """Resolve content/<slug>/<filename> and refuse anything that escapes."""
    base = (_CONTENT / slug).resolve()
    content_resolved = _CONTENT.resolve()
    if base != content_resolved and content_resolved not in base.parents:
        raise ValueError(f"path escapes content dir: {slug}/{filename}")
    return base / filename


@tool
def write_topic_file(slug: str, filename: str, content: str) -> str:
    """Write text to content/<slug>/<filename> (creates the topic folder). Use this
    for discovery.md, strategy.md, wechat.md, manifest.json, etc. Returns the
    absolute path written. slug = kebab-case topic id (e.g. 2026-06-27-ai-backlash)."""
    path = _resolve(slug, filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


@tool
def read_topic_file(slug: str, filename: str) -> str:
    """Read content/<slug>/<filename> and return its text. Returns a 'NOT FOUND'
    message if the file is missing (do not retry blindly — check the path)."""
    path = _resolve(slug, filename)
    if not path.is_file():
        return f"NOT FOUND: {path}"
    return path.read_text(encoding="utf-8")


@tool
def list_topics() -> str:
    """List existing topic-folder slugs under content/ (for de-duplication / to see
    what's already been produced). Returns newline-joined slugs, newest-relevant."""
    if not _CONTENT.is_dir():
        return "(no topics yet)"
    names = sorted(p.name for p in _CONTENT.iterdir() if p.is_dir())
    return "\n".join(names) if names else "(no topics yet)"


@tool
def topic_slug_exists(slug: str) -> bool:
    """Return True if content/<slug>/ already exists (the topic has been done).
    Use before starting a run to avoid duplicate topics."""
    return (_CONTENT / slug).is_dir()
