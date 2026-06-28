# Media-Pilot 🚀

> Autonomous self-media content engine for Claude Code — discover trending topics, write platform-native copy, and produce narrated videos. Built for the Chinese content ecosystem (公众号 / 小红书 / 抖音 / B站).

**[English](./README.md) · [中文](./README.zh-CN.md)**

[Features](#-features) · [Setup](#-setup) · [Usage](#-usage-examples) · [Structure](#-structure)

Media-Pilot turns a topic — or just *"find me something worth writing about"* — into ready-to-publish content across **WeChat (公众号)**, **Xiaohongshu (小红书)**, **Douyin (抖音)**, and **Bilibili (B站)**, plus narrated short videos with fluent Mandarin voiceover.

## ✨ Features

- **🔬 Discovery** — Pulls real trending signals from Chinese platforms (微博 / 抖音 / 百度 / 知乎 / B站 / 36氪 / 虎嗅) **and** international tech media (Hacker News, Reddit, GitHub Trending, dev.to, arXiv, Twitter/X, AI lab blogs from OpenAI / Anthropic / DeepMind / Meta / Mistral). For tech/AI topics it surfaces trends **1–4 weeks before** they reach Chinese platforms.
- **🎯 Strategy** — Picks content angles and maps each one to the right platforms.
- **✍️ Platform writing** — Drafts native copy in each platform's distinct voice: long-form WeChat articles, emoji-heavy Xiaohongshu posts, hook-driven Douyin scripts, deep Bilibili content. Emits **platform-specific** image-prompt docs (`wechat-images.md`, `xiaohongshu-images.md`) so you can generate visuals in your own tool.
- **🎬 Video** — Turns scripts into narrated MP4s with **HyperFrames** (local HTML→MP4 renderer) + **MiniMax TTS** (fluent Mandarin). No HeyGen, no avatar API, no per-minute billing.

## 🧠 How it works

Media-Pilot uses the [superpowers](https://github.com/obra/superpowers) proactive-skill pattern: a `using-media-pilot` meta-skill auto-activates whenever you're doing content work (injected at session start via a hook), then routes to the right stage skill.

```
Discovery → Strategy → Writing → Video
```

Run the full pipeline, or any single stage.

## 🤖 Two ways to run

Media-Pilot is **both** a Claude Code plugin **and** a standalone autonomous agent (the `deepagent` Python package, built on [LangChain `deepagents`](https://docs.langchain.com/oss/python/deepagents/overview)). Same brand, same prompts, same tools — two front-ends:

| | Claude Code plugin | Standalone `deepagent` |
|---|---|---|
| Runs in | the Claude Code REPL (interactive) | a plain Python process / cron |
| Trigger | you chat with Claude | `python -m deepagent run --topic "..."` / `--auto` / `schedule --cron` |
| Best for | hands-on, iterate per stage | **unattended / scheduled** daily content |

### Standalone agent — quick start

```bash
pip install -e ./plugins/media-pilot            # installs the `deepagent` package
python -m deepagent run --topic "GLM-4.6 开放智能体"   # fixed topic → full pipeline (+ video)
python -m deepagent run --auto                          # autonomously pick a trending topic
python -m deepagent run --auto --dry-run                # just pick + log, skip the pipeline
python -m deepagent schedule --cron "7 9 * * *"         # print a crontab line (--install to add)
```

**Configure** (any of): an OpenAI-compatible LLM key + base URL (e.g. 智谱 GLM `https://open.bigmodel.cn/api/paas/v4`, model `glm-4.6`; works with DeepSeek / Moonshot / OpenAI too), `MINIMAX_API_KEY` (Mandarin narration), `GPT_IMAGE_API_KEY`+`GPT_IMAGE_ENDPOINT` (cover/section images), `TAVILY_API_KEY` (trend search). Put them in `.claude/settings.local.json` `env`, or a `.env`, or the real env. For image-text verification add a vision model (`LLM_VISION_MODEL=glm-4v-flash`).

**Brand:** the repo is **brand-neutral** — copy [`brand.example.md`](./brand.example.md) to your workspace root as `brand.md` and fill it in; the agent reads it at runtime and applies your name/slogan/site/palette to every output.

**Architecture:** an orchestrator deepagent + 4 specialized subagents (discovery / strategy / writing / video), context-isolated, passing artifacts by file path. See [`deepagent/`](./deepagent/) — `agent/` (wiring), `prompts/` (stage prompts, shared with the plugin), `tools/`, `motion_graphics/` (the HyperFrames composition engine), `scheduler/` (auto topic-pick + guardrails + cron).

## 📦 Requirements

- **Claude Code** — this is a Claude Code plugin (not a standalone app)
- **Node.js 22+** and **ffmpeg** — for HyperFrames video rendering
- A **web search tool** for discovery — [Tavily MCP](https://tavily.com) recommended (built-in WebSearch/WebFetch also work)
- **MiniMax API key** — for Chinese video narration (see Setup)

## 🔧 Setup

1. **Get a media-workspace.** Media-Pilot is designed to live under `plugins/media-pilot/` in a workspace that also holds a sibling `content/` folder for output (see [Structure](#-structure)). Clone this repo, or create the layout from the tree below.

2. **Add the plugin in Claude Code** — either `/plugin` inside Claude Code, or launch with:
   ```bash
   claude --plugin-dir ./plugins/media-pilot
   ```

3. **Install HyperFrames** (the video engine):
   ```bash
   npx skills add heygen-com/hyperframes
   npx hyperframes doctor   # one-time: downloads bundled Chrome for rendering
   ```

4. **Set your MiniMax key** (get one at the MiniMax open platform — ~¥10 top-up lasts many videos):
   ```jsonc
   // .claude/settings.local.json  (local-only, won't be committed)
   { "env": { "MINIMAX_API_KEY": "your-key-here" } }
   ```

5. **(Recommended) Add Tavily MCP** for trend discovery.

> ⚠️ **HyperFrames ≠ HeyGen.** Despite living under the `heygen-com` GitHub org, HyperFrames is an **open-source local HTML→MP4 framework** — no HeyGen account, no API key, no avatar service.
>
> ⚠️ **MiniMax network:** the bundled TTS script reaches MiniMax **direct, with `--http1.1`** and unsets all proxy env vars. Routing through a proxy causes TLS errors (connection reset / HTTP2 framing / SSL handshake failures). From a domestic CN IP, direct works fine.

## 🎬 Usage examples

**Full automated pipeline:**
```
帮我围绕 "Claude 4.6" 产出一套自媒体内容，公众号+小红书+抖音+B站都要，抖音和B站出视频
```

**Discovery only:**
```
最近 AI 编程领域有什么值得写的？帮我调研一下选题
```

**Single platform:**
```
帮我把这篇博客改成一篇小红书种草文案
```

**Video from a script:**
```
把这个口播脚本做成抖音视频
```

## 📁 Structure

```
media-workspace/
├── CLAUDE.md / AGENTS.md          # workspace conventions (incl. output path rules)
├── plugins/
│   └── media-pilot/               # ← this plugin
│       ├── .claude-plugin/plugin.json
│       ├── hooks/                 # SessionStart → injects using-media-pilot
│       ├── skills/
│           ├── using-media-pilot/ # Meta-skill (proactive trigger)
│           ├── content-discovery/ # Trending research
│           ├── content-strategy/  # Angle + platform mapping
│           ├── platform-writing/  # per-platform copy + wechat-images.md / xiaohongshu-images.md
│           └── video-production/  # HyperFrames + MiniMax TTS
│               └── scripts/minimax_tts.sh
│       └── deepagent/             # standalone agent (deepagents): agent/ prompts/ tools/
│                                 #   motion_graphics/ scheduler/ + _scripts/ (bundled, brand-driven)
└── content/                       # generated content (one folder per topic)
    └── <YYYY-MM-DD-topic-slug>/
        ├── discovery.md · strategy.md
        ├── wechat.md · xiaohongshu.md · douyin-script.md · bilibili.md
        ├── wechat-images.md · xiaohongshu-images.md  # per-platform image prompts (manual)
        ├── audio/                 # MiniMax narration mp3s + manifest.json
        └── douyin.mp4 · xiaohongshu.mp4 · bilibili.mp4
```

All skills write to `content/<YYYY-MM-DD-topic-slug>/` — the discovery stage creates the folder, later stages reuse it.

## 🌐 Content sources

**Domestic:** 微博热搜 · 抖音热榜 · 百度热搜 · 知乎热榜 · B站热门 · 36氪 / 虎嗅

**International:** Hacker News · Reddit · GitHub Trending · dev.to · arXiv · Twitter/X · TechCrunch · The Verge

**AI Labs:** OpenAI · Anthropic · Google DeepMind · Meta AI · Mistral · xAI · Cohere · Hugging Face

## 📝 Output per topic

Each topic produces one folder under `content/`:
- **Research & plan** — `discovery.md`, `strategy.md`
- **Copy** — `wechat.md`, `xiaohongshu.md`, `douyin-script.md`, `bilibili.md`
- **Visuals** — `wechat-images.md` / `xiaohongshu-images.md` (per-platform image prompts; generate in your own tool)
- **Video** — `audio/` (MiniMax narration) + `douyin.mp4` / `xiaohongshu.mp4` / `bilibili.mp4`

## ⚠️ Notes & limitations

- **No auto-publishing.** Media-Pilot produces ready-to-post files; you do the final posting to each platform.
- **No fabricated trends.** Discovery uses real web search; if search is unavailable or rate-limited, it says so honestly.
- **Images are manual.** It emits per-platform prompt docs (`wechat-images.md`, `xiaohongshu-images.md`); bring your own image tool (AI image quality for Chinese-text diagrams is unreliable, so text is overlaid by hand).
- **International-first for tech topics.** For AI/tech, international sources are checked first — they lead Chinese platforms by weeks.

## 🤝 Contributing

PRs welcome. The pipeline is skill-based, so adding a platform, a source, or a new stage is mostly a new skill folder + a routing line in `using-media-pilot`. Keep plugin code under `plugins/` and all generated output under `content/` (never inside the plugin).

## 🙏 Credits

- **[HyperFrames](https://github.com/heygen-com/hyperframes)** (heygen-com) — the open-source HTML→MP4 video engine.
- **[superpowers](https://github.com/obra/superpowers)** (obra) — the proactive-skill pattern this plugin follows.
- **MiniMax** — fluent Mandarin TTS for video narration.
- Inspired by the Chinese self-media creator community.

## 📄 License

MIT — see [LICENSE](./LICENSE).
