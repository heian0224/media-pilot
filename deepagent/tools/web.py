"""Web research tools (Tavily): web_search + web_fetch."""
from __future__ import annotations

from functools import lru_cache

from langchain_core.tools import tool
from tavily import TavilyClient

from .. import config


@lru_cache(maxsize=1)
def _client() -> TavilyClient:
    if not config.TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY not set — discovery cannot search the web.")
    return TavilyClient(api_key=config.TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """Search the web (Chinese + international sources) for fresh info on a query.
    Returns up to 6 results as 'title / url / snippet' blocks. Use for trending
    and topic research. Argument: a focused search query (Chinese or English)."""
    res = _client().search(query=query, max_results=6, search_depth="advanced")
    items = res.get("results", []) if isinstance(res, dict) else []
    lines = []
    for x in items:
        title = x.get("title", "")
        url = x.get("url", "")
        snip = (x.get("content") or "").strip().replace("\n", " ")[:320]
        lines.append(f"- {title}\n  {url}\n  {snip}")
    return "\n".join(lines) if lines else "(no results)"


@tool
def web_fetch(url: str) -> str:
    """Fetch a single URL and return its main text content (truncated). Use to read
    an article / blog / paper page in depth after finding it via web_search.
    Argument: the full https URL."""
    res = _client().extract(urls=[url])
    results = res.get("results", []) if isinstance(res, dict) else []
    if results:
        body = (results[0].get("content") or "").strip()
        return body[:4000] if body else "(empty content)"
    return f"(extract failed: {res.get('failed') if isinstance(res, dict) else res})"
