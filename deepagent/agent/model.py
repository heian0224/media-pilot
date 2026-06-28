"""LLM model construction.

Default model is **GLM (智谱)** reached via its OpenAI-compatible endpoint — but
any OpenAI-compatible provider works by swapping ``base_url`` / ``model`` /
``api_key`` (e.g. DeepSeek, Moonshot, OpenAI itself). Per-role temperature presets
follow the plan: orchestrator plans cooler (0.5), writing runs hotter (0.85).
"""
from __future__ import annotations

from langchain_openai import ChatOpenAI

from .. import config

# role -> temperature
_ROLE_TEMP = {
    "orchestrator": 0.5,
    "discovery": 0.6,
    "strategy": 0.6,
    "writing": 0.85,
    "video": 0.4,
    "default": 0.7,
}


def build_model(
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    temperature: float | None = None,
    role: str | None = None,
    streaming: bool = False,
) -> ChatOpenAI:
    """Construct a ChatOpenAI pointed at the configured OpenAI-compatible endpoint.

    ``role`` selects a default temperature; an explicit ``temperature`` wins.
    """
    key = api_key or config.LLM_API_KEY
    if not key:
        raise RuntimeError(
            "No LLM API key set. Set OPENAI_API_KEY (or GLM_API_KEY) — see "
            ".claude/settings.local.json / .env / brand.example.md."
        )
    temp = temperature if temperature is not None else _ROLE_TEMP.get(role or "default", 0.7)
    return ChatOpenAI(
        model=model or config.LLM_MODEL,
        base_url=base_url or config.LLM_BASE_URL,
        api_key=key,
        temperature=temp,
        streaming=streaming,
    )


def build_orchestrator_model() -> ChatOpenAI:
    return build_model(role="orchestrator")


def build_subagent_model(role: str) -> ChatOpenAI:
    return build_model(role=role)
