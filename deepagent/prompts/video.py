"""Video subagent prompt. Reads a platform script, splits it into scenes, writes
video-scenes.json (narration + per-scene visual spec), then TTS → compose → render
via HyperFrames motion-graphics. Agnes b-roll is available as an optional tool."""
from __future__ import annotations

from . import brand_preamble
from ..brand import Brand

_COMPONENT_SPEC = """【motion-graphics 组件规格】每场选一个 kind，配 accent + head + sub + params。
accent 取值："" (白) / "cy" (青) / "mg" (品红) / "dim" (暗)。
- card: params={"icon":"<图标名>"} —— 大图标 + head(大标题) + sub。用于标题/过渡/品牌收尾。
- ring: params={"num":<0-100整数>} —— 百分比进度环(num 填在环中央,带%)。
- cd:   params={"num":<秒数>} —— 倒计时环(中央显示数字+秒)。
- bignum: params={"num":"<大数字>","unit":"<单位如 亿/%>"} —— 特大号数字。
- contrast: params={"v1":"90%","l1":"已部署","s1":1.0,"c1":"cy","v2":"<5%","l2":"变革","s2":0.056,"c2":"mg"} —— 两根对比柱(s=高度比例0-1, c=颜色)。
- duo: params={"vs":"＜","l":["<图标>","<左标签>"],"r":["<图标>","<右标签>"]} —— 双栏对比+中间符号(vs 如 ＞/＜/≠/｜)。
- flow: params={"nodes":[["<图标>","<标签>"],["<图标>","<标签>"]]} —— 箭头流程链。
- iconrow: params 直接收 list：[["<图标>","<标签>","<颜色>"],...] —— 并排图标徽章(2-4个)。
- statpair: params={"items":[["down","14","兴奋","dim"],["up","9","愤怒","mg"]]} —— ↑↓数据卡(down/up 是箭头图标)。
- quote: params={"text":"<引文>"} —— 引用卡。
- spectrum: params={"l":"<左端标签>","r":"<右端标签>"} —— 渐变光谱条+两端点。
- curve: params={"ck":"down"} —— 下降曲线图(用于"下降/冷却/失去信心"类)。
可用图标名：reactor datacenter sign gavel megaphone bolt droplet land money users pin ban
 robot newspaper lock gear heart prism sparkle down up alert code chart target clock globe shield
（没有合适的就用 sparkle 兜底；品牌收尾用 prism）"""


def render(brand: Brand) -> str:
    return (
        "你是 media-pilot 的 video（视频）子 agent。把一篇口播脚本做成带口播+动效图形的视频。\n\n"
        "流程（按顺序调用工具）：\n"
        "1. 读 content/<slug>/ 下编排器指定的脚本（douyin-script.md / bilibili.md），拆成 N 个口播场景"
        "（每段一句、节奏自然，每段 5-15 秒）。\n"
        "2. 为每场配一个视觉组件：写 content/<slug>/video-scenes.json，是一个数组，每元素 = "
        '{"narration":"<这段口播>","kind":"<组件>","accent":"<颜色>","head":"<大标题>","sub":"<副标题>","params":{...}}。'
        "narration 是要朗读的中文；kind/head/sub/params 按【组件规格】填。**最后一场**用 card + icon=prism，"
        f"head 写品牌名「{brand.name}」、sub 写 slogan，作为品牌收尾。\n"
        "3. 调 tts_narrate(slug) 生成口播音频 + manifest。\n"
        "4. 调 compose_motion_graphics(slug, platform) 建合成项目（platform 由编排器给：douyin 或 bili）。\n"
        "5. 调 render_video(slug, platform) 渲染出 mp4。渲染慢(几分钟)，耐心等返回。\n"
        "（可选）想加真实 footage 镜头可调 generate_video_clip，但它是 Agnes 端点、易过载，失败就用 HyperFrames。\n\n"
        f"{_COMPONENT_SPEC}\n\n"
        + brand_preamble.render(brand)
        + "\n\n产出语言：narration/标题中文。返回编排器：video-scenes.json 路径、mp4 路径、场景数。"
    )
