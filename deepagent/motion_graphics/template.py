"""Motion-graphics composition builder (promoted from the backlash video template).

Lifted verbatim are the 12-component ``graphic`` renderer, the ``tweens`` seek-safe
GSAP recipe, the ``CSS``, and the per-platform ``SIZES``. New: ``build_composition``
takes an arbitrary scene list + audio manifest + output dir + platform + brand
palette (no hardcoded topic), and applies the palette to the CSS by color
substitution so the engine is brand-neutral."""
from __future__ import annotations

import html
import json
import math
import os
import shutil

from .icons import icon

RC = 45.0
C = 2 * math.pi * RC  # ring circumference

CSS_COMPONENT_KINDS = (
    "ring", "cd", "contrast", "bignum", "duo", "flow",
    "iconrow", "statpair", "quote", "spectrum", "curve", "card",
)

_DEFAULT_PALETTE = {
    "bg_start": "#0B1026", "bg_end": "#1E1B4B",
    "cyan": "#22D3EE", "magenta": "#F472B6", "purple": "#7C3AED",
}


def esc(s) -> str:
    return html.escape(str(s))


def acc_of(a: str) -> str:
    return f" {a}" if a else ""


# ── palette → CSS color substitution ──
def _rgb(h: str) -> str:
    h = h.lstrip("#")
    return f"{int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)}"


def _darken(h: str, factor: float = 0.45) -> str:
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#{:02x}{:02x}{:02x}".format(int(r * factor), int(g * factor), int(b * factor))


def _apply_palette(css: str, pal: dict) -> str:
    p = {**_DEFAULT_PALETTE, **(pal or {})}
    repl = {
        "#0B1026": p["bg_start"], "#1E1B4B": p["bg_end"],
        "#22D3EE": p["cyan"], "#F472B6": p["magenta"], "#7C3AED": p["purple"],
        "rgba(34,211,238": f"rgba({_rgb(p['cyan'])}",
        "rgba(244,114,182": f"rgba({_rgb(p['magenta'])}",
        "rgba(124,58,237": f"rgba({_rgb(p['purple'])}",
        "#0e7490": _darken(p["cyan"]), "#9d174d": _darken(p["magenta"]),
    }
    for a, b in repl.items():
        css = css.replace(a, b)
    return css


