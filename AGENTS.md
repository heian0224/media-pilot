# Media-Pilot — Agent Guide

Guidance for any AI coding agent working on **media-pilot**. (Claude Code users: `CLAUDE.md` has the same in Claude-Code terms.) Maintained alongside `README.md`.

## What this is

An **autonomous self-media content engine** for the Chinese ecosystem (公众号 / 小红书 / 抖音 / B站). It runs as **two interchangeable front-ends over one shared core**:

1. **Claude Code plugin** — `skills/` + `hooks/`, used interactively in the Claude Code REPL.
2. **Standalone agent** — the `deepagent` Python package (built on LangChain [`deepagents`](https://docs.langchain.com/oss/python/deepagents/overview)), runnable as a plain process or on cron.

Both share the same brand, prompts, tools, and motion-graphics engine. The repo is **brand-neutral** — no brand strings in code; identity is read from an external `brand.md` (`brand.example.md` is the template).

## Pipeline

```
Discovery → Strategy → Writing → Video
```

`content-discovery` (trending research) → `content-strategy` (angle + platform map) → `platform-writing` (per-platform copy + 配图 prompts) → `video-production` (HyperFrames + MiniMax TTS).

## How to run

**Standalone agent:**
```bash
pip install -e ./plugins/media-pilot
python -m deepagent run --topic "GLM-4.6 开放智能体"   # fixed topic → full pipeline (+ video)
python -m deepagent run --auto                          # autonomously pick a trending topic (de-duped)
python -m deepagent run --auto --dry-run                # just pick + log, skip the pipeline
python -m deepagent schedule --cron "7 9 * * *"         # print a crontab line (--install to add)
```

**Plugin:** `/plugin` in Claude Code, or `claude --plugin-dir ./plugins/media-pilot`, then ask in natural language ("帮我围绕 X 产出一套内容").

## Configuration

OpenAI-compatible LLM key + base URL (default 智谱 GLM `https://open.bigmodel.cn/api/paas/v4`, model `glm-4.6`; vision `glm-4v-flash` for image-text verify; works with DeepSeek/Moonshot/OpenAI too), `MINIMAX_API_KEY` (Mandarin narration), `GPT_IMAGE_API_KEY`+`GPT_IMAGE_ENDPOINT` (cover/section images), `TAVILY_API_KEY` (trend search), optional `NOTIFY_WEBHOOK_URL`. Load via `.claude/settings.local.json` `env`, a `.env`, or the real env.

## Code layout (the `deepagent` package)

```
deepagent/
├── agent/            # orchestrator + 4 subagents (discovery/strategy/writing/video) + runner + backends + model
├── prompts/          # stage prompts (distilled from skills/, shared with the plugin) + platform_dna/
├── tools/            # web, content_io, brand_check, wechat_render, images (+verify&reroll), tts, video, agnes_video
├── motion_graphics/  # 12-component HyperFrames engine (template.py + icons.py), brand palette applied
├── scheduler/        # autonomous topic-pick + de-dup, guardrails, logging/webhook, cron
├── _scripts/         # bundled brand-driven wechat_render.py + run_tts.py (self-contained)
└── cli.py            # python -m deepagent run|schedule
```

Architecture: an orchestrator deepagent delegates to the 4 context-isolated subagents; **artifacts pass by file path** (not message body) to keep context lean. Content lands under the workspace `content/<YYYY-MM-DD-topic-slug>/` (see the workspace `AGENTS.md`/`CLAUDE.md` for the output convention).

## Conventions

- **Output → `content/<YYYY-MM-DD-topic-slug>/`.** Discovery creates the folder; all stages reuse it. Never write output inside the plugin/package.
- **Brand via `brand.md`.** Don't hardcode brand names/palette in code — read from `brand.md` (or `deepagent.brand.load_brand()`). The repo must stay brand-neutral.
- **No auto-publishing.** Produces ready-to-post files; the human does the final posting.
- **No fabricated trends.** Discovery uses real web search; if unavailable, say so.

## Video: two routes

- **HyperFrames** (default) — local HTML→MP4 motion-graphics; the `motion_graphics/` engine (12 component kinds), MiniMax narration. Self-contained, no per-minute billing.
- **Agnes** (`agnes-video-v2.0`, optional) — real-footage b-roll via `tools/agnes_video.py`; the endpoint is intermittently overloaded, so it falls back to HyperFrames on failure.

Requires Node 22+ and ffmpeg for HyperFrames rendering.

## License

MIT — see `LICENSE`.
