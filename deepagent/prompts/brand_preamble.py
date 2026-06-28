"""Shared brand block, rendered from a parsed Brand and injected into subagents."""
from __future__ import annotations

from ..brand import Brand


def render(brand: Brand) -> str:
    if not brand.present:
        return (
            "（未找到 brand.md；按「无品牌」处理：不要署名任何账号、不要编造品牌名、"
            "配色用深空 #0B1026→#1E1B4B + 青 #22D3EE / 品红 #F472B6。）"
        )
    p = brand.palette
    return (
        "品牌规范（所有产出必须严格遵循）：\n"
        f"- 账号名：{brand.name}（{brand.name_en}）\n"
        f"- Slogan：{brand.slogan}\n"
        f"- 网站：{brand.site}\n"
        f"- CTA 签名：{brand.sign_off}（不要用泛化的「关注我」）\n"
        f"- 视觉：深空渐变 {p['bg_start']}→{p['bg_end']}，"
        f"折射光 青 {p['cyan']} + 品红 {p['magenta']} + 紫 {p['purple']}\n"
        "- 招牌动作词：折射（替代解码/拆解/揭秘）\n"
        "若某字段缺失，按缺失处理，绝不编造品牌信息。"
    )
