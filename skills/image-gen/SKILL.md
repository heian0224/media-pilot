---
name: image-gen
description: "Generate images using GPT-Image-2 API. Use this when you need to create visual content for self-media posts, covers, or illustrations. This skill supports custom API endpoints for third-party providers. Requires GPT_IMAGE_API_KEY and GPT_IMAGE_ENDPOINT environment variables."
---

# Image Generation with GPT-Image-2

Generate high-quality images using OpenAI's GPT-Image-2 model or compatible third-party APIs. This skill handles text-to-image generation with configurable aspect ratios, quality levels, and output formats.

## When to Use

- Creating cover images for WeChat articles (16:9)
- Generating vertical images for Xiaohongshu posts (3:4)
- Producing thumbnails for Douyin/Bilibili videos
- Creating visual assets for self-media content
- Any time the user asks for image generation

## Prerequisites

Before using this skill, ensure environment variables are set:

```bash
# Required: API endpoint URL (default: OpenAI official, or third-party provider)
export GPT_IMAGE_ENDPOINT="https://api.openai.com/v1/images/generations"

# Required: API key for the image generation service
export GPT_IMAGE_API_KEY="your-api-key-here"

# Optional: Custom provider name (for logging/compatibility tweaks)
export GPT_IMAGE_PROVIDER="openai"  # or "atlas", "evolink", etc.
```

For third-party providers, set `GPT_IMAGE_ENDPOINT` to their compatible endpoint:

```bash
# Example: Atlas Cloud
export GPT_IMAGE_ENDPOINT="https://api.atlascloud.ai/v1/images/generations"
export GPT_IMAGE_API_KEY="your-atlas-cloud-key"

# Example: EvoLink
export GPT_IMAGE_ENDPOINT="https://api.evolink.ai/v1/images/generations"
export GPT_IMAGE_API_KEY="your-evolink-key"
```

## Process

### 1. Determine image requirements

Confirm with the user:
- **Purpose**: Cover image, illustration, product photo, etc.
- **Platform**: WeChat (16:9), Xiaohongshu (3:4), general use
- **Style**: Photorealistic, illustration, diagram, 3D render, etc.
- **Text content**: Any Chinese text that needs to be overlaid (GPT-Image-2 renders CJK well, but manual overlay is safer for critical text)

### 2. Generate the image

#### Using curl (direct API call)

```bash
#!/bin/bash
# Image generation script for GPT-Image-2
# Usage: ./generate_image.sh "prompt" "1024x1024" "high" "output.png"

PROMPT="$1"
SIZE="${2:-1024x1024}"      # 1024x1024, 1024x1536, 1536x1024, 2048x2048
QUALITY="${3:-medium}"       # low, medium, high, auto
OUTPUT="$4"

# Read from environment
ENDPOINT="${GPT_IMAGE_ENDPOINT:-https://api.openai.com/v1/images/generations}"
API_KEY="${GPT_IMAGE_API_KEY}"

if [ -z "$API_KEY" ]; then
  echo "Error: GPT_IMAGE_API_KEY environment variable not set"
  exit 1
fi

# Make API request
response=$(curl -s -X POST "$ENDPOINT" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"gpt-image-2\",
    \"prompt\": \"$(echo "$PROMPT" | sed 's/"/\\"/g')\",
    \"n\": 1,
    \"size\": \"$SIZE\",
    \"quality\": \"$QUALITY\"
  }")

# Extract base64 image data and decode
image_data=$(echo "$response" | jq -r '.data[0].b64_json')

if [ "$image_data" = "null" ]; then
  echo "Error generating image:"
  echo "$response" | jq '.'
  exit 1
fi

echo "$image_data" | base64 -d > "$OUTPUT"
echo "Image saved to: $OUTPUT"
```

#### Using Python (with polling for async providers)