def graphic(i, kind, a, p, Sx, head=""):
    g = ""
    if kind in ("ring", "cd"):
        num = p["num"]
        unit = '<span class="pct">%</span>' if kind == "ring" else '<span class="unit">秒</span>'
        g = (f'<div class="ring" id="s{i}-rw"><svg class="ring-svg" viewBox="0 0 100 100">'
             f'<circle class="ring-bg" cx="50" cy="50" r="{RC:g}"/><circle class="ring-fg{acc_of(a)}" id="s{i}-ring" cx="50" cy="50" r="{RC:g}"/></svg>'
             f'<div class="ring-num{acc_of(a)}">{num}{unit}</div></div>')
    elif kind == "contrast":
        b1 = (f'<div class="bar-col"><div class="bar {p["c1"]}" id="s{i}-b1"></div><div class="bar-val">{p["v1"]}</div>'
              f'<div class="bar-lab">{esc(p["l1"])}</div></div>')
        b2 = (f'<div class="bar-col"><div class="bar {p["c2"]}" id="s{i}-b2"></div><div class="bar-val">{p["v2"]}</div>'
              f'<div class="bar-lab">{esc(p["l2"])}</div></div>')
        g = f'<div class="bars" id="s{i}-bars">{b1}{b2}</div>'
    elif kind == "bignum":
        g = (f'<div class="bn" id="s{i}-bnw"><svg class="bn-ring" viewBox="0 0 120 120">'
             f'<circle class="bn-bg" cx="60" cy="60" r="54"/><circle class="bn-fg{acc_of(a)}" id="s{i}-bnr" cx="60" cy="60" r="54"/></svg>'
             f'<div class="bn-num{acc_of(a)}" id="s{i}-bn">{p["num"]}<span class="bn-u">{p["unit"]}</span></div></div>')
    elif kind == "duo":
        li, ll = p["l"]
        ri, rl = p["r"]
        g = (f'<div class="duo"><div class="duo-card{acc_of(a)}" id="s{i}-dl">{icon(li, Sx["DICO"])}<div class="duo-l">{esc(ll)}</div></div>'
             f'<div class="duo-vs{acc_of(a)}" id="s{i}-vs">{p["vs"]}</div>'
             f'<div class="duo-card{acc_of(a)}" id="s{i}-dr">{icon(ri, Sx["DICO"])}<div class="duo-l">{esc(rl)}</div></div></div>')
    elif kind == "flow":
        nds = p["nodes"]
        parts = []
        for k, (ni, nl) in enumerate(nds):
            if k > 0:
                parts.append(f'<div class="fl-arrow{acc_of(a)}" id="s{i}-fa{k}">▶</div>')
            parts.append(f'<div class="fl-node{acc_of(a)}" id="s{i}-fn{k}">{icon(ni, Sx["FICO"])}<div class="fl-l">{esc(nl)}</div></div>')
        g = f'<div class="flow">{"".join(parts)}</div>'
    elif kind == "iconrow":
        icons = p if (p and isinstance(p, list)) else p["icons"]
        items = [f'<div class="ic{acc_of(c2)}" id="s{i}-ic{k}">{icon(ic, Sx["IICO"])}<div class="ic-l">{esc(lb)}</div></div>'
                 for k, (ic, lb, c2) in enumerate(icons)]
        g = f'<div class="icrow">{"".join(items)}</div>'
    elif kind == "statpair":
        cards = []
        for k, (di, dn, dl, dc) in enumerate(p["items"]):
            cards.append(f'<div class="sp-card{acc_of(dc)}" id="s{i}-sp{k}"><div class="sp-d">{icon(di, Sx["SPICO"])}</div>'
                         f'<div class="sp-n">{dn}</div><div class="sp-l">{esc(dl)}</div></div>')
        g = f'<div class="sp">{"".join(cards)}</div>'
    elif kind == "quote":
        g = f'<div class="qt{acc_of(a)}" id="s{i}-qt"><div class="qt-m">“</div><div class="qt-t" id="s{i}-qtt">{esc(p["text"])}</div></div>'
    elif kind == "spectrum":
        g = (f'<div class="spec"><div class="spec-lane"><div class="spec-line{acc_of(a)}" id="s{i}-sl"></div>'
             f'<div class="spec-dot l{acc_of(a)}" id="s{i}-sdl"></div><div class="spec-dot r{acc_of(a)}" id="s{i}-sdr"></div></div>'
             f'<div class="spec-labs"><span>{esc(p["l"])}</span><span>{esc(p["r"])}</span></div></div>')
    elif kind == "curve":
        d = "M20 40 C 90 55,120 70,160 100 S 250 145,285 150" if p["ck"] == "down" \
            else "M20 150 C 60 40,90 30,120 60 S 180 150,220 120 S 270 80,285 70"
        g = (f'<svg class="cv" viewBox="0 0 305 170" id="s{i}-cv">'
             f'<path class="cv-axis" d="M20 10 V155 H295"/>'
             f'<path class="cv-line{acc_of(a)}" id="s{i}-cvl" pathLength="1" d="{d}"/></svg>')
    elif kind == "card":
        g = (f'<div class="ccard{acc_of(a)}" id="s{i}-cc">{icon(p["icon"], Sx["CCICO"])}'
             f'<div class="cc-head" id="s{i}-cch">{esc(head)}</div></div>')
    return g


def headsub(i, kind, head, sub):
    h = f'<div class="head{acc_of("cy")}" id="s{i}-head">{esc(head)}</div>' if head and kind != "card" else ""
    s = f'<div class="sub" id="s{i}-sub">{esc(sub)}</div>' if sub else ""
    return h, s


