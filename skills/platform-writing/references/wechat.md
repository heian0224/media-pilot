# 微信公众号 (WeChat Official Account) Writing Guide

Long-form, depth-oriented content for a reader who chose to open the article. The bar is substance — a 公众号 reader will read 2000+ words if they're worth reading.

## Voice & Tone
- **Formal but not stiff** — like a knowledgeable friend or industry expert, not a news anchor
- **有观点** — take a stance, don't just report. Readers come for the take, not the news
- **具体** — real numbers, real examples, real cases. Vague = worthless
- **克制 emoji** — occasional ✅/💡 is fine; emoji spam reads as unprofessional

## Length & Structure
- **2000-4000字** typical; can go longer (5000+) for deep tutorials/analysis
- **标题**: 18-30字, must create curiosity or promise value. Examples:
  - ✅ "Claude 4.6 实测：写代码到底强了多少？我用它重构了一个 5 万行的项目"
  - ✅ "为什么大厂都在裁程序员？一个 AI 程序员的真实观察"
  - ❌ "关于 AI 编程的思考" (too vague)
- **结构**:
  ```
  开头(钩子 + 痛点共鸣, 200-300字)
  → 小标题1 (核心观点/背景)
  → 小标题2 (详细分析/数据/案例)
  → 小标题3 (实操建议/方法论)
  → 结尾(总结 + CTA)
  ```

## Formatting conventions
- **小标题分段** — use ##/### headers, readers skim
- **引用块** for key quotes/data (`> `)
- **短段落** — 1-3 sentences per paragraph, lots of white space
- **加粗** key phrases and numbers (公众号 readers skim)
- **图片** — 封面图 (16:9 or 2.35:1), 正文配图每 500字一张。**写完正文要单独生成 `wechat-images.md`（见下方「配图要求」）**
- **文末** — 引导关注/转发/在看的 CTA

## 配图要求（生成 `wechat-images.md`）

公众号是**长文深度**——读者主动点开、会读 2000+ 字，图片服务于"把事讲透"。`platform-writing` 写完正文后，**单独生成 `wechat-images.md`**（与小红书的 `xiaohongshu-images.md` 分开），含一套公众号专属配图 prompt。

- **数量**：**1 封面 + 正文每 ~500 字一张**（2000 字约 5–6 张，4000 字约 9–10 张）。
- **比例**：**封面 16:9（或 2.35:1 宽幅）**；正文图 16:9 或 4:3，宽度 ~1080px。
- **风格**：比小红书**更密、更"硬"**——可以是数据图、流程图、对比图、信息图，承载信息而不只是氛围。整体调性偏专业 / 深度。
- **封面**：承担"信息流里被点开"的任务——大标题感 + 一个核心视觉钩子（反差 / 数字 / 结果），别太抽象。
- **正文图类型**（按内容选）：封面 / 章节分隔图 / 数据图表 / 流程或架构图 / 对比图（before-after、X vs Y）/ 金句卡 / 引用块 / 结尾引导。
- **中文一律后期叠**：AI 直出中文基本乱码——prompt 生成**无字底图**，再用 Figma / Canva 叠中文（标题、数据标签、图注）。每张图在 prompt 旁列出 **"叠字内容"**。
- **全套风格统一**：同一套调色板 / 质感 / 线宽，封面到结尾一气呵成。
- **每张配齐**：用途、比例、叠字内容、画面描述、可直接喂出图工具的 prompt。

> 公众号图**可以比小红书密**（读者在正文里细看），但仍要避免 AI 直出中文——数据图的坐标轴 / 标签都手工叠。

## Hook patterns that work
- **痛点开场**: "你是不是也遇到过..."
- **反常识**: "很多人以为 X，但其实..."
- **数据/结果先行**: "用这个方法，我 3 天涨了 10000 粉"
- **故事开场**: "上周一个朋友问我..."

## CTA patterns
- "觉得有用，点个**在看**👇"
- "关注我，每周分享 AI 编程干货"
- "加我微信 xxx，进交流群"

## Common mistakes
- ❌ 太长太水 — 4000字但只有 1000字干货 → 掉粉
- ❌ 没有观点 — 纯客观陈述，读完没记住任何观点
- ❌ 标题党过度 — 标题承诺了正文给不了的东西 → 取关
- ❌ 像 AI 写的 — 排比句堆砌、空洞的"在这个数字时代"、过度书面化