```python
#!/usr/bin/env python3
import os
import requests
import base64
import time
from pathlib import Path

def generate_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "medium",
    output_path: str = "output.png",
    endpoint: str = None,
    api_key: str = None
):
    """Generate an image using GPT-Image-2 API."""
    
    endpoint = endpoint or os.environ.get("GPT_IMAGE_ENDPOINT", "https://api.openai.com/v1/images/generations")
    api_key = api_key or os.environ.get("GPT_IMAGE_API_KEY")
    
    if not api_key:
        raise ValueError("GPT_IMAGE_API_KEY environment variable not set")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-image-2",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality
    }
    
    response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    
    # Handle async providers (task_id polling)
    if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
        if "task_id" in data["data"][0]:
            # Async mode - poll for completion
            task_id = data["data"][0]["task_id"]
            print(f"Task submitted: {task_id}, polling for completion...")
            
            while True:
                time.sleep(2)
                status_response = requests.get(
                    f"{endpoint}/tasks/{task_id}",
                    headers=headers,
                    timeout=30
                )
                status_response.raise_for_status()
                status_data = status_response.json()
                
                if status_data.get("data", {}).get("status") == "completed":
                    image_data = status_data["data"]["result"]["data"][0]["b64_json"]
                    break
                elif status_data.get("data", {}).get("status") in ["failed", "error"]:
                    raise Exception(f"Task failed: {status_data}")
                print(f"Status: {status_data.get('data', {}).get('status')}")
        else:
            # Sync mode - direct response
            image_data = data["data"][0]["b64_json"]
    else:
        raise Exception(f"Unexpected response format: {data}")
    
    # Decode and save
    image_bytes = base64.b64decode(image_data)
    Path(output_path).write_bytes(image_bytes)
    print(f"Image saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 generate_image.py \"prompt\" [size] [quality] [output]")
        sys.exit(1)
    
    generate_image(
        prompt=sys.argv[1],
        size=sys.argv[2] if len(sys.argv) > 2 else "1024x1024",
        quality=sys.argv[3] if len(sys.argv) > 3 else "medium",
        output_path=sys.argv[4] if len(sys.argv) > 4 else "output.png"
    )
```

### 3. Platform-specific sizing

| Platform | Aspect Ratio | Recommended Size |
|----------|-------------|------------------|
| WeChat (公众号) | 16:9 | 1536x1024, 1920x1080 |
| Xiaohongshu (小红书) | 3:4 | 1024x1536, 1536x2048 |
| Douyin (抖音) | 16:9 (video) | 1920x1080 |
| Bilibili (B站) | 16:9 (video) | 1920x1080 |
| General square | 1:1 | 1024x1024, 2048x2048 |

### 4. Text rendering (CRITICAL — read before writing any prompt)

GPT-Image-2 renders **both Chinese and Latin text at ~99% accuracy** (CJK is strong) and is excellent at people, icons, and composition. For a self-media image the goal is: **the image is the finished asset, in Chinese — not an empty canvas to overlay later.** So write the actual Chinese strings into the prompt and let the model render them.

| Element | What to do | Example |
|---------|-----------|---------|
| Titles, headlines, section labels | **Write the Chinese directly in the prompt** | 标题写「循环工程」、副标「不再一句句下指令」 |
| UI labels, button text, list items | **Write the Chinese directly** | 「自动化」「工作树」「技能」「连接器」「子代理」 |
| Short Chinese 金句 / callouts | **Write the Chinese directly** | 「决策者在循环内部」 |
| Numbers, badges, version tags | **Render directly** | 「150万浏览」「2026.6」「1 2 3 4」 |
| Proper nouns (Western names, brand/company) | **Keep in original Latin form** — recognizable & renders cleanly | `Boris Cherny`、`Anthropic`、`GitHub`、`Loop Engineering` |
| Icons, people, layout | **Describe each explicitly** with color/position — never `"icon placeholder"` | 三张卡片并排，每张左上一个发光圆形头像图标… |
| Only very long Chinese prose (>1 sentence) | Rarely needed; if so, render a short Chinese title + reserve a band for the body | 居中留出一条横幅区域用于叠加长文案 |

**Two rules that matter most:**

1. **中文优先。** The image is read by a Chinese audience on Chinese platforms — titles, labels, and callouts should be **Chinese strings baked into the image**, not English. Keep only Western proper nouns in Latin. A cover that reads "Loop Engineering" in English is wrong for 公众号/小红书 — it should read「循环工程」.
2. **No skeleton.** Never write `placeholder` / `label` / `no text`. Describe real content and let the model draw it.

