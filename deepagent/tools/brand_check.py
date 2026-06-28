"""Brand-compliance check tool: verifies a produced file carries the brand
identity (account name, site, slogan). Used by the writing subagent to self-check
and by the orchestrator as a guardrail."""
from __future__ import annotations

from langchain_core.tools import tool

from .. import config
from ..brand import load_brand


@tool
def brand_compliance_check(slug: str, filename: str) -> str:
    """Check content/<slug>/<filename> for brand compliance. Verifies the brand
    account name, site, and a slogan fragment are all present. Returns
    'PASS: ...' or 'FAIL: <missing items>'. Call after writing wechat.md etc."""
    path = config.MEDIA_CONTENT_DIR / slug / filename
    if not path.is_file():
        return f"FAIL: file not found — {path}"
    text = path.read_text(encoding="utf-8")
    b = load_brand()
    if not b.present:
        return "PASS (no brand.md configured — nothing to check)."
    missing = []
    if b.name and b.name not in text:
        missing.append(f"账号名「{b.name}」")
    if b.site and b.site not in text:
        missing.append(f"网站 {b.site}")
    slogan_key = b.slogan.split("，")[0] if b.slogan else ""
    if slogan_key and slogan_key not in text:
        missing.append(f"slogan 片段「{slogan_key}」")
    if missing:
        return "FAIL: 缺少 " + " / ".join(missing)
    return f"PASS: 品牌名 + 网站 + slogan 均在文中。"
