"""Pre-run + post-run guardrails for unattended/autonomous runs."""
from __future__ import annotations

import json

from .. import config
from ..brand import load_brand

# key -> (env attr, is it fatal if missing)
_KEY_CHECKS = [
    ("LLM_API_KEY", "LLM_API_KEY", True),       # fatal: nothing runs without the LLM
    ("MINIMAX_API_KEY", "MINIMAX_API_KEY", False),
    ("GPT_IMAGE_API_KEY", "GPT_IMAGE_API_KEY", False),
    ("TAVILY_API_KEY", "TAVILY_API_KEY", False),
]


def pre_run_checks() -> list[str]:
    """Return a list of issue strings (empty = all good). Missing TAVILY/MINIMAX/
    GPT_IMAGE are warnings (those stages degrade); missing LLM_API_KEY is fatal."""
    issues = []
    for _, attr, _ in _KEY_CHECKS:
        if not getattr(config, attr, ""):
            issues.append(f"{attr} not set")
    if not config.MEDIA_CONTENT_DIR.parent.exists():
        issues.append(f"content parent dir missing: {config.MEDIA_CONTENT_DIR.parent}")
    return issues


def fatal_issues(issues: list[str]) -> list[str]:
    return [i for i in issues if "LLM_API_KEY" in i]


def post_run_verify(slug: str) -> dict:
    """Verify a finished run's outputs. Returns a report dict with per-check booleans
    and an overall 'complete' flag (manifest completeness all-true)."""
    d = config.MEDIA_CONTENT_DIR / slug
    report = {"slug": slug, "complete": False, "checks": {}, "missing": []}
    checks = report["checks"]

    manifest = d / "manifest.json"
    comp = {}
    if manifest.is_file():
        try:
            comp = json.loads(manifest.read_text(encoding="utf-8")).get("completeness", {})
        except json.JSONDecodeError:
            pass
    checks["manifest_completeness"] = comp
    report["complete"] = bool(comp) and all(comp.values())

    for label, fname in [
        ("discovery_md", "discovery.md"), ("strategy_md", "strategy.md"),
        ("wechat_md", "wechat.md"), ("wechat_html", "wechat.html"),
        ("douyin_script_md", "douyin-script.md"), ("douyin_mp4", "douyin.mp4"),
    ]:
        ok = (d / fname).is_file()
        checks[label] = ok
        if not ok:
            report["missing"].append(fname)

    # brand sign-off present in the 公众号 article
    b = load_brand()
    wm = (d / "wechat.md").read_text(encoding="utf-8") if (d / "wechat.md").is_file() else ""
    checks["brand_signoff_in_wechat"] = bool(b.present and b.name in wm)
    return report