**Self-check before sending:** open the generated image — are the Chinese title and labels actually rendered and legible? If it's an English-only or empty diagram, the prompt failed; rewrite it with Chinese strings.

## CRITICAL: Prompt Authoring Rules

Two costly mistakes, both fixed here:

**(a) The skeleton mistake** — copying a "background scaffold" prompt (designed for a tool where all text is overlaid by hand) into GPT-Image-2. That prompt produces an *empty* canvas; GPT-Image-2 honors it and draws nothing.

**(b) The English-everywhere mistake** — writing every label in English so the image comes out English-only, useless on Chinese platforms without re-doing the whole thing.

Rules:

1. **Write Chinese strings into the prompt.** Titles, labels, list items, short quotes — use the actual Chinese the image must display: 「循环工程」「记忆」「这活儿每周以上重复」. Let the model render them (CJK accuracy is high).
2. **Keep Western proper nouns in Latin.** Names like `Boris Cherny`, companies like `Anthropic`/`GitHub`, the coinage `Loop Engineering` — leave in English for recognizability. Everything else → Chinese.
3. **Name real entities, never placeholders.** Real names, real labels, real numbers. Never `"name label"` or `"quote placeholder"`.
4. **Describe every visual element explicitly** — each card, node, icon, arrow, badge, color, position. Vague → empty.
5. **Pin a consistent style** (palette, line weight, mood) so a set looks cohesive — follow the brand's visual identity (`brand.md`).
6. **Match the platform's aspect ratio.** WeChat 16:9, Xiaohongshu 3:4.

**Prompt language:** You can mix Chinese and English in the prompt itself — describe layout/structure in whichever language is clearest, but **the text the image must show is Chinese (proper nouns in Latin).** Example: "三张并排的卡片，每张顶部写英文名 `Boris Cherny`，下方写中文公司「Anthropic」和一句中文金句".

**See the appendix at the end of this file for a side-by-side bad-vs-good example.**

## Common Image Prompts by Style

### Photorealistic product photography
```
A premium product photo of [PRODUCT] on a marble counter, soft window light, 
clean ecommerce composition, shallow depth of field, professional studio lighting
```

### Tech illustration style
```
Modern isometric illustration of [SUBJECT], clean 3D render, soft ambient occlusion, 
minimalist color palette with cyan and magenta accents, white background
```

### Infographic/diagram style
```
Clean technical diagram showing [CONCEPT], flat design, bold typography, 
organized layout with clear visual hierarchy, professional color scheme
```

### Social media cover style
```
Eye-catching social media cover about [TOPIC], bold headline typography, 
vibrant gradient background with geometric shapes, modern aesthetic, 
high contrast, designed for mobile screens
```

## Saving and Organizing

Save generated images in the content directory alongside other assets:

```
content/<YYYY-MM-DD-topic-slug>/
├── wechat.md
├── wechat-images.md
├── wechat-cover.png          # ← Generated here
├── xiaohongshu.md
├── xiaohongshu-images.md
├── xiaohongshu-1.png         # ← Generated here
├── xiaohongshu-2.png
└── ...
```

Use descriptive filenames that indicate platform and purpose:
- `wechat-cover.png` - WeChat article cover
- `xiaohongshu-01-cover.png` - Xiaohongshu first image (cover)
- `xiaohongshu-02-diagram.png` - Xiaohongshu second image (diagram)
- `douyin-thumbnail.png` - Douyin video thumbnail

## Quality Checks

Before delivering generated images, verify:
- [ ] Resolution matches platform requirements
- [ ] Text is legible (if rendered by AI)
- [ ] Subject is clear and not cropped awkwardly
- [ ] Colors are appropriate for brand/content
- [ ] No artifacts, distortion, or weird AI glitches
- [ ] File size is reasonable (< 5MB for most platforms)

## Troubleshooting

### API Errors

**401 Unauthorized**
- Check that `GPT_IMAGE_API_KEY` is set correctly
- Verify the key is valid for the provider

**400 Bad Request**
- Check that size dimensions are multiples of 16
- Verify prompt length (max ~4000 chars)
- Ensure quality value is valid: `low`, `medium`, `high`, `auto`

