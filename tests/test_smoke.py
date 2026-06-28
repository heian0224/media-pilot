"""M1 smoke test: one LLM round-trip over the OpenAI-compatible endpoint.

Skips automatically when no API key is set (so the open-source repo's test
suite doesn't fail for users who haven't wired keys yet)."""
import pytest

from deepagent import config
from deepagent.agent.model import build_model


@pytest.mark.skipif(not config.LLM_API_KEY, reason="no LLM_API_KEY set")
def test_llm_chinese_roundtrip():
    model = build_model(role="default")
    resp = model.invoke("请用中文回答：天空是什么颜色？只输出那个颜色词，不要别的字。")
    text = (resp.content if isinstance(resp.content, str) else str(resp.content)) if resp.content else ""
    assert text.strip(), "LLM returned an empty response"
    assert "蓝" in text, f"expected a Chinese color word (蓝…), got: {text!r}"
