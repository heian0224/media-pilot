# Media-Pilot 🚀

> 面向 Claude Code 的自媒体内容自动引擎——发现热点、撰写各平台原生文案、生成配音视频。专为中文内容生态打造（公众号 / 小红书 / 抖音 / B站）。

**[English](./README.md) · [中文](./README.zh-CN.md)**

把一个选题——或只是一句"帮我找点值得写的"——变成可直接发布的跨平台内容：**公众号、小红书、抖音、B站**，外加带流畅中文配音的短视频。

## ✨ 特性

- **🔬 选题发现** — 同时抓中文平台（微博 / 抖音 / 百度 / 知乎 / B站 / 36氪 / 虎嗅）和国际技术媒体（Hacker News、Reddit、GitHub Trending、dev.to、arXiv、Twitter/X、各家 AI 实验室博客）的真实热度信号。技术 / AI 选题能**领先国内平台 1–4 周**发现。
- **🎯 策略** — 选定角度，把内容映射到合适的平台。
- **✍️ 平台写作** — 按各平台调性出稿：公众号深度长文、小红书 emoji 种草、抖音钩子口播、B站硬核内容。另出**按平台分文件**的配图提示词（`wechat-images.md` / `xiaohongshu-images.md`），方便你用自己的工具出图。
- **🎬 视频** — 脚本 → 带配音的 MP4，用 **HyperFrames**（本地 HTML→MP4 渲染）+ **MiniMax TTS**（流畅中文）。不需要 HeyGen、不需要数字人 API、不按分钟计费。

## 🧠 工作原理

