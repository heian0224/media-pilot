# Media-Pilot

An autonomous self-media content engine for Claude Code. Discovers trending topics from global sources (Chinese social platforms + international tech media), writes platform-tailored copy (WeChat / Xiaohongshu / Douyin / Bilibili), and produces videos.

## Architecture

Inspired by the [superpowers](https://github.com/obra/superpowers) plugin's proactive-skill pattern:

- **`using-media-pilot`** — a meta-skill that proactively activates whenever the user is doing content-related work, then dispatches to specialized skills.
- A **SessionStart hook** injects the meta-skill at session start so it's always available.
- Four stage skills form a research-to-publish pipeline:
  - `content-discovery` → `content-strategy` → `platform-writing` → `video-production`

## Pipeline

```
Discovery (find what's trending / worth writing)
   → Strategy (pick angles, map to platforms)
      → Writing (draft platform-native copy)
         → Video (HyperFrames + MiniMax TTS — local HTML→MP4, fluent Mandarin narration)
```

## Sources

- **Domestic**: 微博热搜, 抖音热榜, 百度热搜, 知乎热榜, B站热门, 36氪/虎嗅
- **International**: Hacker News, Reddit (r/programming, r/MachineLearning, r/LocalLLaMA), GitHub Trending, dev.to, arXiv, Twitter/X, TechCrunch/Verge
- **AI Lab Blogs**: OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral, xAI, Cohere, Hugging Face

See each skill's `references/` for exact URLs and fetch guidance.

## Platforms Supported

| Platform | Skill reference |
|----------|----------------|
| 微信公众号 (WeChat) | `platform-writing/references/wechat.md` |
| 小红书 (Xiaohongshu) | `platform-writing/references/xiaohongshu.md` |
| 抖音 (Douyin) | `platform-writing/references/douyin.md` |
| B站 (Bilibili) | `platform-writing/references/bilibili.md` |

## Install

This plugin lives under `plugins/media-pilot` inside a media-workspace. Run Claude from the workspace root so output lands in `./content/`.

```bash
# In Claude Code, add this plugin directory
/plugin

# Or test locally (from the workspace root)
claude --plugin-dir ./plugins/media-pilot
```

## Output convention

Generated content is written to `content/<YYYY-MM-DD-topic-slug>/` at the workspace root (one folder per topic). The `content-discovery` stage creates the folder; all later stages reuse it. Never write output inside the plugin folder. See the workspace `CLAUDE.md` for the full layout.

## Requirements

- Claude Code with skill + hooks support
- WebSearch / WebFetch (or `mcp__web_reader__webReader`) for discovery — without these, discovery can't fetch real trends
- For video: **HyperFrames** (`npx skills add heygen-com/hyperframes`) — local HTML→MP4 renderer, **not** HeyGen, no avatar API. Requires Node.js 22+ and ffmpeg
- Chinese narration: `MINIMAX_API_KEY` env var (MiniMax `speech-2.8-hd`) — see the `video-production` skill and its bundled `scripts/minimax_tts.sh`

## What it does NOT do

- It does not auto-publish to platforms (no account/API integration). It produces ready-to-post files.
- It does not fabricate trending data — if web tools are unavailable, it says so.
