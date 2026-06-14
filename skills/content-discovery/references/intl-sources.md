# International Content Discovery Sources

For tech / AI / creator topics, international sources often surface trends **1–4 weeks before** they reach Chinese platforms. Localizing an early international trend for a Chinese audience is one of the highest-value content plays. Always check these for tech topics.

## Hacker News

- URL: https://news.ycombinator.com
- What: Tech/Startup community voting; the front page is a strong signal for what developers care about
- Best for: 编程工具、开源项目、AI 工程、创业、硅谷文化
- Fetch: `mcp__web_reader__webReader https://news.ycombinator.com` — front page + "Show HN"
- Signal: 200+ points = meaningful; 500+ = broad dev interest; 1000+ = likely to cross over to mainstream tech media

## Reddit

| Subreddit | URL | Focus |
|-----------|-----|-------|
| r/programming | https://www.reddit.com/r/programming | General software engineering |
| r/MachineLearning | https://www.reddit.com/r/MachineLearning | AI/ML research & industry |
| r/LocalLLaMA | https://www.reddit.com/r/LocalLLaMA | Local/open LLMs — **early signal for 模型/AI 应用 trends** |
| r/OpenAI / r/ChatGPT | https://www.reddit.com/r/OpenAI | GPT/ChatGPT ecosystem |
| r/singularity | https://www.reddit.com/r/Singularity | Futurist AI hype & debate |
| r/webdev | https://www.reddit.com/r/webdev | Frontend/web dev |

- Fetch: `mcp__web_reader__webReader https://www.reddit.com/r/<sub>/top/?t=week`
- Signal: "Hot" = current; "Top this week" = sustained. Sort by top-week for content-worthy (not just viral) topics.

## GitHub Trending

- URL: https://github.com/trending
- What: Fastest-growing repos — new tools/frameworks before they're widely known
- Best for: 开发者工具、新框架、AI 应用
- Fetch: `mcp__web_reader__webReader https://github.com/trending?since=weekly`
- Filter by language if domain-specific (e.g. `?since=weekly&language=python`)
- Signal: A repo jumping from 1k → 5k stars in a week = strong content opportunity (教程/评测)

## dev.to

- URL: https://dev.to/top/week
- What: Developer blog platform; tutorials and opinion pieces trending
- Best for: 教程选题、开发者观点
- Signal: High-engagement articles here = proven topics to localize

## arXiv (学术/AI 论文)

- URL: https://arxiv.org/list/cs.AI/recent , https://arxiv.org/list/cs.CL/recent
- What: Pre-print research papers (cs.AI, cs.CL, cs.LG)
- Best for: 前沿 AI 研究、论文解读选题
- Use when: Major labs publish a notable paper (often cross-referenced with their blog)
- Note: Heavy/technical — only pick papers with clear real-world implications for mass content

## Twitter / X

- URL: https://x.com
- What: Real-time discussion; AI/tech discourse moves fastest here
- Key accounts to track (AI/tech):
  - **AI Labs**: @OpenAI, @AnthropicAI, @GoogleDeepMind, @AIatMeta, @MistralAI, @xai
  - **Researchers/engineers**: @karpathy, @ylecun, @sama, @gdb, @_jasonwei, @clem
  - **Commentary/news**: @swyx, @emollick, @simonw
- Fetch: Direct scraping is often blocked; use WebSearch with `site:x.com <topic>` or rely on what HN/Reddit already surfaced (they amplify Twitter). When a claim originates on Twitter, cite the account.
- Signal: A thread going viral among AI accounts → expect it on HN/Reddit within 24-48h → Chinese platforms within 1-2 weeks.

## AI Lab Blogs（大模型公司官方博客）★ 高价值

These are primary sources for model/feature releases — the single most reliable content-driver for AI topics. New posts here almost always generate a wave of derivative content.

| Company | Blog URL | What to watch |
|---------|----------|---------------|
| **OpenAI** | https://openai.com/blog | New models (GPT/o-series), feature launches, safety/research posts |
| **Anthropic** | https://www.anthropic.com/news | Claude releases, research (Constitutional AI, interpretability), policy |
| **Google DeepMind** | https://deepmind.google/discover/blog/ | Gemini updates, AlphaFold/science, research |
| **Meta AI** | https://ai.meta.com/blog/ | Llama releases, open weights, FAIR research |
| **Mistral AI** | https://mistral.ai/news | Open-weight models, European AI perspective |
| **xAI** | https://x.ai/blog | Grok updates |
| **Cohere** | https://cohere.com/blog | Enterprise RAG/IRAD, multilingual |
| **Hugging Face** | https://huggingface.co/blog | Open-source models, demos, community |

- Fetch: `mcp__web_reader__webReader <blog-url>` — check for posts in the last 1-2 weeks
- **Routine**: For any AI content request, scan these blogs first. A new model release (e.g. "Claude 4.6 发布") is immediately content-worthy across all platforms: 公众号 (深度解读), B站 (教程/对比), 抖音 (一句话说清), 小红书 (怎么用)。

## TechCrunch / The Verge / Ars Technica（主流科技媒体）

- URLs: https://techcrunch.com , https://www.theverge.com/tech , https://arstechnica.com
- What: Mainstream tech journalism — useful for confirmation and consumer-angle framing
- Best for: 当一个技术趋势开始破圈进入大众时

## How to prioritize

1. **AI lab blogs** — check first for any AI topic; releases here are the gold standard content trigger
2. **Hacker News + Reddit r/LocalLLaMA** — developer/AI-engineering signal
3. **GitHub Trending** — new tools worth a 教程/评测
4. **Twitter/X** — fastest, but verify (lots of noise)
5. **arXiv** — only for deep research-explainer content
6. **Mainstream tech media** — confirmation/framing, usually lags the above

## Localization insight

When you find a hot international topic, the value-add for Chinese audiences is:
1. **Translate + explain** the core idea in Chinese
2. **Add local context** — how does it affect Chinese users/developers? (e.g. 可用性 in China, 替代方案, 本土对标)
3. **Reframe the angle** — Western coverage is often US-centric; Chinese audiences care about 实操/落地/性价比

This "international trend → localized Chinese take" pipeline is consistently high-performing because you're surfacing something early and making it accessible.
