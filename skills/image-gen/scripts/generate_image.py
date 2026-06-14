#!/usr/bin/env python3
"""
Image generation script for GPT-Image-2
Supports both sync and async API providers with polling

Usage:
  python3 generate_image.py "A cat wearing a hat" --size 1024x1024 --quality high --output cat.png
  python3 generate_image.py "Product photo" --size 1536x1024 --quality medium --output cover.png
"""

import os
import sys
import argparse
import base64
import time
import requests
from pathlib import Path
from typing import Optional


def generate_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "medium",
    output_path: str = "output.png",
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 60
) -> str:
    """Generate an image using GPT-Image-2 API."""

    # Read from environment or parameters
    endpoint = endpoint or os.environ.get("GPT_IMAGE_ENDPOINT", "https://api.openai.com/v1/images/generations")
    api_key = api_key or os.environ.get("GPT_IMAGE_API_KEY")

    if not api_key:
        raise ValueError(
            "GPT_IMAGE_API_KEY environment variable not set. "
            "Please set it with: export GPT_IMAGE_API_KEY=\"your-key-here\""
        )

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

    print(f"Generating image with GPT-Image-2...")
    print(f"Endpoint: {endpoint}")
    print(f"Size: {size}, Quality: {quality}")
    print(f"Prompt: {prompt}")

    try:
        # Make initial request
        response = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        # Check for API errors
        if "error" in data:
            error_msg = data.get("error", {}).get("message", "Unknown error")
            raise Exception(f"API Error: {error_msg}")

        image_data = None

        # Handle different response formats
        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            first_item = data["data"][0]

            # Async mode (task_id polling)
            if "task_id" in first_item:
                task_id = first_item["task_id"]
                print(f"✓ Task submitted: {task_id}")
                print(f"  Polling for completion...")

                max_polls = 60  # 2 minutes max
                poll_count = 0

                while poll_count < max_polls:
                    time.sleep(2)
                    poll_count += 1

                    # Try different polling endpoint formats
                    poll_endpoints = [
                        f"{endpoint}/tasks/{task_id}",
                        f"{endpoint}/results/{task_id}",
                        f"{endpoint.replace('/generations', f'/tasks/{task_id}')}",
                    ]

                    for poll_endpoint in poll_endpoints:
                        try:
                            status_response = requests.get(poll_endpoint, headers=headers, timeout=30)
                            if status_response.status_code == 200:
                                status_data = status_response.json()
                                status = status_data.get("data", {}).get("status") or status_data.get("status")

                                if status == "completed":
                                    # Extract image from completed task
                                    result_data = status_data.get("data", {}).get("result", status_data)
                                    if "data" in result_data and len(result_data["data"]) > 0:
                                        image_data = result_data["data"][0].get("b64_json")
                                        if image_data:
                                            break
                                elif status in ["failed", "error"]:
                                    error_msg = status_data.get("data", {}).get("error", "Task failed")
                                    raise Exception(f"Task failed: {error_msg}")
                                else:
                                    print(f"  Status: {status or 'processing'}")
                                    if poll_count % 10 == 0:
                                        print(f"  Still waiting... ({poll_count * 2}s)")
                            break
                        except requests.RequestException:
                            continue

                    if image_data:
                        break

                if not image_data and poll_count >= max_polls:
                    raise Exception(f"Task timed out after {max_polls * 2} seconds")

            # Sync mode - direct response with b64_json
            elif "b64_json" in first_item:
                image_data = first_item["b64_json"]

            # Sync mode - URL response (less common for GPT-Image-2)
            elif "url" in first_item:
                image_url = first_item["url"]
                print(f"  Downloading from URL...")
                img_response = requests.get(image_url, timeout=30)
                img_response.raise_for_status()
                Path(output_path).write_bytes(img_response.content)
                print(f"✓ Image saved to: {output_path}")
                return output_path
            else:
                raise Exception(f"Unexpected response format: {first_item.keys()}")
        else:
            raise Exception(f"Unexpected API response: {data}")

        if not image_data:
            raise Exception("No image data found in response")

        # Decode and save
        image_bytes = base64.b64decode(image_data)
        Path(output_path).write_bytes(image_bytes)

        print(f"✓ Image saved to: {output_path}")
        print(f"✓ File size: {len(image_bytes) / 1024:.1f} KB")
        return output_path

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except Exception as e:
        raise Exception(f"Image generation failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate images using GPT-Image-2 API")
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument("--size", default="1024x1024",
                       help="Image size (default: 1024x1024). Options: 1024x1024, 1024x1536, 1536x1024, 2048x2048")
    parser.add_argument("--quality", default="medium",
                       choices=["low", "medium", "high", "auto"],
                       help="Image quality (default: medium)")
    parser.add_argument("--output", default="output.png",
                       help="Output file path (default: output.png)")
    parser.add_argument("--endpoint",
                       help="API endpoint (default: GPT_IMAGE_ENDPOINT env var or https://api.openai.com/v1/images/generations)")
    parser.add_argument("--api-key",
                       help="API key (default: GPT_IMAGE_API_KEY env var)")
    parser.add_argument("--timeout", type=int, default=60,
                       help="Request timeout in seconds (default: 60)")

    args = parser.parse_args()

    try:
        generate_image(
            prompt=args.prompt,
            size=args.size,
            quality=args.quality,
            output_path=args.output,
            endpoint=args.endpoint,
            api_key=args.api_key,
            timeout=args.timeout
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()