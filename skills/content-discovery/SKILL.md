---
name: content-discovery
description: "Find what's worth creating content about. Use this skill whenever the user wants to discover trending topics, find hot angles, research what to write about, or gather reference material for self-media content. Covers both Chinese social trending (微博/抖音/百度/知乎/B站) and international tech media (Hacker News, Reddit, GitHub Trending, dev.to, arXiv, Twitter/X, and AI lab blogs from OpenAI/Anthropic/DeepMind/Meta/Mistral). Invoke before brainstorming topics."
---

# Content Discovery

Discover what's trending and worth creating content about. This skill gathers real signals from domestic and international sources, then uses AI judgment to rank topics by content potential.

## When to Use

- User asks "最近有什么热点" / "有什么值得写的" / "帮我找选题" / "what should I write about"
- User has a broad domain (e.g. "AI 编程") and wants concrete angles
- Before writing, when the user needs reference material and a competitive view

## Process

### 1. Clarify scope

Ask (briefly, only if unclear):
- What domain/topic? (e.g. AI, 编程, 职场, 消费)
- Which audience/platforms are they targeting? (affects which sources matter)
- Domestic focus, international focus, or both?

### 2. Pull signals from sources

Read `references/cn-sources.md` and `references/intl-sources.md` for the exact source list, fetch URLs, and how to interpret each.

**Domestic trending** — Chinese platforms' hot lists give real-time mass interest:
- 微博热搜, 抖音热榜, 百度热搜, 知乎热榜, B站热门

**International tech media** — for tech/creator topics, these surface trends 1-4 weeks before they hit China:
- Hacker News, Reddit (r/programming, r/MachineLearning, r/LocalLLaMA), GitHub Trending, dev.to, arXiv
- **Twitter/X** — follow key accounts and AI discussions
- **AI lab blogs** — OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral (new model/paper releases drive huge content demand)

Use the WebSearch / WebFetch tools (or `mcp__web_reader__webReader`) to pull current data. **If web tools are rate-limited or unavailable, tell the user honestly** — do not invent trending topics.

### 3. Cross-reference and deduplicate

The same story often appears on multiple sources. Merge them and note where it's trending (e.g. "Claude 4.6 发布 — 同时登上 HN 首页 + Reddit r/LocalLLaMA + Twitter 热议").

### 4. Rank by content potential

Score each candidate topic on:

| Signal | What it means |
|--------|--------------|
| **Heat** | How widely it's being discussed right now |
| **Velocity** | Is interest rising fast? (early = better content window) |
| **Angle availability** | How many distinct takes are possible (tutorial, opinion, comparison, news) |
| **Platform fit** | Does it fit the user's target platforms? |
| **Originality gap** | Is the existing coverage shallow/generic (room for a better take)? |
| **Longevity** | Evergreen potential vs. a 2-day flash |

### 5. Deliver

**Create the working directory** `content/<YYYY-MM-DD-topic-slug>/` (today's date + a short kebab-case topic slug, e.g. `content/2026-06-13-claude-4.6/`). This is the single output folder every later stage reuses. Then save the discovery report to `discovery.md` inside it:

```markdown
# 选题调研：<topic>
日期: YYYY-MM-DD

## Top 5 选题建议（按内容潜力排序）

### 1. <选题>
- **热度来源**: 微博热搜 #3, HN 首页, Twitter
- **为什么值得写**: ...
- **推荐角度**: 
  - 教程向（适合公众号/B站）
  - 争议观点（适合知乎/视频）
- **目标平台**: 公众号 + 抖音
- **参考资料**: [link1], [link2]

### 2. ...
```

Also save `references.json` with the raw source links gathered, for the writing stage to cite.

## International-Lag Insight

For tech/AI topics specifically: international sources (HN, AI lab blogs, Twitter) often surface trends **1-4 weeks before** they reach Chinese platforms. Surfacing an international trend early and localizing it for a Chinese audience is one of the highest-value content plays. Always check international sources for tech topics, even if the user only named Chinese platforms.

## Anti-Patterns

- **Don't invent trends.** If you can't fetch a source, say so and work with what you have.
- **Don't dump raw lists.** Rank and explain why each topic is worth writing — that's the value.
- **Don't ignore the user's domain.** A trending celebrity gossip item is useless to an AI-programming creator.
