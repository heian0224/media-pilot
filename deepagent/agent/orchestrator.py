"""Orchestrator assembly: create_deep_agent(model, tools, system_prompt, subagents, backend)."""
from __future__ import annotations

from deepagents import create_deep_agent

from ..prompts.orchestrator import ORCHESTRATOR_PROMPT
from ..tools import brand_check, content_io, images, wechat_render
from .backends import build_backend
from .model import build_orchestrator_model
from .subagents import build_subagents


def build_orchestrator():
    return create_deep_agent(
        model=build_orchestrator_model(),
        tools=[
            content_io.list_topics,
            content_io.topic_slug_exists,
            content_io.write_topic_file,
            content_io.read_topic_file,
            brand_check.brand_compliance_check,
            wechat_render.render_wechat_html,
            images.generate_images,
        ],
        system_prompt=ORCHESTRATOR_PROMPT,
        subagents=build_subagents(),
        backend=build_backend(),
    )
