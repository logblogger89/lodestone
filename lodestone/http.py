"""Small, polite HTTP helper built on the standard library (no installs needed)."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Optional

USER_AGENT = "Lodestone/0.1 (personal job search; github.com/logblogger89/lodestone)"


class HttpError(Exception):
    def __init__(self, status: int, url: str):
        super().__init__(f"HTTP {status} for {url}")
        self.status = status
        self.url = url


def get_json(url: str, *, timeout: float = 25, retries: int = 1, method: str = "GET",
             body: Optional[dict] = None) -> Any:
    data = json.dumps(body).encode() if body is not None else None
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    last: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(2 * (attempt + 1))
                last = e
                continue
            raise HttpError(e.code, url) from None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = e
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
                continue
    raise ConnectionError(f"{url}: {last}")
