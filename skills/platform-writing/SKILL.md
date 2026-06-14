---
name: platform-writing
description: "Write polished self-media copy tailored to specific Chinese platforms. Use this to draft WeChat articles (公众号), Xiaohongshu posts (小红书), Douyin scripts (抖音), or Bilibili content (B站). Each platform has a distinct voice, structure, and length — read the matching reference file before writing. Invoke after content-strategy has defined the angle, or when the user asks for a specific platform's copy."
---

# Platform Writing

Turn a strategy/outline into finished, platform-native copy. The critical thing: **each platform has a different voice.** Copy that works on 公众号 flops on 小红书, and vice versa. Always consult the reference for the target platform before writing.

## When to Use

- After `content-strategy` produces an outline
- User asks directly for a specific platform's copy: "帮我写篇公众号文章" / "写个小红书文案"

## Brand

If the workspace has a **`brand.md`** (the self-media brand spec), follow it for every piece: the account name, slogan, **CTA sign-off** (sign as the brand — e.g. "关注「黯镜 AI」" — not a generic "关注我"), and visual identity. Keep the brand consistent across all platforms and reference the brand's site if it declares one. Read `brand.md` at the workspace root before writing.

## Process

### 1. Identify the target platform(s)

Confirm which platform(s). If multiple, write each separately — do NOT produce one piece and lightly retarget it. The DNA differs too much.

| Platform | Read this reference first |
|----------|---------------------------|
| 公众号 (WeChat) | `references/wechat.md` |
| 小红书 (Xiaohongshu) | `references/xiaohongshu.md` |
| 抖音 (Douyin) | `references/douyin.md` |
| B站 (Bilibili) | `references/bilibili.md` |

**MUST**: Read the reference file for the platform before writing. It encodes the voice, structure, length, and format conventions. Writing without it produces generic copy that reads wrong for the platform.

### 2. Write the copy

Follow the reference's structure and voice precisely. Key platform differences at a glance:

| | 公众号 | 小红书 | 抖音 | B站 |
|---|---|---|---|---|
| **长度** | 2000-4000字 | 300-800字 | 口播150-400字 | 文案+脚本 |
| **语气** | 正式/深度 | 轻松/种草感 | 口语/有力 | 知识/幽默 |
| **emoji** | 克制 | 多用✨🔥💡 | 口语tag | 适度 |
| **结构** | 深度长文 | 标题党+清单 | 钩子→主体→CTA | 完整脚本 |
| **配图** | 1封面 | 6-9张 | 视频封面 | 视频封面 |

### 3. Quality check before delivering

For each piece, verify:
- [ ] Hook in the first line/3 seconds (critical for 抖音/小红书)
- [ ] Voice matches the platform DNA (not generic "AI voice")
- [ ] Length is in the platform's range
- [ ] Has a clear CTA (关注/点赞/收藏/转发)
- [ ] Platform-native formatting (小红书 emoji/段间空行, 公众号 小标题/引用, etc.)
- [ ] No awkward translation-style phrasing — reads like a real Chinese creator wrote it

### 4. Save and deliver

Save each piece as a separate file inside the working directory (`content/<YYYY-MM-DD-topic-slug>/`):
- `wechat.md`
- `xiaohongshu.md`
- `douyin-script.md` (口播脚本)
- `bilibili.md` (文案/脚本)

Tell the user where each file is and offer to produce video for the platforms that need it (抖音/小红书 → invoke `video-production`).

### 5. Produce platform-specific 配图 prompt docs

Written platforms need visuals; we do **not** auto-generate images (AI image quality is unreliable and Chinese text garbles). Instead produce a **platform-specific** prompts doc the user feeds to their own image tool — **one file per platform**, because each platform's images differ in aspect ratio, density, and style:

- **公众号** → `wechat-images.md` — 16:9 封面 + ~1 per 500字, denser / diagram-friendly, formal depth style. See `references/wechat.md` → 配图要求.
- **小红书** → `xiaohongshu-images.md` — 3:4 竖版, 6–9 张, 封面 = 点击率, 文字卡为主. See `references/xiaohongshu.md` → 配图要求.
- **抖音 / B站** → no separate image set (visuals are built into the video in `video-production`).

Do **not** produce a single generic `images.md` — always split by platform. For each platform file you produce:

1. **For each image** list: slot/purpose, target aspect ratio, a ready-to-paste prompt, and the exact Chinese text to overlay manually.
2. **Lock a consistent visual style up top** per file — shared palette, line weight, mood — so the set looks cohesive.
3. **Chinese-text-heavy diagrams**: prompt for a clean scaffold with **no in-image text**, then list the Chinese labels to overlay in Figma/Canva/PS. Never ask the image model to render Chinese characters.
4. **Reference the image slots from the copy** (mark 配图 positions inline) so the user knows where each goes.

Tell the user which `<platform>-images.md` files are ready. For platforms that need **video** (抖音/小红书), continue to `video-production` after copy + 配图 prompts are ready.

## Writing Quality Standards

The bar is "reads like a human creator who knows the platform wrote it," not "grammatically correct AI text." Specifically:

- **公众号**: Substantive. Real examples, real data, a genuine point of view. Not a listicle of obvious points.
- **小红书**: Specific and relatable. "亲测" feeling, concrete numbers ("3 天涨粉 500"), emoji that feels native not forced.
- **抖音**: Tight. Every sentence earns its place. Opens with a scroll-stopping hook. Ends with a reason to engage.
- **B站**: Respects the audience's intelligence. Detailed enough to be useful, personable enough to be watchable.

If copy reads like it could be on any platform (generic), it's wrong for all of them. Rewrite it platform-specific.

## Multi-Platform Batching

When writing for multiple platforms in one go, you can parallelize: each platform's copy is independent once the strategy is set. But write them as genuinely different pieces — a 公众号 article is not a 小红书 post with paragraphs.

## Anti-Patterns

- **Don't write before reading the reference.** The reference encodes hard-won platform knowledge.
- **Don't cross-contaminate voices.** 公众号 formality in a 小红书 post feels wrong, and vice versa.
- **Don't pad.** Shorter and tighter beats longer and rambling, especially on 抖音/小红书.
- **Don't forget the CTA.** Every piece should ask the reader to do something.
