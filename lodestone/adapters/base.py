"""Adapter contracts. A new job system or careers site = one new file implementing one of these."""
from __future__ import annotations

from typing import Protocol

from ..models import Posting


class BoardAdapter(Protocol):
    """Hosted job boards addressed by a slug (Greenhouse, Lever, Ashby, SmartRecruiters)."""
    type: str
    label: str
    host: str

    def exists(self, slug: str) -> int | None:
        """Number of open jobs if the board exists, else None (used by auto-detection)."""
        ...

    def list_jobs(self, company: str, slug: str) -> list[Posting]: ...


class SiteAdapter(Protocol):
    """Careers sites addressed by feed params from the source index (Workday, Google, Amazon...)."""
    type: str
    label: str
    host: str

    def list_feed(self, company: str, feed: dict) -> list[Posting]: ...

    # Optional: fetch the full posting when the list view is thin (no description or locations).
    # Called only for jobs that pass the role rules.
    def detail(self, p: Posting) -> dict: ...
