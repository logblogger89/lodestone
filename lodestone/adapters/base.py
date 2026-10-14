"""Adapter contract every job-system plugin implements."""
from __future__ import annotations

from typing import Protocol

from ..models import Posting


class SourceAdapter(Protocol):
    type: str
    label: str
    host: str

    def fetch(self, slug: str) -> object: ...
    def parse(self, payload: object, company: str, slug: str) -> list[Posting]: ...
    def exists(self, slug: str) -> int | None:
        """Number of open jobs if the board exists, else None."""
        ...

    def list_jobs(self, company: str, slug: str) -> list[Posting]:
        return self.parse(self.fetch(slug), company, slug)
