#!/usr/bin/env bash
# Reusable MiniMax TTS for HyperFrames videos.
# Reads narration segments (one per line) from a scenes file, calls MiniMax
# speech-2.8-hd for each, writes sceneN.mp3 + manifest.json.
#
# Usage:
#   bash minimax_tts.sh --out <audio-dir> --scenes <scenes.txt> [--voice <id>] [--speed <num>]
#   scenes.txt: one narration segment per line (blank lines skipped). One line = one scene.
#
# Requires: MINIMAX_API_KEY env var, curl, ffprobe, python3.
# MiniMax must be reached DIRECT with --http1.1 (proxies cause TLS errors) — proxy vars are unset.
set -uo pipefail
unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY NO_PROXY

KEY="${MINIMAX_API_KEY:?MINIMAX_API_KEY not set}"
URL="https://api.minimaxi.com/v1/t2a_v2"
VOICE="male-qn-qingse"
SPEED="1.3"
OUT=""
SCENES=""

while [ $# -gt 0 ]; do
  case "$1" in
    --out) OUT="$2"; shift 2;;
    --scenes) SCENES="$2"; shift 2;;
    --voice) VOICE="$2"; shift 2;;
    --speed) SPEED="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

[ -n "$OUT" ] || { echo "--out <dir> required" >&2; exit 2; }
[ -n "$SCENES" ] || { echo "--scenes <file> required" >&2; exit 2; }
[ -f "$SCENES" ] || { echo "scenes file not found: $SCENES" >&2; exit 2; }

mkdir -p "$OUT"
: > "$OUT/manifest.jsonl"

i=0
while IFS= read -r line || [ -n "$line" ]; do
  # skip blank lines
  [ -z "${line// /}" ] && continue
  i=$((i+1))
  name="scene${i}"
  echo "[$name] generating…"

  payload=$(python3 -c '
import json, sys
print(json.dumps({
  "model": "speech-2.8-hd", "text": sys.argv[1], "stream": False,
  "voice_setting": {"voice_id": sys.argv[2], "speed": float(sys.argv[3]), "vol": 1, "pitch": 0},
  "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
}, ensure_ascii=False))' "$line" "$VOICE" "$SPEED")

  resp="$OUT/$name.resp.json"
  if ! curl -sS -m 90 --http1.1 -X POST "$URL" \
        -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
        --data "$payload" -o "$resp"; then
    echo "  curl FAILED for $name" >&2; exit 1
  fi

  mp3="$OUT/$name.mp3"
  python3 - "$resp" "$mp3" "$name" "$line" <<'PY'
import json, sys, pathlib
rj = json.load(open(sys.argv[1], encoding="utf-8"))
br = rj.get("base_resp", {})
if br.get("status_code", -1) != 0:
    sys.exit("API ERROR: " + str(br))
hexa = (rj.get("data") or {}).get("audio")
if not hexa:
    sys.exit("no audio: " + json.dumps(rj, ensure_ascii=False)[:300])
pathlib.Path(sys.argv[2]).write_bytes(bytes.fromhex(hexa))
print(f"  decoded {len(hexa)//2} bytes -> {sys.argv[3]}.mp3")
PY

  dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$mp3")
  kb=$(($(stat -f%z "$mp3") / 1024))
  echo "  ok  ${dur}s  ${kb}KB"

  python3 -c '
import json, sys
print(json.dumps({"scene": sys.argv[1], "file": sys.argv[2],
                  "duration": float(sys.argv[3]), "text": sys.argv[4]}, ensure_ascii=False))' \
    "$name" "$mp3" "$dur" "$line" >> "$OUT/manifest.jsonl"
done < "$SCENES"

python3 - "$OUT/manifest.jsonl" "$OUT/manifest.json" <<'PY'
import json, sys
lines = [l for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
items = [json.loads(l) for l in lines]
json.dump(items, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
total = sum(x["duration"] for x in items)
print(f"\nDONE — {len(items)} scenes, total {total:.1f}s")
print(f"manifest: {sys.argv[2]}")
PY
