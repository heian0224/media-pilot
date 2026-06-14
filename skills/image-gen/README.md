# Image Generation Skill

Automated image generation using GPT-Image-2 API for self-media content production.

## Features

- **Multiple API providers**: Works with OpenAI official or third-party providers (Atlas Cloud, EvoLink, etc.)
- **Platform-specific sizing**: Built-in support for WeChat (16:9), Xiaohongshu (3:4), Douyin/Bilibili
- **Flexible quality levels**: low, medium, high, auto
- **Async polling support**: Handles providers with async task queues
- **Batch generation**: Generate multiple images in one request
- **Chinese text rendering**: GPT-Image-2 has excellent CJK support (~99% accuracy)

## Setup

### 1. Configure environment variables

```bash
# Required: API endpoint
export GPT_IMAGE_ENDPOINT="https://api.openai.com/v1/images/generations"

# Required: API key  
export GPT_IMAGE_API_KEY="your-api-key-here"

# Optional: Provider name (for logging/tweaks)
export GPT_IMAGE_PROVIDER="openai"
```

### 2. Third-party provider examples

```bash
# Atlas Cloud (cheaper, ~80% discount)
export GPT_IMAGE_ENDPOINT="https://api.atlascloud.ai/v1/images/generations"
export GPT_IMAGE_API_KEY="your-atlas-cloud-key"
export GPT_IMAGE_PROVIDER="atlas"

# EvoLink
export GPT_IMAGE_ENDPOINT="https://api.evolink.ai/v1/images/generations"
export GPT_IMAGE_API_KEY="your-evolink-key"
export GPT_IMAGE_PROVIDER="evolink"

# Custom provider
export GPT_IMAGE_ENDPOINT="https://your-provider.com/api/v1/images/generations"
export GPT_IMAGE_API_KEY="your-provider-key"
```

Add these to your `~/.zshrc` or `~/.bashrc` to persist across sessions.

### 3. Make scripts executable

```bash
chmod +x scripts/generate_image.sh
chmod +x scripts/generate_image.py
```

## Usage

### Bash script

```bash
# Basic usage
./scripts/generate_image.sh "A cat wearing a hat" "1024x1024" "high" "cat.png"

# WeChat cover (16:9)
./scripts/generate_image.sh "Tech article cover about AI programming, modern minimal style" "1536x1024" "high" "wechat-cover.png"

# Xiaohongshu image (3:4)
./scripts/generate_image.sh "Vertical lifestyle photo of workspace setup, aesthetic lighting" "1024x1536" "medium" "xhs-01.png"

# Square social media
./scripts/generate_image.sh "Minimalist illustration of cloud architecture" "1024x1024" "high" "square.png"
```

### Python script

```bash
# Basic usage
python3 scripts/generate_image.py "A cat wearing a hat" --size 1024x1024 --quality high --output cat.png

# With custom endpoint
python3 scripts/generate_image.py "Product photo" \
  --size 1536x1024 \
  --quality medium \
  --output cover.png \
  --endpoint "https://api.atlascloud.ai/v1/images/generations"

# High-quality vertical image
python3 scripts/generate_image.py "Modern workspace setup" \
  --size 1024x1536 \
  --quality high \
  --output workspace.png
```

### In Claude Code

When working with self-media content, simply ask for image generation:

```
"为这篇公众号文章生成一个封面图"
"帮我生成小红书需要的配图"
"Generate a cover image for the WeChat article about AI programming"
```

The skill will automatically use the appropriate size and style based on the platform.

## Platform-specific guidelines

### WeChat (公众号)
- **Aspect ratio**: 16:9
- **Recommended sizes**: 1536x1024, 1920x1080
- **Style**: Professional, clean, tech-oriented
- **Text**: Generate background, overlay headline manually

### Xiaohongshu (小红书)
- **Aspect ratio**: 3:4 (vertical)
- **Recommended sizes**: 1024x1536, 1536x2048
- **Style**: Aesthetic, lifestyle, vibrant colors
- **Quantity**: 6-9 images per post
- **First image**: Critical for click-through rate

### Douyin (抖音) & Bilibili (B站)
- **Aspect ratio**: 16:9 (horizontal)
- **Recommended sizes**: 1920x1080
- **Style**: Eye-catching, bold, high contrast
- **Purpose**: Video thumbnails

## Common image prompts

### Tech article covers
```
Modern tech article cover about [TOPIC], minimal isometric illustration, 
clean 3D render, cyan and magenta accents, white background, professional style
```

### Lifestyle photography
```
Aesthetic vertical photo of workspace setup, soft natural lighting, 
minimalist decor, shallow depth of field, modern lifestyle photography
```

### Product photography
```
Premium product photo of [PRODUCT], soft window light, clean ecommerce 
composition, marble counter, professional studio lighting
```

