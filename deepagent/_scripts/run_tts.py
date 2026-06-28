#!/usr/bin/env python3
"""Reusable MiniMax TTS runner: 场景文件（每行一段）→ sceneN.mp3 + manifest.json.

用法:
  .venv/bin/python scripts/run_tts.py --scenes <dir>/bili-scenes.txt --out <dir>/bili-audio
  .venv/bin/python scripts/run_tts.py --scenes <dir>/douyin-scenes.txt --out <dir>/audio

直连 curl --http1.1（这个组合在本网络最稳）。voice male-qn-qingse, speed 1.3。
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time

KEY = os.environ.get("MINIMAX_API_KEY")
if not KEY:
    sys.exit("MINIMAX_API_KEY 未设置")
URL = "https://api.minimaxi.com/v1/t2a_v2"


def curl_json(url, payload=None, method="GET", timeout=120):
    if method == "GET" and payload is not None:
        method = "POST"  # 带 body 必须是 POST，否则 MiniMax 返回 404
    cmd = ["curl", "-sS", "-m", str(timeout), "--http1.1", "-X", method, url,
           "-H", f"Authorization: Bearer {KEY}", "-H", "Content-Type: application/json"]
    pf = None
    if payload is not None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
            pf = f.name
        cmd += ["--data", f"@{pf}"]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 10)
    finally:
        if pf:
            os.unlink(pf)
    if r.returncode != 0:
        raise RuntimeError(f"curl rc={r.returncode}: {r.stderr.decode('utf-8','replace')[:300]}")
    raw = r.stdout.decode("utf-8", "replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON parse fail ({e}); raw[:200]={raw[:200]!r}")


def tts(text, voice, speed):
    return curl_json(URL, {
        "model": "speech-2.8-hd", "text": text, "stream": False,
        "voice_setting": {"voice_id": voice, "speed": speed, "vol": 1, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    })


def save_audio(rj, path):
    data = rj.get("data") or {}
    if data.get("audio"):
        path.write_bytes(bytes.fromhex(data["audio"]))
        return "hex"
    url = data.get("audio_url") or rj.get("download_url")
    if url:
        subprocess.run(["curl", "-sS", "-m", "120", "--http1.1", "-o", str(path), url],
                       check=True, timeout=130)
        return "url"
    raise RuntimeError(f"no audio: {json.dumps(rj, ensure_ascii=False)[:400]}")


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def main():
    ap = argparse.ArgumentParser(description="MiniMax TTS: 场景文件 → mp3 + manifest")
    ap.add_argument("--scenes", required=True, help="场景文件，每行一段口播（空行跳过）")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--voice", default="male-qn-qingse")
    ap.add_argument("--speed", type=float, default=1.3)
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    scenes = [ln.strip() for ln in pathlib.Path(args.scenes).read_text(encoding="utf-8").splitlines() if ln.strip()]

    manifest = []
    for i, text in enumerate(scenes, 1):
        name = f"scene{i}"
        print(f"[{name}] ({len(text)}字) generating…", flush=True)
        for attempt in range(4):
            try:
                rj = tts(text, args.voice, args.speed)
                break
            except Exception as e:
                print(f"   retry {attempt+1}/4: {e}", flush=True)
                if attempt == 3:
                    sys.exit(f"  ERROR [{name}]: {e}")
                time.sleep(4)
        if rj.get("base_resp", {}).get("status_code", -1) != 0:
            sys.exit(f"  API ERROR [{name}]: {rj.get('base_resp')}")
        path = out / f"{name}.mp3"
        mode = save_audio(rj, path)
        dur = duration(path)
        manifest.append({"scene": name, "file": str(path), "duration": round(dur, 3), "text": text})
        print(f"   ok ({mode}) {dur:.2f}s  {path.stat().st_size//1024} KB", flush=True)

    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    total = sum(m["duration"] for m in manifest)
    print(f"\nDONE — {len(manifest)} scenes, total {total:.1f}s → {out/'manifest.json'}")


if __name__ == "__main__":
    main()
