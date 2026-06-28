"""Image-text verification: use a vision-capable LLM to read the Chinese text
rendered in a generated image and check it against the strings the prompt asked
for. Powers the generate → verify → re-roll loop in tools/images.py.

Caveat: vision OCR is itself imperfect (may mis-read or "correct" a wrong char),
so this reliably catches GROSS failures (empty / garbled / missing text) and
catches subtle single-char errors sometimes. We keep the best candidate across
attempts regardless, so the loop only ever helps, never hurts."""
from __future__ import annotations

import base64
import re

from openai import OpenAI

from .. import config


def _client() -> OpenAI:
    return OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY)


def extract_expected_terms(prompt: str) -> list[str]:
    """Pull the Chinese text the prompt asked the model to render.

    Scans quoted spans ('…', "…", 「…」) and, from those containing CJK, extracts
    maximal CJK runs of length >= 2. Returning runs (not whole quoted strings)
    makes verification tolerant of Latin tokens / line breaks in the read-back
    while still catching single-char errors (e.g. 玻璃 vs 破晓)."""
    spans = re.findall(r"['\"]([^'\"]+)['\"]", prompt)
    spans += re.findall(r"「([^」]+)」", prompt)
    runs: set[str] = set()
    for s in spans:
        if not re.search(r"[一-鿿]", s):
            continue
        for run in re.findall(r"[一-鿿]{2,}", s):
            runs.add(run)
    return sorted(runs, key=len, reverse=True)


def read_image_text(image_bytes: bytes) -> str:
    """Ask the vision model to read all Chinese text in the image, verbatim."""
    b64 = base64.b64encode(image_bytes).decode()
    resp = _client().chat.completions.create(
        model=config.LLM_VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "逐字读出图中所有中文与数字文字，原样输出，不要纠正或补全。"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                ],
            }
        ],
        max_tokens=300,
        timeout=60,
    )
    return (resp.choices[0].message.content or "").strip()


def verify(image_bytes: bytes, expected_terms: list[str]) -> tuple[bool, list[str], str]:
    """Return (passed, missing_terms, read_text). passed = no expected term missing.
    If there are no expected terms to check, returns passed=True (nothing to verify)."""
    if not expected_terms:
        return True, [], ""
    text = read_image_text(image_bytes)
    missing = [t for t in expected_terms if t not in text]
    return (len(missing) == 0), missing, text