def fore(i, kind, a, head, sub, p, N, Sx):
    n = f"{i + 1:02d}"
    badge = f'<div class="num" id="s{i}-num">{n}<span class="num-tot">/{N}</span></div>'
    motif = ('<div class="motif"><svg viewBox="0 0 100 100">'
             '<polygon points="50,8 88,78 12,78" fill="none" stroke="#22D3EE" stroke-width="3" opacity=".5"/>'
             '<line x1="50" y1="8" x2="50" y2="78" stroke="#F472B6" stroke-width="2" opacity=".4"/>'
             '<line x1="50" y1="40" x2="20" y2="62" stroke="#22D3EE" stroke-width="2" opacity=".35"/>'
             '<line x1="50" y1="40" x2="80" y2="62" stroke="#F472B6" stroke-width="2" opacity=".35"/></svg></div>')
    g = graphic(i, kind, a, p, Sx, head)
    if kind in ("card", "quote"):
        s = f'<div class="sub" id="s{i}-sub">{esc(sub)}</div>' if sub else ""
        body = g + s
    else:
        h, s = headsub(i, kind, head, sub)
        body = h + g + s
    return badge + motif + f'<div class="stage">{body}</div>'


def tweens(i, kind, S, p):
    t = [f'g.from("#s{i}-num",{{opacity:0,x:-22,duration:.4,ease:"power2.out",immediateRender:false}},{S:.3f});']
    if kind in ("ring", "cd"):
        off = 0.0 if kind == "cd" else round(C * (1 - p["num"] / 100), 1)
        t += [f'g.from("#s{i}-rw",{{scale:.62,opacity:0,duration:.6,ease:"back.out(1.4)",immediateRender:false}},{S + .05:.3f});',
              f'g.fromTo("#s{i}-ring",{{strokeDashoffset:{C:.1f}}},{{strokeDashoffset:{off},duration:.9,ease:"power2.out",immediateRender:false}},{S + .15:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .45:.3f});']
    elif kind == "contrast":
        t += [f'g.from("#s{i}-head",{{opacity:0,y:18,duration:.4,immediateRender:false}},{S:.3f});',
              f'g.fromTo("#s{i}-b1",{{scaleY:0}},{{scaleY:{p["s1"]},duration:.7,ease:"power3.out",immediateRender:false}},{S + .15:.3f});',
              f'g.fromTo("#s{i}-b2",{{scaleY:0}},{{scaleY:{p["s2"]},duration:.7,ease:"power3.out",immediateRender:false}},{S + .3:.3f});',
              f'g.from("#s{i}-bars .bar-val,#s{i}-bars .bar-lab",{{opacity:0,y:8,stagger:.08,duration:.4,immediateRender:false}},{S + .55:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .75:.3f});']
    elif kind == "bignum":
        t += [f'g.from("#s{i}-bnw",{{scale:.6,opacity:0,duration:.6,ease:"back.out(1.3)",immediateRender:false}},{S + .05:.3f});',
              f'g.fromTo("#s{i}-bnr",{{strokeDashoffset:339.3}},{{strokeDashoffset:0,duration:1.0,ease:"power2.out",immediateRender:false}},{S + .1:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .5:.3f});']
    elif kind == "duo":
        t += [f'g.from("#s{i}-head",{{opacity:0,y:18,duration:.4,immediateRender:false}},{S:.3f});',
              f'g.from("#s{i}-dl",{{opacity:0,x:-70,duration:.55,ease:"power3.out",immediateRender:false}},{S + .1:.3f});',
              f'g.from("#s{i}-dr",{{opacity:0,x:70,duration:.55,ease:"power3.out",immediateRender:false}},{S + .1:.3f});',
              f'g.from("#s{i}-vs",{{scale:0,opacity:0,duration:.5,ease:"back.out(2)",immediateRender:false}},{S + .45:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .55:.3f});']
    elif kind == "flow":
        nds = p["nodes"]
        for k in range(len(nds)):
            t.append(f'g.from("#s{i}-fn{k}",{{opacity:0,scale:.5,duration:.5,ease:"back.out(1.5)",immediateRender:false}},{S + .1 + k * .25:.3f});')
            if k > 0:
                t.append(f'g.from("#s{i}-fa{k}",{{opacity:0,x:-14,duration:.35,immediateRender:false}},{S + .1 + k * .25 + .12:.3f});')
        t += [f'g.from("#s{i}-head",{{opacity:0,y:18,duration:.4,immediateRender:false}},{S:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .1 + len(nds) * .25:.3f});']
    elif kind == "iconrow":
        icons = p if isinstance(p, list) else p["icons"]
        for k in range(len(icons)):
            t.append(f'g.from("#s{i}-ic{k}",{{opacity:0,y:30,scale:.6,duration:.45,ease:"back.out(1.5)",immediateRender:false}},{S + .1 + k * .14:.3f});')
        t += [f'g.from("#s{i}-head",{{opacity:0,y:18,duration:.4,immediateRender:false}},{S:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .1 + len(icons) * .14:.3f});']
    elif kind == "statpair":
        for k in range(len(p["items"])):
            t.append(f'g.from("#s{i}-sp{k}",{{opacity:0,y:30,scale:.6,duration:.5,ease:"back.out(1.5)",immediateRender:false}},{S + .1 + k * .18:.3f});')
        t.append(f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .6:.3f});')
    elif kind == "quote":
        t += [f'g.from("#s{i}-qt",{{opacity:0,scale:.85,duration:.6,ease:"power3.out",immediateRender:false}},{S + .1:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .5:.3f});']
    elif kind == "spectrum":
        t += [f'g.from("#s{i}-head",{{opacity:0,y:18,duration:.4,immediateRender:false}},{S:.3f});',
              f'g.from("#s{i}-sl",{{scaleX:0,duration:.7,ease:"power2.out",immediateRender:false}},{S + .15:.3f});',
              f'g.from("#s{i}-sdl",{{opacity:0,scale:0,duration:.4,ease:"back.out(2)",immediateRender:false}},{S + .4:.3f});',
              f'g.from("#s{i}-sdr",{{opacity:0,scale:0,duration:.4,ease:"back.out(2)",immediateRender:false}},{S + .55:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .7:.3f});']
    elif kind == "curve":
        t += [f'g.from("#s{i}-head",{{opacity:0,y:18,duration:.4,immediateRender:false}},{S:.3f});',
              f'g.from("#s{i}-cv",{{opacity:0,scale:.85,duration:.5,immediateRender:false}},{S + .1:.3f});',
              f'g.fromTo("#s{i}-cvl",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.0,ease:"power2.out",immediateRender:false}},{S + .3:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .7:.3f});']
    elif kind == "card":
        t += [f'g.from("#s{i}-cc",{{opacity:0,scale:.7,duration:.55,ease:"back.out(1.4)",immediateRender:false}},{S + .05:.3f});',
              f'g.from("#s{i}-sub",{{opacity:0,y:16,duration:.45,immediateRender:false}},{S + .4:.3f});']
    return "\n      ".join(t)


