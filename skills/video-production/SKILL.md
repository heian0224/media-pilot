---
name: video-production
description: "Turn finished scripts/copy into videos using HyperFrames (open-source local HTML→MP4 framework — NOT HeyGen). Use after platform-writing has produced a Douyin/Xiaohongshu/Bilibili script, or when the user asks for a video from text. Chinese narration is generated with MiniMax TTS (fluent Mandarin) — never Kokoro. Routes to the HyperFrames workflow skills (faceless-explainer for short口播, general-video for long-form). No HeyGen API key needed."
---

# Video Production (HyperFrames + MiniMax)

Convert finished scripts into actual MP4 videos using **HyperFrames** — an open-source framework that renders HTML/CSS/media into deterministic MP4s, fully local. **HyperFrames is NOT HeyGen** (despite living in the `heygen-com` GitHub org): it needs no API key, only Node 22+ and ffmpeg.

**Chinese narration uses MiniMax TTS** (`speech-2.8-hd`) — fluent Mandarin. Do NOT use HyperFrames' bundled Kokoro for Chinese (it needs espeak-ng and sounds robotic).

## When to Use

- After `platform-writing` produces a 抖音/小红书/B站 script that needs video output
- User asks: "把这个文案做成视频" / "生成口播视频" / "make a video from text"
- Full pipeline reaches the video stage

## Prerequisites

- **Node.js 22+** and **ffmpeg** (both required by HyperFrames).
- **HyperFrames skills installed** (one-time): `npx skills add heygen-com/hyperframes` — installs the skill family to `.agents/skills/`. Then `npx hyperframes doctor` (downloads bundled Chrome for rendering; first run is network-heavy).
- **`MINIMAX_API_KEY` env var** for Chinese narration. Get a key at the MiniMax open platform (~10 RMB top-up lasts many videos).

## Pipeline

```
script (from platform-writing)
  → split into scenes (one narration segment per scene)
  → MiniMax TTS per scene   →  audio/sceneN.mp3 + manifest.json (durations)
  → HyperFrames composition (index.html): scenes timed by audio durations
  → lint + inspect
  → render  →  MP4 (video + narration)
```

## Routing — which HyperFrames workflow

The HyperFrames skill family (`.agents/skills/`) covers different video types; route via `hyperframes-read-first`. For this plugin's content:

| Need | Workflow |
|------|----------|
| 抖音/小红书 short口播 explainer (≤~3 min, concept, no product) | `faceless-explainer` |
| B站 long-form / deep-dive (>~3 min) | `general-video` |
| Captions/subtitles on existing footage | `embedded-captions` |

The workflow skills default to Kokoro TTS — **override the audio step with MiniMax** for Chinese (below).

## MiniMax narration (THE voice method for Chinese)

Use the bundled **`scripts/minimax_tts.sh`** (parameterized; reusable per topic):

```bash
# scenes.txt: one narration segment per line (one line = one scene)
bash plugins/media-pilot/skills/video-production/scripts/minimax_tts.sh \
  --out content/<YYYY-MM-DD-topic-slug>/audio \
  --scenes content/<YYYY-MM-DD-topic-slug>/scenes.txt \
  --voice male-qn-qingse --speed 1.3
# → audio/scene1.mp3 … sceneN.mp3 + audio/manifest.json
```

- **Model/voice**: `speech-2.8-hd`, default voice `male-qn-qingse` (Mandarin). Other `z*` voices available.
- **Endpoint**: `POST https://api.minimaxi.com/v1/t2a_v2`, `Authorization: Bearer $MINIMAX_API_KEY`. Response `data.audio` is hex-encoded mp3 → decode to file.
- **Network — critical**: reach MiniMax **direct, with `--http1.1`**, and `unset` all `*proxy*` env vars first. Routing through a proxy causes TLS errors (connection reset / HTTP2 framing / SSL_ERROR_SYSCALL). From a domestic CN IP, direct works fine.
- **Wiring into the composition**: each scene's narration is a timed `<audio class="clip" data-start data-duration data-track-index src="sceneN.mp3">`. Scene N's `data-start` = sum of previous scenes' durations (read from `manifest.json`).

## Process

### 1. Confirm source + target
- Source script (`douyin-script.md` / `xiaohongshu.md` / `bilibili.md`)
- Aspect: **9:16 vertical** (抖音/小红书, 1080×1920) or **16:9** (B站/公众号, 1920×1080)
- MiniMax voice id (default `male-qn-qingse`)

### 2. Generate narration
Split the script into narration segments (one per scene), write to `scenes.txt` (one per line), run `minimax_tts.sh` → `audio/sceneN.mp3` + `manifest.json`.

### 3. Build the HyperFrames composition
Route to `faceless-explainer` (short) or `general-video` (long); or author directly per `hyperframes-core`. Each scene: the timed narration audio + an on-screen visual (large key phrase, minimal graphics). Vertical = 1080×1920.

### 4. Lint, inspect, render
```bash
npx hyperframes lint
npx hyperframes inspect
npx hyperframes render --output content/<topic>/douyin.mp4
```
Name the final MP4 per platform: `douyin.mp4` / `xiaohongshu.mp4` / `bilibili.mp4`, inside the topic folder.

## Quality checks

- [ ] Narration audio plays and matches each scene's visual
- [ ] Correct aspect ratio (9:16 for 抖音/小红书)
- [ ] Duration fits the platform norm (抖音 ≤90s, B站 5-15min)
- [ ] First 3s has a visual hook
- [ ] No silent gaps; Chinese narration clear and natural
- [ ] On-screen text readable at phone resolution (vertical)

## Notes / gotchas

- **HyperFrames ≠ HeyGen.** No HeyGen key, no avatar API. Local HTML→MP4.
- **Voice = MiniMax.** Not Kokoro (robotic Chinese), not HeyGen.
- **Chrome download** (first `doctor`/`render`) is ~100MB+ and network-heavy; the Bash call may need `dangerouslyDisableSandbox: true`.
- **MiniMax + proxy = TLS errors.** Always direct + `--http1.1`; unset proxy env vars.
- **Deterministic render only**: no `Date.now()` / `Math.random()` / network inside the composition HTML.
- Rendering long videos (5+ min) needs `--timeout` increased.

## Anti-Patterns

- Don't assume HyperFrames needs a HeyGen key — it doesn't.
- Don't use Kokoro for Chinese narration — use **MiniMax**.
- Don't route MiniMax through a proxy (TLS breaks) — direct + `--http1.1`.
- Don't render at the wrong aspect ratio — confirm 9:16 vs 16:9 before rendering (re-rendering is expensive).
