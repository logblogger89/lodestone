"""Small, polite HTTP helper built on the standard library (no installs needed)."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional

USER_AGENT = "Lodestone/0.1 (personal job search; github.com/logblogger89/lodestone)"


class HttpError(Exception):
    def __init__(self, status: int, url: str):
        super().__init__(f"HTTP {status} for {url}")
        self.status = status
        self.url = url


def get_json(url: str, *, timeout: float = 25, retries: int = 1, method: str = "GET",
             body: Optional[dict] = None, form: Optional[dict] = None,
             headers: Optional[dict] = None) -> Any:
    return json.loads(fetch(url, timeout=timeout, retries=retries, method=method, body=body, form=form,
                            headers={"Accept": "application/json", **(headers or {})}))


def get_text(url: str, *, timeout: float = 30, retries: int = 1, headers: Optional[dict] = None) -> str:
    """Fetch an HTML page (for careers sites that embed their job data in the page)."""
    return fetch(url, timeout=timeout, retries=retries, headers={"User-Agent": BROWSER_UA, **(headers or {})})


# Some careers sites serve their embedded data only to browser-like clients.
BROWSER_UA = "Mozilla/5.0 (compatible; Lodestone/0.1; personal job search)"


def fetch(url: str, *, timeout: float = 25, retries: int = 1, method: str = "GET",
          body: Optional[dict] = None, form: Optional[dict] = None, headers: Optional[dict] = None) -> str:
    hdrs = {"User-Agent": USER_AGENT, **(headers or {})}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json"
    elif form is not None:
        data = urllib.parse.urlencode(form).encode()
        hdrs["Content-Type"] = "application/x-www-form-urlencoded"
    if data is not None and method == "GET":
        method = "POST"
    last: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep((10 if e.code == 429 else 2) * (attempt + 1))
                last = e
                continue
            raise HttpError(e.code, url) from None
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
                continue
    raise ConnectionError(f"{url}: {last}")
