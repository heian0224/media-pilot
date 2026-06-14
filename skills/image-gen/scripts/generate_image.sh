#!/bin/bash
# Image generation script for GPT-Image-2
# Usage: ./generate_image.sh "prompt" "size" "quality" "output"
# Example: ./generate_image.sh "A cat wearing a hat" "1024x1024" "high" "cat.png"

set -e

# Parameters
PROMPT="$1"
SIZE="${2:-1024x1024}"      # 1024x1024, 1024x1536, 1536x1024, 2048x2048
QUALITY="${3:-medium}"       # low, medium, high, auto
OUTPUT="${4:-output.png}"

# Validate inputs
if [ -z "$PROMPT" ]; then
  echo "Error: Prompt is required"
  echo "Usage: $0 \"prompt\" [size] [quality] [output]"
  echo "Example: $0 \"A cat wearing a hat\" \"1024x1024\" \"high\" \"cat.png\""
  exit 1
fi

# Read from environment
ENDPOINT="${GPT_IMAGE_ENDPOINT:-https://api.openai.com/v1/images/generations}"
API_KEY="${GPT_IMAGE_API_KEY}"

if [ -z "$API_KEY" ]; then
  echo "Error: GPT_IMAGE_API_KEY environment variable not set"
  echo "Please set it with: export GPT_IMAGE_API_KEY=\"your-key-here\""
  exit 1
fi

echo "Generating image with GPT-Image-2..."
echo "Endpoint: $ENDPOINT"
echo "Size: $SIZE, Quality: $QUALITY"
echo "Prompt: $PROMPT"

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

# Check for errors in response
if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
  echo "Error from API:"
  echo "$response" | jq '.'
  exit 1
fi

# Extract base64 image data and decode
image_data=$(echo "$response" | jq -r '.data[0].b64_json')

if [ "$image_data" = "null" ] || [ -z "$image_data" ]; then
  echo "Error: Could not extract image data from response:"
  echo "$response" | jq '.'
  exit 1
fi

# Decode and save
echo "$image_data" | base64 -d > "$OUTPUT"

echo "✓ Image saved to: $OUTPUT"
echo "✓ File size: $(du -h "$OUTPUT" | cut -f1)"