### Infographic style
```
Clean technical diagram showing [CONCEPT], flat design, bold typography, 
organized layout, professional color scheme, white background
```

## Cost optimization

GPT-Image-2 generation costs vary by provider:

| Provider | Cost per image | Notes |
|----------|----------------|-------|
| OpenAI official | $0.01–$0.04 | Depends on size/quality |
| Atlas Cloud | ~$0.008 | ~80% discount |
| EvoLink | ~$0.01 | ~60% discount |

**Tips to reduce costs:**

1. **Use lower quality for drafts**: `quality: "low"` or `medium`
2. **Generate multiple images at once**: `n: 4` (when variations are needed)
3. **Reuse across platforms**: Generate once, crop/resize for different platforms
4. **Batch requests**: Group multiple generations to reduce API overhead
5. **Choose cheaper providers**: Third-party providers often offer significant discounts

## Troubleshooting

### Common errors

**`Error: GPT_IMAGE_API_KEY environment variable not set`**
```bash
export GPT_IMAGE_API_KEY="your-key-here"
```

**`400 Bad Request`**
- Check size dimensions are multiples of 16
- Verify prompt length (< 4000 chars)
- Ensure quality is: `low`, `medium`, `high`, or `auto`

**`401 Unauthorized`**
- Verify API key is correct
- Check key hasn't expired
- Ensure key has image generation permissions

**`429 Rate Limit`**
- Implement exponential backoff
- Check provider's rate limits
- Consider upgrading API tier
- Wait before retrying

**Image quality issues**
- Try higher quality: `quality: "high"`
- Be more specific in prompt
- Add style descriptors: "photorealistic", "3D render", "illustration"

### Testing your setup

```bash
# Quick test with default settings
python3 scripts/generate_image.py "A simple red apple on a white table" --output test.png

# Test with custom endpoint
ENDPOINT="https://api.atlascloud.ai/v1/images/generations" \
API_KEY="your-key" \
python3 scripts/generate_image.py "Test image" --output test.png
```

## Integration with content pipeline

This skill integrates seamlessly with the media-pilot content pipeline:

1. **Discovery** → Find trending topics
2. **Strategy** → Plan content angles  
3. **Writing** → Generate platform copy
4. **Image Generation** → Create visual assets (this skill)
5. **Video Production** → Produce video content

Example workflow:
```
User: "帮我为Loop Engineering这篇文章生成公众号封面和小红书的配图"

Skill: 
1. Read wechat.md and xiaohongshu.md to understand content
2. Generate wechat-cover.png (1536x1024, high quality)
3. Generate xiaohongshu-1.png through xiaohongshu-8.png (1024x1536)
4. Save all images in content/2026-06-14-loop-engineer/
5. Report completion with file paths
```

## API compatibility

This skill works with any GPT-Image-2 compatible API:

- ✅ OpenAI official API
- ✅ Atlas Cloud
- ✅ EvoLink
- ✅ NagaAI
- ✅ Most third-party providers

If your provider requires custom request/response handling, modify the scripts accordingly or set the appropriate environment variables.

## File organization

Generated images should be saved alongside content:

```
content/
└── 2026-06-14-loop-engineer/
    ├── wechat.md
    ├── wechat-cover.png          # ← WeChat cover
    ├── xiaohongshu.md
    ├── xiaohongshu-01-cover.png  # ← Xiaohongshu images
    ├── xiaohongshu-02-diagram.png
    ├── xiaohongshu-03-list.png
    └── ...
```

Use descriptive filenames that indicate platform and purpose for easy identification.

## Advanced usage

### Batch generation

```bash
# Generate multiple variations at once
python3 -c "
import os
import sys
sys.path.insert(0, 'scripts')
from generate_image import generate_image

prompts = [
    ('Tech cover 1', 'minimal AI illustration', '1536x1024'),
    ('Tech cover 2', 'modern data center', '1536x1024'),
    ('Tech cover 3', 'abstract neural network', '1536x1024'),
]

for i, (name, prompt, size) in enumerate(prompts):
    try:
        generate_image(prompt, size, 'high', f'cover-{i+1}.png')
    except Exception as e:
        print(f'Failed: {name} - {e}')
"
```

### Custom styles

```bash
# Define style presets
STYLE_PRESETS=(
    "minimal tech, clean 3D render, cyan/magenta accents, white background"
    "photorealistic product shot, soft lighting, marble surface"
    "isometric illustration, flat design, bold colors"
)

# Use in generation
./scripts/generate_image.sh \
  "AI chip architecture, ${STYLE_PRESETS[0]}" \
  "1536x1024" \
  "high" \
  "ai-chip.png"
```

## Support

For issues with:
- **API access**: Check your provider's documentation
- **Image quality**: Review prompts and quality settings
- **Rate limits**: Upgrade API tier or implement backoff
- **Provider-specific**: Contact provider support

For media-pilot integration issues, check the main plugin documentation.