CSS = r"""
*{margin:0;padding:0;box-sizing:border-box;}
html,body{margin:0;width:__W__px;height:__H__px;overflow:hidden;background:#0B1026;font-family:sans-serif;}
.clip{position:absolute;inset:0;}
.scene-bg{position:absolute;inset:0;background:linear-gradient(160deg,#0B1026 0%,#1E1B4B 50%,#0B1026 100%);}
.scene-bg::after{content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 18% 28%,rgba(34,211,238,.07) 0%,transparent 45%),radial-gradient(circle at 82% 72%,rgba(244,114,182,.07) 0%,transparent 45%),repeating-linear-gradient(0deg,transparent,transparent 59px,rgba(255,255,255,.022) 60px),repeating-linear-gradient(90deg,transparent,transparent 59px,rgba(255,255,255,.022) 60px);}
.motif{position:absolute;top:4.5%;right:5%;width:__MOTIF__px;height:__MOTIF__px;opacity:.55;}
.num{position:absolute;top:4.5%;left:5%;color:rgba(255,255,255,.32);font-weight:800;font-size:__NUM__px;letter-spacing:1px;}
.num-tot{font-size:.5em;opacity:.7;}
.stage{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:__GAP__px;padding:9% 8%;}
.head{color:#fff;font-weight:800;font-size:__HEAD__px;text-align:center;line-height:1.25;text-shadow:0 0 24px rgba(34,211,238,.3);}
.head.cy{color:#22D3EE;}.head.mg{color:#F472B6;}.head.dim{color:rgba(255,255,255,.7);}
.sub{color:rgba(255,255,255,.66);font-size:__SUB__px;font-weight:500;text-align:center;line-height:1.5;text-shadow:0 2px 14px rgba(0,0,0,.6);}
.ic{display:block;}
.cy{color:#22D3EE;}.mg{color:#F472B6;}.dim{color:rgba(255,255,255,.6);}
.ring{position:relative;width:__RING__px;height:__RING__px;}
.ring-svg{width:100%;height:100%;}
.ring-bg{fill:none;stroke:rgba(255,255,255,.1);stroke-width:6;}
.ring-fg{fill:none;stroke-width:6;stroke-linecap:round;stroke-dasharray:__C__;transform:rotate(-90deg);transform-origin:center;}
.ring-fg.cy{stroke:#22D3EE;filter:drop-shadow(0 0 6px rgba(34,211,238,.7));}.ring-fg.mg{stroke:#F472B6;filter:drop-shadow(0 0 6px rgba(244,114,182,.7));}
.ring-num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:__RINGNUM__px;color:#fff;text-shadow:0 0 30px rgba(34,211,238,.5);}
.ring-num.mg{color:#F472B6;}.pct,.unit{font-size:.42em;margin-left:.06em;opacity:.85;}
.bars{display:flex;gap:__BARGAP__px;align-items:flex-end;height:__BARH__px;}
.bar-col{display:flex;flex-direction:column;align-items:center;gap:12px;}
.bar{width:__BARW__px;height:__BARH__px;border-radius:12px 12px 0 0;transform-origin:bottom;background:linear-gradient(180deg,#22D3EE,#0e7490);box-shadow:0 0 24px rgba(34,211,238,.35);}
.bar.mg{background:linear-gradient(180deg,#F472B6,#9d174d);box-shadow:0 0 24px rgba(244,114,182,.35);}
.bar-val{font-weight:900;font-size:__BARVAL__px;color:#fff;}
.bar-lab{font-size:__BARLAB__px;color:rgba(255,255,255,.62);font-weight:600;}
.bn{position:relative;width:__BNRING__px;height:__BNRING__px;display:flex;align-items:center;justify-content:center;}
.bn-ring{position:absolute;inset:0;width:100%;height:100%;}
.bn-bg{fill:none;stroke:rgba(255,255,255,.08);stroke-width:2;}
.bn-fg{fill:none;stroke-width:2.5;stroke-linecap:round;stroke-dasharray:339.3;transform:rotate(-90deg);transform-origin:center;}
.bn-fg.cy{stroke:#22D3EE;}.bn-fg.mg{stroke:#F472B6;}
.bn-num{position:relative;font-weight:900;font-size:__BN__px;color:#fff;text-shadow:0 0 40px rgba(244,114,182,.45);}
.bn-num.mg{color:#F472B6;}.bn-u{font-size:.42em;margin-left:.08em;opacity:.85;}
.duo{display:flex;align-items:center;gap:__DUOGAP__px;}
.duo-card{width:__DUOCARD__px;padding:__DUOPAD__px;border-radius:18px;background:rgba(255,255,255,.04);border:1.5px solid rgba(34,211,238,.3);display:flex;flex-direction:column;align-items:center;gap:14px;box-shadow:0 0 30px rgba(34,211,238,.12);}
.duo-card.mg{border-color:rgba(244,114,182,.35);box-shadow:0 0 30px rgba(244,114,182,.12);}
.duo-l{font-size:__DUOL__px;font-weight:700;color:#fff;}
.duo-vs{font-size:__DUOVS__px;font-weight:900;}
.flow{display:flex;align-items:center;gap:10px;}
.fl-node{width:__FNODE__px;padding:__FNODEPAD__px;border-radius:16px;background:rgba(255,255,255,.04);border:1.5px solid rgba(34,211,238,.3);display:flex;flex-direction:column;align-items:center;gap:12px;}
.fl-l{font-size:__FLAB__px;font-weight:700;color:#fff;}
.fl-arrow{font-size:__FLARROW__px;}
.icrow{display:flex;gap:__ICGAP__px;}
.ic{width:__ICARD__px;padding:__ICPAD__px;border-radius:50%;background:rgba(255,255,255,.04);border:1.5px solid rgba(244,114,182,.32);display:flex;flex-direction:column;align-items:center;gap:14px;}
.ic.cy{border-color:rgba(34,211,238,.32);}
.ic-l{font-size:__ICL__px;font-weight:700;color:#fff;}
.sp{display:flex;gap:__SPGAP__px;}
.sp-card{width:__SPW__px;padding:__SPPAD__px;border-radius:18px;background:rgba(255,255,255,.04);border:1.5px solid rgba(244,114,182,.32);display:flex;flex-direction:column;align-items:center;gap:10px;}
.sp-d{opacity:.85;}.sp-n{font-size:__SPN__px;font-weight:900;color:#fff;}.sp-l{font-size:__SPL__px;color:rgba(255,255,255,.65);font-weight:600;}
.qt{max-width:__QTW__px;padding:__QTPAD__px;border-radius:20px;background:rgba(124,58,237,.1);border:1.5px solid rgba(124,58,237,.4);position:relative;text-align:center;}
.qt-m{font-size:__QTM__px;line-height:.6;color:#7C3AED;font-weight:900;height:.4em;}
.qt-t{font-size:__QT__px;font-weight:800;color:#fff;line-height:1.4;text-shadow:0 2px 16px rgba(0,0,0,.5);}
.spec{width:__SPECW__px;display:flex;flex-direction:column;gap:22px;}
.spec-lane{position:relative;height:__SPECH__px;display:flex;align-items:center;}
.spec-line{position:absolute;inset:0;height:__SPECH__px;border-radius:9px;background:linear-gradient(90deg,#22D3EE,#7C3AED,#F472B6);transform-origin:left;box-shadow:0 0 20px rgba(124,58,237,.4);}
.spec-dot{position:absolute;top:50%;width:__SPECDOT__px;height:__SPECDOT__px;border-radius:50%;transform:translate(-50%,-50%);box-shadow:0 0 18px currentColor;}
.spec-dot.l{left:0;background:#22D3EE;}.spec-dot.r{left:100%;background:#F472B6;}
.spec-labs{display:flex;justify-content:space-between;font-size:__SPECLAB__px;font-weight:800;color:#fff;}
.cv{width:__CVW__px;height:__CVH__px;}
.cv-axis{fill:none;stroke:rgba(255,255,255,.18);stroke-width:2;}
.cv-line{fill:none;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;filter:drop-shadow(0 0 6px currentColor);}
.cv-line.cy{stroke:#22D3EE;}.cv-line.mg{stroke:#F472B6;}.cv-line.dim{stroke:rgba(255,255,255,.6);}
.ccard{width:__CCARDW__px;padding:__CCPAD__px;border-radius:26px;background:rgba(255,255,255,.04);border:1.5px solid rgba(34,211,238,.3);display:flex;flex-direction:column;align-items:center;gap:__CCGAP__px;box-shadow:0 0 50px rgba(34,211,238,.12);}
.ccard.mg{border-color:rgba(244,114,182,.35);box-shadow:0 0 50px rgba(244,114,182,.12);}
.ccard.dim{border-color:rgba(255,255,255,.18);}
.cc-head{font-size:__CCHEAD__px;font-weight:900;color:#fff;text-align:center;line-height:1.25;text-shadow:0 0 26px rgba(34,211,238,.3);}
"""

