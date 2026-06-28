"""Generate 公众号 images via GPT-Image-2, with verify-and-re-roll.

Which images to render = the ``![alt](wechat-<slot>.png)`` references in
content/<slug>/wechat.md (cover always). Prompts come from wechat-images.json.

For each image: generate → ask a vision model to read back the rendered Chinese
→ if any expected term (the 「…」 strings in the prompt) is missing, re-roll, up
to IMAGE_REROLL_ATTEMPTS (default 3). The best candidate (fewest missing terms)
is kept, so the loop only ever helps. Proxies forced off; 8 retries per API call.
"""
from __future__ import annotations

import base64
import json
import re
import time

from langchain_core.tools import tool

from .. import config
from . import image_verify

_NO_PROXY = {"http": None, "https": None}


def _gen_one(prompt: str) -> bytes:
    import requests  # transitively available via cos-python-sdk-v5

    for attempt in range(8):
        try:
            r = requests.post(
                config.GPT_IMAGE_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {config.GPT_IMAGE_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-image-2",
                    "prompt": prompt,
                    "n": 1,
                    "size": "1536x1024",
                    "quality": "medium",
                },
                timeout=150,
                proxies=_NO_PROXY,
            )
            if r.status_code >= 500:
                raise RuntimeError(f"HTTP {r.status_code}")
            r.raise_for_status()
            item = r.json().get("data", [{}])[0]
            if "b64_json" in item:
                return base64.b64decode(item["b64_json"])
            raise RuntimeError("no b64_json in response")
        except Exception:
            if attempt == 7:
                raise
            time.sleep(8 + attempt * 6)


def _slot_order(slot: str) -> tuple:
    if slot == "cover":
        return (0, 0)
    m = re.fullmatch(r"part(\d+)", slot)
    if m:
        return (1, int(m.group(1)))
    return (2, slot)


@tool
def generate_images(slug: str) -> str:
    """Generate 公众号 images for content/<slug>/ (cover + every wechat-partN.png
    referenced in wechat.md). Each image is verified by a vision model reading back
    its Chinese text; if expected terms are missing it is re-rolled up to 3 times,
    keeping the best attempt. Returns a summary: generated / re-rolled / failed."""
    if not config.GPT_IMAGE_API_KEY:
        return "FAIL: GPT_IMAGE_API_KEY not set"
    base = config.MEDIA_CONTENT_DIR / slug
    md_path = base / "wechat.md"
    if not md_path.is_file():
        return f"FAIL: {md_path} not found"

    md = md_path.read_text(encoding="utf-8")
    referenced = set(re.findall(r"!\[[^\]]*\]\(wechat-([a-z0-9]+)\.png\)", md))
    needed = sorted({"cover"} | referenced, key=_slot_order)

    prompts: dict[str, str] = {}
    jobs_path = base / "wechat-images.json"
    if jobs_path.is_file():
        try:
            for j in json.loads(jobs_path.read_text(encoding="utf-8")):
                prompts[j.get("slot")] = j.get("prompt", "")
        except json.JSONDecodeError:
            pass

    written, no_prompt, failed, rerolled = [], [], [], []
    for slot in needed:
        prompt = prompts.get(slot)
        if not prompt:
            no_prompt.append(slot)
            continue
        expected = image_verify.extract_expected_terms(prompt)
        best = None  # (bytes, missing_count, passed, attempts_used)
        gen_failed = False
        for attempt in range(config.IMAGE_REROLL_ATTEMPTS):
            try:
                img = _gen_one(prompt)
            except Exception as e:
                failed.append(f"{slot}(gen:{type(e).__name__})")
                gen_failed = True
                break
            try:
                ok, missing, _ = image_verify.verify(img, expected)
            except Exception:
                # verifier flaked — accept this attempt, don't block the pipeline
                ok, missing = True, []
            miss_n = len(missing)
            if best is None or miss_n < best[1]:
                best = (img, miss_n, ok, attempt + 1)
            if ok:
                break
        if gen_failed or best is None:
            continue
        (base / f"wechat-{slot}.png").write_bytes(best[0])
        written.append(slot)
        if best[3] > 1 or not best[2]:
            tag = f"{slot}×{best[3]}"
            if best[1]:
                tag += f"({best[1]} term(s) still off)"
            rerolled.append(tag)

    msg = f"generated {len(written)}: {', '.join(written)}"
    if rerolled:
        msg += f" | re-rolled: {', '.join(rerolled)}"
    if no_prompt:
        msg += f" | no prompt (skipped): {', '.join(no_prompt)}"
    if failed:
        msg += f" | FAILED: {', '.join(failed)}"
    return msg
