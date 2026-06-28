"""Autonomous topic selection: survey trending AI topics, de-dup against the
content/ history, return one pick. Powers ``run --auto``."""
from __future__ import annotations

import json
import re

from deepagents import create_deep_agent
from deepagents.backends import StateBackend

from .. import config
from ..agent.model import build_subagent_model
from ..tools.content_io import list_topics, topic_slug_exists
from ..tools.web import web_search

_PICK_PROMPT = (
    "你是一个自媒体选题编辑。任务：挑出当前最值得写的一个 AI 选题。"
    "用 web_search 调研最新热点（国际：Hacker News / Reddit / arXiv / AI lab blogs；"
    "中文：微博 / 知乎 / B站 / 36氪），优先选有真实热度、有数据/事件、且中国读者关心的。"
    "用 topic_slug_exists 核对候选 slug 没被用过——绝不重复已做过的题。"
    "最后只返回一个 JSON 对象，不要任何多余文字："
    '{"topic": "<中文选题，一句话>", "slug": "<YYYY-MM-DD>-<英文kebab-slug>", "reason": "<为什么值得写，1-2句>"}'
)


def recent_slugs(n: int = 12) -> list[str]:
    """Newest-first list of existing topic-folder slugs under content/."""
    c = config.MEDIA_CONTENT_DIR
    if not c.is_dir():
        return []
    names = [p.name for p in c.iterdir() if p.is_dir()]
    # sort by leading date desc, then name
    return sorted(names, key=lambda s: (s[:10], s), reverse=True)[:n]


def _core(slug: str) -> str:
    """Strip the leading YYYY-MM-DD- from a slug for same-topic detection."""
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)


def is_duplicate(slug: str, recent: list[str]) -> bool:
    """True if the exact slug exists OR the date-stripped core matches a recent one."""
    if slug in recent:
        return True
    core = _core(slug)
    return any(_core(r) == core for r in recent)


def pick_auto_topic(retries: int = 2) -> dict:
    """Survey trends + de-dup, return {'topic', 'slug', 'reason'}. Re-rolls if the
    pick duplicates a recent topic (bounded by ``retries``)."""
    recent = recent_slugs()
    agent = create_deep_agent(
        model=build_subagent_model("discovery"),
        tools=[web_search, list_topics, topic_slug_exists],
        system_prompt=_PICK_PROMPT,
        backend=StateBackend(),
    )
    msg = (
        f"今天是 {config.TODAY}。挑一个最值得写的 AI 选题。近期已做过、要避开重复的选题："
        f"{recent[:10] or '(暂无)'}。"
    )
    last_pick: dict = {}
    for _ in range(retries + 1):
        result = agent.invoke({"messages": [{"role": "user", "content": msg}]})
        text = getattr(result["messages"][-1], "content", "") or ""
        m = re.search(r'\{[^{}]*"topic"[^{}]*\}', text, re.S)
        if not m:
            last_pick = {"topic": text.strip()[:80], "slug": "", "reason": "parse-fail"}
            break
        try:
            pick = json.loads(m.group(0))
        except json.JSONDecodeError:
            last_pick = {"topic": text.strip()[:80], "slug": "", "reason": "parse-fail"}
            break
        last_pick = pick
        slug = pick.get("slug", "")
        if slug and not is_duplicate(slug, recent):
            return pick
    return last_pick
