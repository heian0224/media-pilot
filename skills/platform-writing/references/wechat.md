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
- **中文直接烘焙进图**：GPT-Image-2 直出中文准确率 ~99%——把中文标题 / 数据标签 / 图注**直接写进 prompt 让模型渲染**，图即成品（不再走"无字底图 + 后期叠字"）。中文尽量短（标题 + 关键词 + 数字），专有名词保留英文。细节见 `image-gen` skill。
- **全套风格统一**：同一套调色板 / 质感 / 线宽，封面到结尾一气呵成。
- **每张配齐**：用途、比例、画面描述、要烘焙的中文文字、可直接喂出图工具的 prompt。
- **末尾品牌收尾图：固定复用一张品牌收尾图（`brand/assets/wechat-signoff.png`，按 workspace 根目录 `brand.md` 的账号名 / slogan / 站点 / 关注 CTA 制作一次），所有文章共用，不要每篇重新生成。** 文章专属金句写进正文（不进末尾图）。配图清单里不要再列「结尾引导图」。

## 渲染成可粘贴的 HTML（`wechat.md` → `wechat.html`）

公众号后台粘贴时会剥掉 `<style>` 和 class，只有 inline style 留得住——所以写完 `wechat.md`、出好配图 PNG 后，**必须跑渲染器**把品牌样式烘焙进每个元素，产出可直接粘贴的 `wechat.html`（见 `SKILL.md` 第 6 步）：

```bash
python3 plugins/media-pilot/skills/platform-writing/scripts/wechat_render.py content/<date>-<slug>/wechat.md
```

**在 `wechat.md` 里标记配图的方式**（渲染器按此插图，写错则图不出现）：
- **封面**：正文第一个 `> 引用块` 自动作为导语 + 插入 `wechat-cover.png`，**不要再手动加封面图**（会重复）。
- **正文配图**：用原生 markdown `![图注](wechat-<名>.png)` 写在想出现的位置（文件须存在，否则出占位卡）。**不要**用 `【配图N：…】` 这种纯文本标记——它会被当成字面文字、不插图。
- **结尾**：含品牌名 + slogan 的段落/引用（如「黯镜 AI，折射未来幻想。」）会自动触发签名卡 + 收尾图。

> 公众号图**可以比小红书密**（读者在正文里细看）——数据图的坐标轴、标签、图注都可以直接烘焙中文进图。

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
