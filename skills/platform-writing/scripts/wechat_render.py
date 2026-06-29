#!/usr/bin/env python3
"""
wechat_render.py — 把 wechat.md 渲染成「可直接粘贴进微信公众号」的富文本 HTML。

== 它解决什么 ==
公众号后台只保留行内样式 (style="...")，会丢弃 <style> 标签和 CSS class。
本脚本把品牌主题 CSS 全部烘焙成每个元素的 inline style，输出自包含的 wechat.html：
浏览器打开即所见即所得，选中内容 Ctrl+C → 公众号后台 Ctrl+V，样式完整保留。

== 使用流程 ==
1. python3 scripts/wechat_render.py [path/to/wechat.md] [-o out.html] [--urls urls.json]
   （默认：找最新的 content/*/wechat.md，输出同目录 wechat.html）
2. 浏览器打开 wechat.html 预览
3. 选中白色文章区（或 Ctrl+A）→ Ctrl+C
4. 公众号后台新建图文 → 编辑器 Ctrl+V → 样式保留 ✅

== 关于图片（重要）==
公众号粘贴时只抓取「公网可访问的图片 URL」，本地相对路径 / data-uri 不会带过去。
所以：
  • 文字 / 排版：一次粘贴全部到位。
  • 7 张 PNG：在公众号编辑器里用「图片」工具拖入文中已标好的位置。
若图已传图床，准备 urls.json：{"cover":"https://.../c.jpg","part1":"https://.../1.jpg",...}
用 --urls urls.json 传入，<img src> 换成 URL，图片也能一次粘贴到位。

品牌：黯镜 AI（深空 + 青/品红折射），见 workspace 根 brand.md。
"""
import argparse
import glob
import html
import json
import os
import re
import shutil
import sys

# ───────────────────────── 品牌主题（inline style 常量） ─────────────────────────
FONT = ('font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",'
        '"Helvetica Neue","Segoe UI",Roboto,"Hiragino Sans GB",sans-serif;')
INK = "#2b2b3a"          # 正文
INK_DEEP = "#0B1026"     # 标题 / 重点
CY = "#22D3EE"           # 折射光 · 青
MG = "#F472B6"           # 折射光 · 品红
VI = "#7C3AED"           # 折射光 · 紫
LAV = "#F5F3FF"          # 浅紫底
LAV2 = "#FAF9FF"
MUTE = "#9a9ab0"

S_CONTAINER = (f"max-width:600px;margin:0 auto;padding:8px 18px 56px;{FONT}"
               f"color:{INK};font-size:16px;line-height:1.85;letter-spacing:.3px;")
S_H1 = (f"font-size:25px;font-weight:800;color:{INK_DEEP};line-height:1.4;"
        f"margin:28px 0 6px;letter-spacing:.5px;")
S_KICKER = (f"font-size:13px;font-weight:700;color:{MG};letter-spacing:2px;"
            f"margin:0 0 18px;text-transform:uppercase;")
S_LEAD = (f"margin:0 0 26px;padding:16px 20px;background:{LAV};border-left:4px solid {CY};"
          f"border-radius:6px;font-size:16px;color:#4b4b66;line-height:1.85;")
S_H2 = (f"margin:40px 0 18px;font-size:21px;font-weight:800;color:{INK_DEEP};"
        f"line-height:1.45;padding-left:14px;border-left:5px solid {MG};")
S_H3 = f"margin:26px 0 12px;font-size:17px;font-weight:700;color:{VI};line-height:1.5;"
S_P = "margin:0 0 18px;"
S_STRONG = f"color:{INK_DEEP};font-weight:700;"
S_EM = f"color:{VI};font-style:normal;font-weight:500;"
S_CODE = (f"background:{LAV};color:{VI};padding:2px 6px;border-radius:4px;"
          f"font-size:14px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;")
S_QUOTE = (f"margin:26px 0;padding:16px 20px;background:{LAV2};border-left:4px solid {VI};"
           f"border-radius:8px;color:#4b4b66;font-size:15px;line-height:1.85;")
S_HR = (f'<div style="height:1px;margin:34px 0;'
        f'background:linear-gradient(90deg,transparent,{CY},{MG},transparent);"></div>')
