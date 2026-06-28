"""Runtime configuration: workspace paths + secret loading.

Secrets/keys are loaded with this precedence (first wins; the real process
environment is never overwritten):

    1. ``$MEDIA_WORKSPACE_ROOT/.claude/settings.local.json`` ``env`` block
       (the existing home for keys in this workspace; gitignored)
    2. a ``.env`` at the workspace root          (open-source friendly)
    3. a ``.env`` next to this package            (where the user put theirs)
    4. the real process environment

The LLM is wired OpenAI-compatibly — set ``OPENAI_API_KEY`` + ``OPENAI_BASE_URL``
(or the ``GLM_*`` aliases). Nothing here is brand-specific and no key is baked in.
"""
from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

# double + single quote, built without quote literals to dodge source-encoding pitfalls
_QUOTE_CHARS = chr(34) + chr(39)


def _detect_workspace_root() -> Path:
    """Find the workspace root: an ancestor (or cwd ancestor) containing both
    a ``content/`` dir and a ``brand.md``. Falls back to cwd."""
    env_root = os.environ.get("MEDIA_WORKSPACE_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    def _is_root(p: Path) -> bool:
        return (p / "content").is_dir() and (p / "brand.md").is_file()

    for cand in [Path.cwd().resolve(), *Path.cwd().resolve().parents]:
        if _is_root(cand):
            return cand
    pkg = Path(__file__).resolve()
    for cand in [pkg.parent, *pkg.parents]:
        if _is_root(cand):
            return cand
    return Path.cwd().resolve()


def _apply(k: str, v) -> None:
    if isinstance(v, str) and k not in os.environ:
        os.environ[k] = v


def _load_settings_json(root: Path) -> None:
    sfile = root / ".claude" / "settings.local.json"
    if not sfile.is_file():
        return
    try:
        data = json.loads(sfile.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    env_block = data.get("env") if isinstance(data, dict) else None
    if isinstance(env_block, dict):
        for k, v in env_block.items():
            _apply(k, v)


def _load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        _apply(k.strip(), v.strip().strip(_QUOTE_CHARS))


WORKSPACE_ROOT: Path = _detect_workspace_root()
PKG_DIR: Path = Path(__file__).resolve().parent

# Today's real date (system clock) — injected into prompts so the agent uses the
# correct YYYY-MM-DD in topic slugs and reports instead of guessing its cutoff date.
TODAY: str = date.today().isoformat()

# load order: settings.local.json -> workspace .env -> package .env
_load_settings_json(WORKSPACE_ROOT)
_load_dotenv(WORKSPACE_ROOT / ".env")
_load_dotenv(PKG_DIR / ".env")

# --- Paths (overridable via env) ---
BRAND_MD_PATH: Path = Path(os.environ.get("BRAND_MD_PATH", str(WORKSPACE_ROOT / "brand.md"))).expanduser()
MEDIA_CONTENT_DIR: Path = Path(os.environ.get("MEDIA_CONTENT_DIR", str(WORKSPACE_ROOT / "content"))).expanduser()
LOG_DIR: Path = Path(os.environ.get("MEDIA_PILOT_LOG_DIR", str(WORKSPACE_ROOT / "logs"))).expanduser()


def _first(*names: str, default: str = "") -> str:
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return default


# --- LLM (OpenAI-compatible). GLM_* aliases win, then OPENAI_*. ---
LLM_API_KEY: str = _first("GLM_API_KEY", "OPENAI_API_KEY", "ZHIPU_API_KEY", "DEEPSEEK_API_KEY")
LLM_BASE_URL: str = _first("GLM_BASE_URL", "OPENAI_BASE_URL", default="https://open.bigmodel.cn/api/paas/v4")
LLM_MODEL: str = _first("GLM_MODEL", "OPENAI_MODEL", default="glm-4.6")
# Vision model (for image-text verification / re-roll). Same endpoint, vision-capable model.
LLM_VISION_MODEL: str = os.environ.get("LLM_VISION_MODEL", "glm-4v-flash")
# Max re-roll attempts when a generated image's Chinese text fails verification.
IMAGE_REROLL_ATTEMPTS: int = int(os.environ.get("IMAGE_REROLL_ATTEMPTS", "3"))

# --- Other service keys ---
MINIMAX_API_KEY: str = os.environ.get("MINIMAX_API_KEY", "")
GPT_IMAGE_API_KEY: str = os.environ.get("GPT_IMAGE_API_KEY", "")
GPT_IMAGE_ENDPOINT: str = os.environ.get("GPT_IMAGE_ENDPOINT", "https://api.openai.com/v1/images/generations")
TAVILY_API_KEY: str = os.environ.get("TAVILY_API_KEY", "")
# Agnes (OpenAI-compatible text/image/video; video model agnes-video-v2.0)
AGNES_API_KEY: str = os.environ.get("AGNES_API_KEY", "")
AGNES_BASE_URL: str = os.environ.get("AGNES_BASE_URL", "https://apihub.agnes-ai.com").rstrip("/")
NOTIFY_WEBHOOK_URL: str = os.environ.get("NOTIFY_WEBHOOK_URL", "")

# MiniMax TTS defaults
TTS_VOICE: str = os.environ.get("MEDIA_PILOT_TTS_VOICE", "male-qn-qingse")
TTS_SPEED: float = float(os.environ.get("MEDIA_PILOT_TTS_SPEED", "1.3"))


def ensure_content_dir() -> Path:
    MEDIA_CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    return MEDIA_CONTENT_DIR
