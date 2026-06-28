"""Structured run logging (JSONL) + optional webhook notification."""
from __future__ import annotations

import json

from .. import config


def log_run(record: dict) -> None:
    """Append a JSON-lines record to logs/media-pilot-<TODAY>.jsonl."""
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    path = config.LOG_DIR / f"media-pilot-{config.TODAY}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def notify(text: str) -> None:
    """POST a text payload to NOTIFY_WEBHOOK_URL (if set). Best-effort, never raises."""
    if not config.NOTIFY_WEBHOOK_URL:
        return
    try:
        import requests

        requests.post(config.NOTIFY_WEBHOOK_URL, json={"text": text},
                      timeout=10, proxies={"http": None, "https": None})
    except Exception:
        pass