S_LI = "margin:9px 0;padding-left:1.3em;text-indent:-1.3em;line-height:1.8;"
S_SRC = f"font-size:13px;color:{MUTE};line-height:1.75;margin:0 0 18px;"
S_FIG = "margin:30px 0 10px;text-align:center;"
S_IMG = "width:100%;max-width:600px;border-radius:10px;display:block;margin:0 auto;"
S_CAP = f"margin-top:8px;font-size:13px;color:{MUTE};line-height:1.6;"
S_IMGPLACE = (f"margin:30px 0;padding:18px;border:1.5px dashed #c9c9e0;border-radius:10px;"
              f"text-align:center;color:{MUTE};font-size:14px;background:{LAV2};")

CAPTIONS = {}  # optional auto-captions for numbered ## 01–05 headings, e.g. {"part1": "图｜…"}. Empty by default.

# 末尾品牌收尾图：共享品牌资产，所有文章复用。位置无关——从 cwd 和本文件向上查找
# brand/assets/wechat-signoff.png；找不到则跳过（签名卡仍以文本/HTML 渲染，不影响出图）。
def _find_signoff():
    roots = [os.getcwd(), os.path.dirname(os.path.abspath(__file__))]
    for start in roots:
        d = start
        for _ in range(8):
            cand = os.path.join(d, "brand", "assets", "wechat-signoff.png")
            if os.path.exists(cand):
                return cand
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
    return None

BRAND_SIGNOFF = _find_signoff()