SIZES = {
    "bili": dict(W=1920, H=1080, MOTIF=70, NUM=34, GAP=28, HEAD=52, SUB=44, RING=380, RINGNUM=120,
                 BARH=360, BARW=130, BARGAP=100, BARVAL=54, BARLAB=36, BNRING=470, BN=200,
                 DUOCARD=320, DUOPAD=46, DUOL=50, DUOVS=96, DUOGAP=10, FNODE=250, FNODEPAD=40,
                 FLAB=46, FLARROW=70, ICARD=230, ICPAD=44, ICGAP=34, ICL=44, SPW=400, SPPAD=52,
                 SPGAP=50, SPN=140, SPL=46, SPICO=110, QTW=1000, QTPAD=64, QT=76, QTM=150,
                 SPECW=820, SPECH=20, SPECDOT=46, SPECLAB=56, CVW=900, CVH=440,
                 CCARDW=720, CCPAD=70, CCGAP=34, CCHEAD=92, CCICO=240, DICO=150, FICO=170, IICO=160),
    "douyin": dict(W=1080, H=1920, MOTIF=56, NUM=30, GAP=24, HEAD=48, SUB=40, RING=340, RINGNUM=108,
                   BARH=300, BARW=110, BARGAP=72, BARVAL=46, BARLAB=32, BNRING=410, BN=168,
                   DUOCARD=270, DUOPAD=40, DUOL=44, DUOVS=80, DUOGAP=8, FNODE=210, FNODEPAD=34,
                   FLAB=40, FLARROW=58, ICARD=195, ICPAD=36, ICGAP=24, ICL=38, SPW=350, SPPAD=44,
                   SPGAP=40, SPN=120, SPL=40, SPICO=92, QTW=820, QTPAD=54, QT=68, QTM=130,
                   SPECW=700, SPECH=18, SPECDOT=40, SPECLAB=48, CVW=780, CVH=400,
                   CCARDW=620, CCPAD=58, CCGAP=28, CCHEAD=78, CCICO=210, DICO=130, FICO=148, IICO=140),
}
for _k in SIZES:
    SIZES[_k]["C"] = f"{C:.1f}"


