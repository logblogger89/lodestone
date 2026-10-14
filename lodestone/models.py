"""Core data shapes shared by every adapter and pipeline step."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class Company:
    name: str
    segment: str = ""
    canada_locations: str = ""
    fit_tier: str = ""
    why_relevant: str = ""
    discovery_source: str = ""
    ats: Optional[str] = None          # greenhouse | lever | ashby | smartrecruiters | None
    slug: Optional[str] = None
    ats_checked_at: Optional[str] = None
    status: str = "active"             # active | muted | blocked

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Posting:
    """One job as seen on one source."""
    source: str                        # adapter type, e.g. "greenhouse"
    company: str
    slug: str
    source_job_id: str
    title: str
    url: str                           # exact posting URL (R2 deep link)
    location_raw: str = ""
    country_hint: Optional[str] = None # structured country from the source, when given
    remote_hint: Optional[bool] = None
    workplace: Optional[str] = None    # onsite | hybrid | remote, when the source says
    department: str = ""
    posted_at: Optional[str] = None
    description: str = ""              # plain text, may be empty for list-only sources
    pay: Optional[dict] = None         # {"min","max","currency","interval","posted": True}
    extra: dict = field(default_factory=dict)

    @property
    def canonical_key(self) -> str:
        return f"{self.source}:{self.slug}:{self.source_job_id}"