**429 Rate Limit**
- Implement exponential backoff
- Check provider's rate limits
- Consider upgrading API tier

### Image Quality Issues

**Text is garbled**
- Try higher quality setting: `quality: "high"`
- Generate background only, overlay text manually
- Simplify prompt text

**Composition issues**
- Be more specific about camera angle and framing
- Add composition keywords: "centered", "rule of thirds", "wide angle"
- Specify background clearly

**Style mismatch**
- Add style descriptors: "photorealistic", "3D render", "flat illustration"
- Reference specific styles: "in the style of minimal tech diagrams"
- Specify lighting: "soft studio lighting", "dramatic side lighting"

## Integration with Content Pipeline

This skill integrates with the `platform-writing` skill:

1. After generating platform copy (wechat.md, xiaohongshu.md)
2. Platform-writing produces 配图 prompt docs (wechat-images.md, xiaohongshu-images.md)
3. Use this skill to generate images based on those prompts
4. Save images alongside the content files
5. User manually uploads images to platforms

## Rate Limiting and Cost Management

GPT-Image-2 generation costs vary by provider:
- OpenAI official: ~$0.01–$0.04 per image (depending on size/quality)
- Third-party providers: Often 20–80% cheaper

To manage costs:
- Generate multiple images in one request when possible: `n: 4`
- Use lower quality for drafts: `quality: "low"` or `medium`
- Cache generated images and reuse across platforms
- Batch generation requests to reduce overhead

## Anti-Patterns

- **Don't** generate images without confirming platform requirements first
- **Don't** use this skill for logo design (iteration is expensive)
- **Don't** forget to set environment variables—API calls will fail silently
- **Don't** assume all providers support the same parameters (check docs)
- **Don't** render critical Chinese text without verification—manual overlay is safer
- **Don't** copy a "scaffold" prompt (full of `placeholder`/`no text`) verbatim into GPT-Image-2 — it draws an empty diagram. Rewrite it rich (see appendix).
- **Don't** write `no text` globally — that nukes English names/labels the model would otherwise render perfectly. Only reserve Chinese long-form copy.

## Appendix: Bad vs Good Prompt (side-by-side)

**Scenario:** a card showing three people's quotes about Loop Engineering, for a 公众号 article.

❌ **BAD — skeleton prompt** (image comes back empty: blank circles, no names, no badge):
```
Three clean speech-bubble cards side by side on dark background, each with a
circular avatar placeholder, a name label, and a short quote; one card has a
small red badge "1.5M views"; cyan accents, flat design, no text
```
Why it fails: every element is a `placeholder`, and it ends with `no text`.

❌ **ALSO BAD — English-everywhere prompt** (image comes out English-only, useless for Chinese platforms without re-doing it):
```
Three cards side by side, each with a name "Boris Cherny"/"Anthropic", a label
"Automations"/"Memory", title "Loop Engineering", subtitle "Build a loop"...
```
Why it fails: Chinese audience can't use an English-only cover on 公众号/小红书.

✅ **GOOD — Chinese-first, content-rich prompt** (Chinese labels baked in, proper nouns in Latin):
```
三张并排的对话气泡卡片，深蓝到紫色渐变背景，带细网格纹理。
卡片1：左侧一个青色发光的圆形头像图标，上方英文名 Boris Cherny，下方中文公司「Anthropic」，
气泡里写中文金句「我已经不写提示词了，我的工作是写循环」。
卡片2：品红色发光头像，英文名 Peter Steinberger，中文「OpenClaw」，右上角贴一个红色发光角标
「150万浏览」，气泡金句「别再给 Agent 写 prompt，去设计驱动 Agent 的循环」。
卡片3：黄绿色发光头像，英文名 Addy Osmani，中文「Google」，气泡金句「把下指令的人，换成你设计的系统」。
青色与品红霓虹高亮，扁平发光描边，演讲幻灯片风格。
```
Why it works: the Chinese 金句 and 公司名 are rendered directly (CJK accuracy is high), Western names stay in Latin for recognizability, the badge 「150万浏览」 is explicit, and every card's structure is spelled out. The image is the finished asset — no manual overlay needed.