def _scaffold(name: str, out_dir: str) -> None:
    for fn, c in [
        ("package.json", json.dumps({"name": name, "private": True, "type": "module",
                                     "scripts": {"render": "npx --yes hyperframes@0.6.118 render"}}, indent=2)),
        ("meta.json", json.dumps({"id": name, "name": name, "createdAt": "2026-06-28T00:00:00.000Z"})),
        ("hyperframes.json", json.dumps({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
                                         "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
                                         "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}})),
    ]:
        with open(os.path.join(out_dir, fn), "w") as f:
            f.write(c)


def build_composition(
    name: str,
    scenes,
    audio_manifest_path: str,
    out_project_dir: str,
    platform: str = "douyin",
    palette: dict | None = None,
) -> str:
    """Write a complete HyperFrames project to ``out_project_dir``.

    scenes: list of (kind, accent, head, sub, params) — one per audio clip, in order.
    audio_manifest_path: manifest.json produced by run_tts (gives per-scene durations + audio files).
    platform: "bili" (16:9) or "douyin" (9:16).
    palette: {bg_start, bg_end, cyan, magenta, purple}; defaults to the brand-default deep-space theme.
    """
    Sx = SIZES[platform]
    w, h = Sx["W"], Sx["H"]
    with open(audio_manifest_path) as f:
        m = json.load(f)
    assert len(scenes) == len(m), f"{name}: {len(scenes)} scenes vs {len(m)} audio clips"

    cum = 0.0
    tm = []
    for it in m:
        d = float(it["duration"])
        tm.append((round(cum, 3), d))
        cum += d
    T = round(cum, 3)
    N = len(scenes)

    clips = []
    for i, (S, d) in enumerate(tm):
        kind, a, head, sub, p = scenes[i]
        clips.append(
            f'      <div id="scene{i+1}" class="clip" data-start="{S:.3f}" '
            f'data-duration="{d - 0.002:.3f}" data-track-index="1">'
            f'{fore(i, kind, a, head, sub, p, N, Sx)}</div>'
        )
    sb = "\n".join(clips)
    ah = "\n".join(
        f'      <audio id="aud-scene{i+1}" class="clip" data-start="{tm[i][0]:.3f}" '
        f'data-duration="{tm[i][1] - 0.002:.3f}" data-track-index="2" src="audio/scene{i+1}.mp3"></audio>'
        for i in range(N)
    )
    tw = "\n      ".join(tweens(i, scenes[i][0], tm[i][0], scenes[i][4]) for i in range(N))

    css = _apply_palette(CSS, palette or {})
    for k, v in Sx.items():
        css = css.replace(f"__{k}__", str(v))

    doc = f"""<!doctype html><html lang="zh"><head><meta charset="UTF-8"/><meta name="viewport" content="width={w}, height={h}"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{css}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="{w}" data-height="{h}">
{sb}
{ah}
<script>window.__timelines=window.__timelines||{{}};const g=gsap.timeline({{paused:true}});
      {tw}
window.__timelines["main"]=g;</script></div></body></html>"""

    os.makedirs(os.path.join(out_project_dir, "audio"), exist_ok=True)
    for it in m:
        shutil.copy(it["file"], os.path.join(out_project_dir, "audio", f"{it['scene']}.mp3"))
    with open(os.path.join(out_project_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    _scaffold(name, out_project_dir)
    return out_project_dir
