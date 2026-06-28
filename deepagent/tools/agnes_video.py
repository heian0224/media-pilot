"""Agnes video generation tool (agnes-video-v2.0): text-to-video or image-to-video
real-footage b-roll clips. Async submit → poll → download mp4.

NOTE: the Agnes /v1/videos endpoint has been intermittently overloaded (free-period
$0/sec). The tool returns a clear FAIL on timeout so the caller can fall back to
HyperFrames. Proxies forced off (system proxy breaks this provider's TLS)."""
from __future__ import annotations

import time
from pathlib import Path

from langchain_core.tools import tool

from .. import config

_NO_PROXY = {"http": None, "https": None}


@tool
def generate_video_clip(
    prompt: str,
    out_path: str,
    num_frames: int = 121,
    frame_rate: int = 24,
    image: str = "",
    submit_timeout: int = 180,
    poll_timeout: int = 600,
) -> str:
    """Generate a short video clip via Agnes agnes-video-v2.0 — text-to-video, or
    image-to-video if an image URL is given. num_frames must follow 8n+1 (81/121/241/441).
    Async: submits, polls until ready, downloads mp4 to out_path. Takes minutes per
    clip. Returns 'OK: <path>' or 'FAIL: ...' (if the endpoint is overloaded, retry
    later or use the HyperFrames path instead)."""
    if not config.AGNES_API_KEY:
        return "FAIL: AGNES_API_KEY not set"
    import requests

    H = {"Authorization": f"Bearer {config.AGNES_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "agnes-video-v2.0", "prompt": prompt,
               "num_frames": num_frames, "frame_rate": frame_rate}
    if image:
        payload["image"] = image

    resp = None
    for a in range(3):
        try:
            r = requests.post(f"{config.AGNES_BASE_URL}/v1/videos", headers=H, json=payload,
                              timeout=submit_timeout, proxies=_NO_PROXY)
            r.raise_for_status()
            resp = r.json()
            break
        except Exception as e:
            if a == 2:
                return (f"FAIL submit ({type(e).__name__}: {str(e)[:120]}) — Agnes video "
                        "endpoint may be overloaded; retry later or use HyperFrames.")
            time.sleep(6 + a * 4)

    vid = (resp or {}).get("video_id") or (resp or {}).get("task_id")
    if not vid:
        return f"FAIL: no video_id in response: {str(resp)[:200]}"

    # already done synchronously?
    url = (resp.get("remixed_from_video_id")
           or (resp.get("data") or {}).get("url") if isinstance(resp.get("data"), dict) else None)
    if not url:
        deadline = time.time() + poll_timeout
        last: dict = {}
        while time.time() < deadline:
            time.sleep(8)
            try:
                last = requests.get(f"{config.AGNES_BASE_URL}/agnesapi",
                                    params={"video_id": vid, "model_name": "agnes-video-v2.0"},
                                    headers=H, timeout=60, proxies=_NO_PROXY).json()
            except Exception:
                continue
            if str(last.get("status", "")).lower() in ("completed", "succeeded", "success", "failed", "error"):
                break
        url = (last.get("remixed_from_video_id")
               or (last.get("data") or {}).get("url") if isinstance(last.get("data"), dict) else None
               or last.get("url"))
        if str(last.get("status", "")).lower() in ("failed", "error") or not url:
            return f"FAIL: status={last.get('status')} no url. {str(last)[:300]}"

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(requests.get(url, timeout=300, proxies=_NO_PROXY).content)
    return f"OK: {out}"
