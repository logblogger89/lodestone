"""Text helpers: strip HTML to plain text, normalize names into slugs."""
from __future__ import annotations

import html
import re
import unicodedata

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"[ \t\r\f\v]+")


def html_to_text(s: str) -> str:
    if not s:
        return ""
    s = html.unescape(html.unescape(s))          # Greenhouse double-escapes content
    s = re.sub(r"(?i)<\s*(br|/p|/li|/h\d|/div)\s*/?>", "\n", s)
    s = re.sub(r"(?i)<\s*li[^>]*>", "\n- ", s)
    s = _TAG.sub(" ", s)
    s = _WS.sub(" ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


def ascii_fold(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def slug_candidates(name: str) -> list[str]:
    """Likely ATS board slugs for a company name, most likely first."""
    base = re.sub(r"\(.*?\)", " ", name)                     # drop "(Square / Cash App)"
    base = ascii_fold(base).lower().replace("&", " and ")
    words = re.findall(r"[a-z0-9]+", base)
    if not words:
        return []
    cands = ["".join(words), "-".join(words)]
    noise = {"inc", "ltd", "corp", "co", "the", "ai", "labs", "technologies", "group", "canada"}
    core = [w for w in words if w not in noise]
    if core and core != words:
        cands += ["".join(core), "-".join(core)]
    if len(words) > 1:
        cands.append(words[0])
    seen, out = set(), []
    for c in cands:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def norm_title(s: str) -> str:
    s = ascii_fold(s).lower()
    s = re.sub(r"\b(sr|snr)\b\.?", "senior", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())
