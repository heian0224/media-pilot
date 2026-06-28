"""Writing subagent prompt — distilled from platform-writing skill + platform DNA.
M3a focuses on the 公众号 article (wechat.md + wechat-images.json)."""
from __future__ import annotations

from . import brand_preamble
from .platform_dna import WECHAT, XIAOHONGSHU, DOUYIN, BILIBILI
from .. import config
from ..brand import Brand


def render(brand: Brand) -> str:
    p = brand.palette
    return (
        f"今天是 {config.TODAY}。\n\n"
        "你是 media-pilot 的 writing（成稿）子 agent。读取 content/<slug>/strategy.md 和 "
        "discovery.md，为各平台写差异化成稿。**本轮以公众号为必交项**。\n\n"
        "必交产出：\n"
        "1. content/<slug>/wechat.md —— 公众号长文。严格按下方【公众号 DNA】结构；"
        "末尾必须有品牌签名行（含品牌 slogan，触发签名卡）+ 一个含 "
        "关注/在看/转发 + 品牌名 + 品牌 site 的 > 引用块（触发 CTA 卡）。\n"
        "2. content/<slug>/wechat-images.json —— 一个 JSON 数组，描述公众号配图的生成 prompt。"
        "格式：[{\"slot\": \"cover\", \"prompt\": \"...\"}, {\"slot\": \"part1\", \"prompt\": \"...\"}, …]。"
        f"slot 取 cover / part1 / part2 …（与 wechat.md 里的 ![](wechat-partN.png) 一一对应）。"
        f"每个 prompt 是给图像模型的英文描述：深空渐变背景 {p['bg_start']}→{p['bg_end']} + 折射光 "
        f"青 {p['cyan']} / 品红 {p['magenta']}，**烘焙进中文标题/标签**（写明要显示的中文文字），"
        "扁平霓虹线描风，16:9。cover 是封面（带主标题），partN 是对应章节的配图。\n"
        "3.（可选，鼓励）顺带写 xiaohongshu.md / douyin-script.md / bilibili.md。\n"
        "4. 写完用 brand_compliance_check 自检 wechat.md；不通过就修到通过。\n\n"
        f"{WECHAT}\n{XIAOHONGSHU}\n{DOUYIN}\n{BILIBILI}\n\n"
        + brand_preamble.render(brand)
        + "\n\n产出语言：中文（图像 prompt 里描述用英文、要显示的文字用中文）。"
        "返回给编排器：wechat.md 路径、wechat-images.json 路径、品牌自检结果（pass/fail）。"
    )
