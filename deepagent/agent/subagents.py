"""Subagent definitions. discovery + strategy + writing (M3a) + video (M3b)."""
from __future__ import annotations

from ..brand import load_brand
from ..prompts import discovery as discovery_prompt
from ..prompts import strategy as strategy_prompt
from ..prompts import video as video_prompt
from ..prompts import writing as writing_prompt
from ..tools import agnes_video, brand_check, content_io, tts, video as video_tools, web
from .model import build_subagent_model


def build_discovery_subagent() -> dict:
    brand = load_brand()
    return {
        "name": "discovery",
        "description": (
            "选题调研：对一个选题或方向做联网调研，产出 content/<slug>/discovery.md "
            "（调研报告）+ references.json（来源链接）。需要「调研」阶段时委派给它。"
        ),
        "system_prompt": discovery_prompt.render(brand),
        "tools": [web.web_search, web.web_fetch, content_io.write_topic_file, content_io.read_topic_file],
        "model": build_subagent_model("discovery"),
    }


def build_strategy_subagent() -> dict:
    brand = load_brand()
    return {
        "name": "strategy",
        "description": (
            "内容策略：读取 content/<slug>/discovery.md，产出 content/<slug>/strategy.md "
            "（3-5 个差异化角度 + 角度到平台的映射 + 每个目标平台的大纲）。需要「策略」阶段时委派给它。"
        ),
        "system_prompt": strategy_prompt.render(brand),
        "tools": [content_io.read_topic_file, content_io.write_topic_file],
        "model": build_subagent_model("strategy"),
    }


def build_writing_subagent() -> dict:
    brand = load_brand()
    return {
        "name": "writing",
        "description": (
            "写成稿：读取 content/<slug>/strategy.md，写公众号 wechat.md + wechat-images.json"
            "（必交项），可顺带写其他平台。完成后用 brand_compliance_check 自检。需要「写作」阶段时委派给它。"
        ),
        "system_prompt": writing_prompt.render(brand),
        "tools": [content_io.read_topic_file, content_io.write_topic_file, brand_check.brand_compliance_check],
        "model": build_subagent_model("writing"),
    }


def build_video_subagent() -> dict:
    brand = load_brand()
    return {
        "name": "video",
        "description": (
            "做视频：读口播脚本（douyin-script.md / bilibili.md），拆场景，写 video-scenes.json，"
            "TTS 口播，motion-graphics 合成 + 渲染出 mp4（HyperFrames 路线）。可选 generate_video_clip "
            "加 Agnes 真实 footage（易过载，失败回退 HyperFrames）。需要「视频」阶段时委派给它。"
        ),
        "system_prompt": video_prompt.render(brand),
        "tools": [
            tts.tts_narrate,
            video_tools.compose_motion_graphics,
            video_tools.render_video,
            agnes_video.generate_video_clip,
            content_io.read_topic_file,
            content_io.write_topic_file,
        ],
        "model": build_subagent_model("video"),
    }


def build_subagents() -> list:
    return [
        build_discovery_subagent(),
        build_strategy_subagent(),
        build_writing_subagent(),
        build_video_subagent(),
    ]
