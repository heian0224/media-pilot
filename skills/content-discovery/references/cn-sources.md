# Chinese Content Discovery Sources

Domestic trending sources for the Chinese self-media market. Use these to gauge mass interest and find topics already resonating with Chinese audiences.

## 热榜聚合（一站式看多个平台）

| Source | URL | Notes |
|--------|-----|-------|
| 今日热榜 | https://tophub.today | Aggregates 微博/知乎/抖音/B站/百度 etc. — **best single starting point** |
| 韭菜盒子 / DailyHot | https://dailyhot.arthals.dev | Clean aggregator, API-friendly |
| 黑客派热榜 | https://bhdu.hackshen.com | Tech-leaning aggregation |

## 微博热搜

- URL: https://s.weibo.com/top/summary
- What: Real-time mass-interest topics in China. High velocity, short lifespan.
- Best for: 消费、娱乐、社会热点、突发新闻
- Angle: Often opinion/controversy-driven — good for 知乎/公众号评论向

## 抖音热榜

- URL: https://www.douyin.com/hot
- What: Short-video trending — what's getting views right now
- Best for: 消费、生活、娱乐、情绪共鸣类
- Angle: Strong signal for what works as 短视频 — topics here translate well to 抖音 content

## 百度热搜

- URL: https://top.baidu.com/board?tab=realtime
- What: Search-volume-driven, broadest mass interest
- Best for: 大众话题、社会热点
- Angle: More conservative/official-leaning than 微博

## 知乎热榜

- URL: https://www.zhihu.com/hot
- What: Discussion/Q&A trending — longer-form, more thoughtful
- Best for: 深度讨论、专业话题、职场、科技
- Angle: Good seed for 公众号深度文章 and B站知识类视频

## B站热门

- URL: https://www.bilibili.com/v/popular/all
- What: Video content trending — what creators are succeeding with
- Best for: 知识科普、教程、二次元、年轻向
- Angle: Direct signal for what B站 audiences engage with; study top video titles/thumbnails

## 36氪 / 虎嗅（科技商业）

- 36氪: https://36kr.com/hot-list/catalog
- 虎嗅: https://www.huxiu.com
- What: Tech/business news and analysis
- Best for: 科技、创业、商业模式分析
- Angle: Useful for cross-checking international tech trends that have landed in China

## How to fetch

- Use `mcp__web_reader__webReader` with the URL for rendered pages.
- For `tophub.today`, fetch the homepage — it summarizes all platforms in one page (token-efficient).
- If a site blocks scraping (returns login wall), note it and fall back to WebSearch for that platform's trending keywords.

## Interpretation notes

- **微博 = 情绪/争议导向**, **知乎 = 深度/专业**, **抖音 = 消费/生活**, **B站 = 知识/年轻向**, **百度 = 大众/官方**.
- A topic trending on multiple platforms simultaneously = high-value, broad appeal.
- A topic trending only on 知乎 but not 微博 = niche/professional, good for targeted 公众号/B站 content, less for mass 抖音.
