"""Source adapters: one per job system (ATS). Registered by type name (D-005: plugins, not hard-coding)."""
from .ashby import AshbyAdapter
from .greenhouse import GreenhouseAdapter
from .lever import LeverAdapter
from .smartrecruiters import SmartRecruitersAdapter

ADAPTERS = {a.type: a for a in (GreenhouseAdapter(), LeverAdapter(), AshbyAdapter(), SmartRecruitersAdapter())}
# Detection order: most common for tech companies first.
DETECT_ORDER = ["greenhouse", "ashby", "lever", "smartrecruiters"]
