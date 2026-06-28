"""Run one topic through the orchestrator (M2: discovery stage only)."""
from __future__ import annotations

from .. import config
import json

from .orchestrator import build_orchestrator


def _write_manifest_for_latest_today() -> str | None:
    """Guarantee a manifest.json for the newest content/<TODAY>-*/ folder, listing
    its files + per-stage completeness. Belt-and-suspenders — doesn't rely on the
    agent remembering to write one."""
    base = config.MEDIA_CONTENT_DIR
    cands = sorted(
        [p for p in base.glob(f"{config.TODAY}-*") if p.is_dir()],
        key=lambda p: p.stat().st_mtime,
    )
    if not cands:
        return None
    d = cands[-1]
    files = sorted(p.name for p in d.iterdir() if p.is_file())
    manifest = {
        "date": config.TODAY,
        "slug": d.name,
        "files": files,
        "completeness": {
            "discovery": (d / "discovery.md").is_file(),
            "strategy": (d / "strategy.md").is_file(),
            "writing": (d / "wechat.md").is_file(),
            "html": (d / "wechat.html").is_file(),
            "images": bool(list(d.glob("wechat-*.png"))),
            "video": bool(list(d.glob("*.mp4"))),
        },
    }
    out = d / "manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)


def run_topic(topic: str, verbose: bool = True) -> dict:
    agent = build_orchestrator()
    user_msg = (
        f"今天是 {config.TODAY}。选题：「{topic}」。按当前（M3）范围执行完整流水线：\n"
        f"1) topic_slug_exists 确认没撞题（slug 必须以 {config.TODAY}- 开头，英文/拼音 kebab-case）；\n"
        f"2) 委派 discovery（调研）→ strategy（策略）；\n"
        f"3) 委派 writing，要求它产出 wechat.md + wechat-images.json + **douyin-script.md**（都必交）；\n"
        f"4) 你**先** generate_images(slug) 再 render_wechat_html(slug)（顺序关键）；\n"
        f"5) 委派 video 子 agent 做抖音竖版视频（platform=douyin，脚本读 douyin-script.md）。\n"
        f"每阶段 read_topic_file 核对落盘。返回：一句话结论 + slug + 文件清单（含 douyin.mp4）。"
    )
    result = agent.invoke({"messages": [{"role": "user", "content": user_msg}]})
    manifest_path = _write_manifest_for_latest_today()
    if verbose:
        last = result["messages"][-1]
        text = getattr(last, "content", str(last))
        print(text if isinstance(text, str) else str(text))
        if manifest_path:
            print(f"\n[manifest] {manifest_path}")
    return result