# ───────────────────────── markdown 行内格式 ─────────────────────────
def inline(t: str) -> str:
    t = html.escape(t)
    codes = []

    def code_sub(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    t = re.sub(r"`([^`]+)`", code_sub, t)
    t = re.sub(r"\*\*(.+?)\*\*", rf'<strong style="{S_STRONG}">\1</strong>', t)
    t = re.sub(r"\*([^*]+?)\*", rf'<em style="{S_EM}">\1</em>', t)

    def code_back(m):
        return f'<code style="{S_CODE}">{codes[int(m.group(1))]}</code>'

    return re.sub(r"\x00(\d+)\x00", code_back, t)


# ───────────────────────── 解析 markdown → blocks ─────────────────────────
def parse(md: str):
    lines = md.replace("\r\n", "\n").split("\n")
    blocks = []
    para, quote, lst, lst_type = [], [], [], None

    def flush_para():
        if para:
            blocks.append(("p", "\n".join(para))); para.clear()

    def flush_quote():
        if quote:
            blocks.append(("quote", list(quote))); quote.clear()

    def flush_list():
        nonlocal lst_type
        if lst:
            blocks.append(("list", lst_type, list(lst))); lst.clear()
        lst_type = None

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_para(); flush_quote(); flush_list(); continue
        if re.match(r"^-{3,}$", line):
            flush_para(); flush_quote(); flush_list()
            blocks.append(("hr", None)); continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_para(); flush_quote(); flush_list()
            blocks.append(("h", len(m.group(1)), m.group(2))); continue
        if line.startswith(">"):
            flush_para(); flush_list()
            quote.append(line[1:].lstrip()); continue
        m = re.match(r"^([-*])\s+(.*)$", line)
        if m:
            flush_para(); flush_quote()
            lst.append(m.group(2)); lst_type = "ul"; continue
        m = re.match(r"^(\d+)\.\s+(.*)$", line)
        if m:
            flush_para(); flush_quote()
            lst.append(m.group(2)); lst_type = "ol"; continue
        flush_quote(); flush_list()
        para.append(line)
    flush_para(); flush_quote(); flush_list()
    return blocks


# ───────────────────────── 组件 ─────────────────────────
def img_tag(src, alt="", caption=""):
    cap = f'<figcaption style="{S_CAP}">{caption}</figcaption>' if caption else ""
    return (f'<figure style="{S_FIG}"><img src="{src}" alt="{html.escape(alt)}" '
            f'style="{S_IMG}"/>{cap}</figure>')


def img_placeholder(label, caption=""):
    cap = f"<br>{caption}" if caption else ""
    return (f'<div style="{S_IMGPLACE}">📷 图片位置 · {label}{cap}<br>'
            f'<span style="font-size:12px;">（公众号编辑器中用「图片」工具上传对应 PNG）</span></div>')


def img_tag_wrap(img, slot, caption=""):
    """按 img 表决定输出 <img> 还是占位卡。src 用相对文件名（与 html 同目录）。"""
    e = img.get(slot)
    if not e:
        return ""
    if e.get("url"):
        return img_tag(e["url"], e.get("alt", ""), caption)
    if e.get("file"):
        return img_tag(e["file"], e.get("alt", ""), caption)
    return img_placeholder(e.get("label", slot), caption)


def native_image(md_dir, alt, file):
    """原生 markdown 图片 ![](file.png) → <figure>，文件缺失则出占位卡。"""
    if os.path.exists(os.path.join(md_dir, file)):
        return img_tag(file, alt, alt)
    return img_placeholder(f"{alt}（缺 {file}）")


def cta_card(lines):
    inner = "<br>".join("" if ln == "" else inline(ln) for ln in lines)
    return (f'<div style="margin:28px 0;padding:22px;border-radius:12px;'
            f'background:linear-gradient(135deg,{VI}15,{CY}10);'
            f'border:1px solid {CY}40;color:#3b3b55;font-size:15px;line-height:1.95;">'
            f'{inner}</div>')


def signoff_card():
    return (f'<div style="margin:40px 0 26px;padding:26px 20px;text-align:center;'
            f'background:linear-gradient(135deg,#0B1026,#1E1B4B);border-radius:14px;">'
            f'<div style="font-size:22px;font-weight:800;color:{CY};letter-spacing:2px;">黯镜 AI</div>'
            f'<div style="margin-top:8px;font-size:13px;color:{MG};letter-spacing:1.5px;">'
            f'折射未来幻想</div>'
            f'<div style="margin-top:4px;font-size:12px;color:rgba(255,255,255,.45);'
            f'letter-spacing:1px;">futurefantasy.tech</div></div>')


# ───────────────────────── blocks → 文章 HTML ─────────────────────────
def render(blocks, img, md_dir):
    out = []
    lead_done = False
    sec_no = 0

    def section_image(slot, caption=""):
        chunk = img_tag_wrap(img, slot, caption)
        if chunk:
            out.append(chunk)

    for b in blocks:
        kind = b[0]

        if kind == "h":
            level, text = b[1], b[2]
            if level == 1:
                out.append(f'<h1 style="{S_H1}">{inline(text)}</h1>')
                out.append(f'<div style="{S_KICKER}">黯镜 AI · 深度解读</div>')
            else:
                m = re.match(r"^(\d+)(\s*)(.*)", text)
                numbered = bool(m)
                if m:
                    sec_no = int(m.group(1))
                    body = (f'<span style="color:{CY};">{m.group(1)}</span>'
                            f'{m.group(2)}{inline(m.group(3))}')
                else:
                    body = inline(text)
                tag = "h2" if level == 2 else "h3"
                style = S_H2 if level == 2 else S_H3
                out.append(f'<{tag} style="{style}">{body}</{tag}>')
                if level == 2 and numbered and 1 <= sec_no <= 5:
                    section_image(f"part{sec_no}", CAPTIONS.get(f"part{sec_no}", ""))
            continue

        if kind == "quote":
            lines = b[1]
            joined = "<br>".join("" if ln == "" else inline(ln) for ln in lines)
            blob = " ".join(lines)
            # 品牌收尾（在引用块里也能触发，如「黯镜 AI，折射未来幻想」）
            if "折射未来幻想" in blob and "黯镜" in blob:
                section_image("ending", "")
                out.append(signoff_card()); continue
            if any(k in blob for k in ("关注", "在看", "转发")) and \
                    ("黯镜" in blob or "futurefantasy" in blob):
                out.append(cta_card(lines)); continue
            if not lead_done:
                out.append(f'<blockquote style="{S_LEAD}">{joined}</blockquote>')
                lead_done = True
                section_image("cover", ""); continue
            out.append(f'<blockquote style="{S_QUOTE}">{joined}</blockquote>'); continue

        if kind == "hr":
            out.append(S_HR); continue

        if kind == "list":
            ltype, items = b[1], b[2]
            for i, it in enumerate(items):
                if ltype == "ul":
                    marker = f'<span style="color:{MG};">●</span>&nbsp;&nbsp;'
                else:
                    marker = f'<span style="color:{CY};font-weight:700;">{i+1}.</span>&nbsp;&nbsp;'
                out.append(f'<p style="{S_LI}">{marker}{inline(it)}</p>')
            out.append('<div style="height:8px;"></div>'); continue

        if kind == "p":
            stripped = b[1].strip()
            # 原生 markdown 图片 ![说明](文件.png) → 居中图 + 图注
            m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", stripped)
            if m:
                out.append(native_image(md_dir, m.group(1), m.group(2))); continue
            if re.match(r"^\*?(数据)?来源[:：]", stripped):
                out.append(f'<p style="{S_SRC}">{inline(stripped.strip("*"))}</p>'); continue
            if "折射未来幻想" in stripped and "黯镜" in stripped:
                section_image("ending", "")
                out.append(signoff_card()); continue
            out.append(f'<p style="{S_P}">{inline(b[1])}</p>'); continue

    return "\n".join(out)


# ───────────────────────── 图片表 ─────────────────────────
def build_img_map(md_dir, urls):
    files = {
        "cover": "wechat-cover.png",
        "part1": "wechat-part1.png", "part2": "wechat-part2.png",
        "part3": "wechat-part3.png", "part4": "wechat-part4.png",
        "part5": "wechat-part5.png",
        "ending": "wechat-ending.png",
    }
    labels = {"cover": "封面图", "part1": "Part1 配图", "part2": "Part2 配图",
              "part3": "Part3 配图", "part4": "Part4 配图", "part5": "Part5 配图",
              "ending": "结尾金句图"}
    img = {}
    for slot, fn in files.items():
        e = {"label": labels[slot], "alt": labels[slot]}
        if urls.get(slot):
            e["url"] = urls[slot]
        else:
            e["file"] = fn if os.path.exists(os.path.join(md_dir, fn)) else None
        img[slot] = e
    return img


# ───────────────────────── 主流程 ─────────────────────────
def find_default_md():
    cands = sorted(glob.glob("content/*/wechat.md"))
    if not cands:
        sys.exit("找不到 content/*/wechat.md，请显式传入 md 路径。")
    return cands[-1]


def main():
    ap = argparse.ArgumentParser(description="wechat.md → 可粘贴公众号的 inline-styled HTML")
    ap.add_argument("md", nargs="?", help="输入 wechat.md（默认最新的 content/*/wechat.md）")
    ap.add_argument("-o", "--out", help="输出 html 路径（默认 md 同目录 wechat.html）")
    ap.add_argument("--urls", help="图床 URL 映射 json：{\"cover\":\"https://...\",...}")
    args = ap.parse_args()

    md_path = os.path.abspath(args.md or find_default_md())
    md_dir = os.path.dirname(md_path)

    # 末尾品牌收尾图：固定复用共享品牌资产（覆盖任何旧的 per-article 图）。
    # 没有 per-article wechat-ending.png 也不影响——共享图会自动补上。
    ending_local = os.path.join(md_dir, "wechat-ending.png")
    if os.path.exists(BRAND_SIGNOFF):
        shutil.copy(BRAND_SIGNOFF, ending_local)

    md = open(md_path, encoding="utf-8").read()
    first = md.splitlines()[0].lstrip("#").strip()
    title = first or "文章"

    urls = json.load(open(args.urls, encoding="utf-8")) if args.urls else {}
    img = build_img_map(md_dir, urls)

    article = render(parse(md), img, md_dir)
    doc = f"""<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{html.escape(title)}</title>
<style>
  body{{background:#eef0f7;margin:0;padding:36px 12px;font-family:sans-serif;}}
  #page{{max-width:640px;margin:0 auto;background:#fff;border-radius:14px;
         box-shadow:0 6px 30px rgba(20,20,50,.08);overflow:hidden;}}
  .tip{{max-width:640px;margin:0 auto 14px;padding:10px 14px;background:#fff8e6;
        border:1px solid #f0d878;color:#8a6d00;border-radius:8px;font-size:13px;
        line-height:1.7;font-family:sans-serif;}}
  @media (max-width:640px){{ body{{padding:0;background:#fff;}} #page{{border-radius:0;}} }}
</style>
</head>
<body>
  <div class="tip">📋 预览模式｜发布流程：选中下方白色区域 → Ctrl+C → 公众号后台编辑器 Ctrl+V。
  图片见文中位置，在公众号「图片」工具里上传对应 PNG。</div>
  <div id="page">
    <section id="article" style="{S_CONTAINER}">
{article}
    </section>
  </div>
</body>
</html>
"""
    out_path = os.path.abspath(args.out or os.path.join(md_dir, "wechat.html"))
    open(out_path, "w", encoding="utf-8").write(doc)
    has_url = any(v.get("url") for v in img.values())
    print(f"✅ 已生成：{out_path}")
    print(f"   标题：{title}")
    print(f"   图片：{'图床 URL（可一次粘贴）' if has_url else '本地相对路径（预览用，发布时在公众号里上传 PNG）'}")
    print(f"   下一步：浏览器打开该文件 → 选中白色文章区 → 复制 → 粘贴进公众号后台。")


if __name__ == "__main__":
    main()