采用 [superpowers](https://github.com/obra/superpowers) 的主动技能模式：一个 `using-media-pilot` 元技能在你做任何内容工作时自动激活（会话开始时由 hook 注入），再路由到对应的阶段技能。

```
发现 → 策略 → 写作 → 视频
```

可跑完整流水线，也可单跑某个阶段。

## 🤖 两种运行方式

Media-Pilot **既是 Claude Code 插件，也是独立自主运行的 agent**（`deepagent` Python 包，基于 [LangChain `deepagents`](https://docs.langchain.com/oss/python/deepagents/overview)）。同一套品牌、prompt、工具、视频引擎——两个前端：

| | Claude Code 插件 | 独立 `deepagent` |
|---|---|---|
| 跑在哪 | Claude Code REPL（交互） | 普通 Python 进程 / cron |
| 触发 | 跟 Claude 对话 | `python -m deepagent run --topic "..."` / `--auto` / `schedule --cron` |
| 适合 | 手动、逐阶段调 | **无人值守 / 定时**出内容 |

### 独立 agent 快速上手

```bash
pip install -e ./plugins/media-pilot             # 装上 deepagent 包
python -m deepagent run --topic "GLM-4.6 开放智能体"  # 定题 → 全流程（含视频）
python -m deepagent run --auto                         # 自主选一个 trending 选题
python -m deepagent run --auto --dry-run               # 只选题+记日志，不跑流水线
python -m deepagent schedule --cron "7 9 * * *"        # 打印 crontab 行（--install 安装）
```

**配置**：OpenAI 兼容 LLM key + base URL（默认智谱 GLM `https://open.bigmodel.cn/api/paas/v4`，模型 `glm-4.6`；视觉 `glm-4v-flash` 用于图片文字核验；也支持 DeepSeek / Moonshot / OpenAI），`MINIMAX_API_KEY`（中文口播），`GPT_IMAGE_API_KEY`+`GPT_IMAGE_ENDPOINT`（封面/分节图），`TAVILY_API_KEY`（选题搜索）。放 `.claude/settings.local.json` 的 `env`、或 `.env`、或真实环境变量。

**品牌**：仓库**品牌中立**——把 [`brand.example.md`](./brand.example.md) 拷成工作区根的 `brand.md` 填好，agent 运行时读取并应用到所有产出。

**架构**：一个编排 agent + 4 个上下文隔离的子 agent（discovery / strategy / writing / video），产物靠**文件路径**传递。见 [`deepagent/`](./deepagent/) 目录。

## 📦 环境要求

- **Claude Code** —— 这是一个 Claude Code 插件（不是独立 App）
- **Node.js 22+** 和 **ffmpeg** —— HyperFrames 视频渲染用
- 一个**联网搜索工具**用于选题发现 —— 推荐 [Tavily MCP](https://tavily.com)（内置 WebSearch / WebFetch 也行）
- **MiniMax API key** —— 视频中文配音用（见安装）

## 🔧 安装

1. **准备 media-workspace。** Media-Pilot 设计为放在 workspace 的 `plugins/media-pilot/` 下，同级有个 `content/` 目录放产出（见[目录结构](#-目录结构)）。Clone 本仓库，或按下方目录树自建。

2. **在 Claude Code 里加载插件** —— 在 Claude Code 内 `/plugin`，或启动时：
   ```bash
   claude --plugin-dir ./plugins/media-pilot
   ```

3. **安装 HyperFrames**（视频引擎）：
   ```bash
   npx skills add heygen-com/hyperframes
   npx hyperframes doctor   # 首次运行：下载渲染用的 Chrome
   ```

4. **设置 MiniMax key**（在 MiniMax 开放平台获取，充值约 ¥10 可做很多条视频）：
   ```jsonc
   // .claude/settings.local.json  （本地配置，不会被提交）
   { "env": { "MINIMAX_API_KEY": "你的-key" } }
   ```

5. **（推荐）配置 Tavily MCP** 用于选题发现。

> ⚠️ **HyperFrames ≠ HeyGen。** 虽然它挂在 `heygen-com` 这个 GitHub 组织下，但 HyperFrames 是**开源的本地 HTML→MP4 框架**——不需要 HeyGen 账号、不要 API key、不是数字人服务。
>
> ⚠️ **MiniMax 网络：** 插件自带的 TTS 脚本以**直连 + `--http1.1`** 方式调用 MiniMax，并会 unset 所有 proxy 环境变量。走代理会导致 TLS 报错（连接重置 / HTTP2 framing / SSL 握手失败）。国内 IP 直连即可。

## 🎬 使用示例

**全自动流水线：**
```
帮我围绕 "Claude 4.6" 产出一套自媒体内容，公众号+小红书+抖音+B站都要，抖音和B站出视频
```

**只做选题发现：**
```
最近 AI 编程领域有什么值得写的？帮我调研一下选题
```

**单平台：**
```
帮我把这篇博客改成一篇小红书种草文案
```

**脚本转视频：**
```
把这个口播脚本做成抖音视频
```

## 📁 目录结构

```
media-workspace/
├── CLAUDE.md / AGENTS.md          # workspace 约定（含输出路径规则）
├── plugins/
│   └── media-pilot/               # ← 本插件
│       ├── .claude-plugin/plugin.json
│       ├── hooks/                 # SessionStart → 注入 using-media-pilot
│       └── skills/
│           ├── using-media-pilot/ # 元技能（主动触发）
│           ├── content-discovery/ # 热点调研
│           ├── content-strategy/  # 角度 + 平台映射
│           ├── platform-writing/  # 各平台写作 + wechat-images.md / xiaohongshu-images.md
│           └── video-production/  # HyperFrames + MiniMax TTS
│               └── scripts/minimax_tts.sh
└── content/                       # 产出内容（每个选题一个文件夹）
    └── <YYYY-MM-DD-topic-slug>/
        ├── discovery.md · strategy.md
        ├── wechat.md · xiaohongshu.md · douyin-script.md · bilibili.md
        ├── wechat-images.md · xiaohongshu-images.md  # 按平台的配图提示词（手工出图）
        ├── audio/                 # MiniMax 配音 mp3 + manifest.json
        └── douyin.mp4 · xiaohongshu.mp4 · bilibili.mp4
```

所有技能都写到 `content/<YYYY-MM-DD-topic-slug>/`——发现阶段建文件夹，后续阶段复用。

## 🌐 内容源

**国内：** 微博热搜 · 抖音热榜 · 百度热搜 · 知乎热榜 · B站热门 · 36氪 / 虎嗅

**国际：** Hacker News · Reddit · GitHub Trending · dev.to · arXiv · Twitter/X · TechCrunch · The Verge

**AI 实验室：** OpenAI · Anthropic · Google DeepMind · Meta AI · Mistral · xAI · Cohere · Hugging Face

## 📝 单个选题的产出

每个选题在 `content/` 下一个文件夹：
- **调研 + 计划** — `discovery.md`、`strategy.md`
- **文案** — `wechat.md`、`xiaohongshu.md`、`douyin-script.md`、`bilibili.md`
- **配图** — `wechat-images.md` / `xiaohongshu-images.md`（按平台的配图提示词，用自己的工具出图）
- **视频** — `audio/`（MiniMax 配音）+ `douyin.mp4` / `xiaohongshu.mp4` / `bilibili.mp4`

## ⚠️ 说明与限制

- **不自动发布。** 只产出可发布的文件，最终发到各平台由你手动完成。
- **不编造热点。** 发现用真实联网搜索；搜索不可用或被限流时如实说明，绝不编。
- **配图需手工。** 出按平台的提示词文档（`wechat-images.md` / `xiaohongshu-images.md`），用自己的图像工具生成（AI 生成带中文的图容易乱码，文字部分建议手工叠加）。
- **技术选题优先看国际源。** AI / 技术话题先查国际源——它们领先国内平台数周。

## 🤝 贡献

欢迎 PR。流水线是基于技能的，新增平台 / 数据源 / 阶段基本就是新建一个 skill 文件夹 + 在 `using-media-pilot` 里加一行路由。插件代码放 `plugins/`，所有产出放 `content/`（绝不写进插件目录）。

## 🙏 致谢

- **[HyperFrames](https://github.com/heygen-com/hyperframes)**（heygen-com）—— 开源的 HTML→MP4 视频引擎。
- **[superpowers](https://github.com/obra/superpowers)**（obra）—— 本插件采用的主动技能模式。
- **MiniMax** —— 流畅中文 TTS 配音。
- 灵感来自中文自媒体创作者社区。

## 📄 许可证

MIT —— 见 [LICENSE](./LICENSE)。
