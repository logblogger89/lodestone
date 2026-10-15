"""Source adapters: one per job system or careers site. Registered by type name (D-005: plugins,
not hard-coding). Which company uses which adapter lives in data/sources/source_index.csv."""
from .amazon import AmazonAdapter
from .apple import AppleAdapter
from .ashby import AshbyAdapter
from .eightfold import EightfoldAdapter
from .enterprise import ALL as ENTERPRISE
from .google import GoogleAdapter
from .greenhouse import GreenhouseAdapter
from .html_sites import ALL as HTML_SITES
from .lever import LeverAdapter
from .meta import MetaAdapter
from .oracle_hcm import OracleHcmAdapter
from .page import PageAdapter
from .small_ats import ALL as SMALL_ATS
from .smartrecruiters import SmartRecruitersAdapter
from .workday import WorkdayAdapter

ADAPTERS = {a.type: a for a in (
    GreenhouseAdapter(), LeverAdapter(), AshbyAdapter(), SmartRecruitersAdapter(), WorkdayAdapter(),
    EightfoldAdapter(), GoogleAdapter(), AmazonAdapter(), AppleAdapter(), MetaAdapter(), OracleHcmAdapter(), *SMALL_ATS, *ENTERPRISE, *HTML_SITES, PageAdapter())}
# Board-style systems we can auto-detect from a company name, most common first.
DETECT_ORDER = ["greenhouse", "ashby", "lever", "smartrecruiters"]


def pull(platform: str, company: str, feed: dict):
    """List a company's jobs. Board adapters take a slug; site adapters take their feed params."""
    a = ADAPTERS[platform]
    if hasattr(a, "list_feed"):
        return a.list_feed(company, feed)
    return a.list_jobs(company, feed["slug"])
