---
name: content-strategy
description: "Turn a topic (or discovery results) into a concrete content plan: pick angles, decide which platforms to target, and structure each piece before writing. Use this after content-discovery, or when the user has a topic but no plan. Bridges research and writing — produces a per-platform outline that platform-writing can execute."
---

# Content Strategy

Take a topic or discovery report and produce a concrete, platform-aware content plan. This is the bridge between "what's worth writing" and "the actual copy."

## When to Use

- After `content-discovery` has surfaced topics
- User gives a topic directly and wants to create content for multiple platforms
- User says "帮我围绕 XX 写内容" / "这个选题怎么做"

## Process

### 1. Confirm inputs

You need:
- **Topic** — either from discovery report or stated directly
- **Target platforms** — 公众号 / 小红书 / 抖音 / B站 (default: ask user, or all four if "全套")
- **Goal** — traffic? authority? conversion? (affects angle choice)

If any are unclear, ask. Don't guess platforms — copy style differs too much.

### 2. Generate angles

For the topic, brainstorm 3–5 distinct content angles. Different angles suit different platforms:

| Angle type | Best platforms | Example (topic: "Claude 4.6 发布") |
|-----------|----------------|-----------------------------------|
| **News/第一时间** | 公众号, 抖音 | "Claude 4.6 来了，5 个你必须知道的变化" |
| **教程/实操** | 公众号, B站, 小红书 | "手把手教你用 Claude 4.6 提升 3 倍效率" |
| **对比/评测** | B站, 知乎, 公众号 | "Claude 4.6 vs GPT-5: 实测 10 个任务" |
| **观点/解读** | 公众号, 知乎 | "为什么说 Claude 4.6 改变了 AI 编程的格局" |
| **种草/清单** | 小红书, 抖音 | "Claude 4.6 必收藏的 8 个神仙用法✨" |

### 3. Map angles → platforms

Decide which angle each platform gets. Not every platform needs every angle — pick the best fit:

```
公众号: 深度解读 + 实操教程 (long-form)
小红书: 种草清单 (visual, casual)
抖音:   一句话新闻 + 口播教程 (short, hook-driven)
B站:    对比评测 + 详细教程 (mid-length, knowledge)
```

### 4. Structure each piece

For each platform, write a brief outline (not the full copy — that's platform-writing's job):

**公众号大纲示例:**
```
标题方向: Claude 4.6 实测：写代码到底强了多少？
- 开头: 痛点（AI 编程工具现状）
- 核心变化: 3 个关键升级 + 实测对比
- 实操: 3 个最佳使用场景 + prompt 示例
- 结尾: 适合谁用 + 局限性
CTA: 关注/转发
```

### 5. Deliver

Save the plan to `strategy.md` inside the working directory discovery created (`content/<YYYY-MM-DD-topic-slug>/`):

```markdown
# 内容策略：<topic>

## 目标平台: 公众号 / 小红书 / 抖音 / B站

## 选题角度
1. ...
2. ...

## 各平台方案

### 公众号
- 角度: ...
- 大纲: ...
- 预计字数: 2000-3000 字

### 小红书
- 角度: ...
- 大纲: ...
- 配图建议: ...

### 抖音
- 角度: ...
- 脚本结构: 钩子(3s) → 主体(30s) → CTA(5s)

### B站
- 角度: ...
- 大纲: ...
- 预计时长: 8-12 分钟

## 下一步
→ 调用 platform-writing skill 逐个产出文案
```

## Principles

- **One strong angle per platform** — don't try to cram everything into one piece.
- **Match angle to platform DNA** — see `platform-writing/references/*.md` for each platform's style DNA.
- **Leave room for the writer** — strategy produces the skeleton; platform-writing adds the voice.
- **Reuse research** — the same discovery material feeds all platforms; just reframe it.

## Anti-Patterns

- Don't write the full copy here — that's platform-writing's job. Strategy = structure + angle.
- Don't pick the same angle for every platform — that wastes the multi-platform opportunity.
- Don't skip the outline — writing without structure produces rambling copy.
