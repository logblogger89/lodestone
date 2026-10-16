"""Split a posting into its sections (D-065): the job description shown in the app, the company's own "About us"
text, and the team's description when the posting has one. Plain text in, plain text out; the app formats it.
"""
from __future__ import annotations

import re

MAX_TEXT = 12000
_HEAD_WORDS = re.compile(
    r"^(about|who we are|who you are|our (team|company|mission|story|values)|the team|meet the team|team overview|"
    r"what you|what we|why |the role|role (overview|summary|description)|position (overview|summary)|the position|the opportunity|the impact|responsibilities|requirements|qualifications|"
    r"key responsibilities|basic qualifications|preferred qualifications|minimum qualifications|nice to have|bonus|"
    r"benefits|perks|compensation|pay|salary|location|how we work|life at|working at|equal|accommodation|"
    r"diversity|inclusion|privacy|additional information|job description|overview|summary|your (role|impact|day)|"
    r"you will|you'll|you have|in this role|day to day|must have|skills)", re.I)
COMPANY_HEAD = re.compile(r"^(about (us|the company|the business|{co})\b|who we are|our (company|mission|story)|"
                          r"company overview|at {co}\b|life at {co}|why {co}\b)", re.I)
TEAM_HEAD = re.compile(r"^(about the (team|group|org|organi[sz]ation|department|product team|.{0,30} team)|the team\b|"
                       r"meet the team|our team|team overview|what your team does|who you'?ll work with|"
                       r"your team)", re.I)
LEGAL_HEAD = re.compile(r"equal (employment|opportunit)|\beeo\b|accommodation|privacy|e-?verify|land acknowledg|"
                        r"pay transparency|applicant (notice|privacy)|disclaimer|recruitment fraud|right to work|"
                        r"diversity,? (equity|inclusion)|our commitment to (diversity|inclusion)", re.I)


def _caps_heading(t: str) -> bool:
    """A short line in capitals ("ROLE OVERVIEW", "THE PERKS"), but not a pay range, a hashtag-style tag ("LI-REMOTE")
    or an acronym on its own line."""
    return t.isupper() and not re.search(r"[\d$€£#@]|^LI-", t) and len(re.findall(r"[A-Z]{3,}", t)) >= 2


def _is_heading(line: str) -> bool:
    t = line.strip().strip("*#_").strip()
    if not t or len(t) > 70 or t.endswith((".", ",", ";")) or t.startswith(("-", "•", "·")):
        return False
    short = len(t.split()) <= 6
    return t.endswith(":") or bool(_HEAD_WORDS.match(t)) or (short and (t.istitle() or _caps_heading(t)))


def sections(text: str) -> list[tuple[str, str]]:
    """[(heading, body)], the first heading is '' for text before any heading."""
    out, head, buf = [], "", []
    for line in (text or "").splitlines():
        if _is_heading(line):
            if buf or head:
                out.append((head, "\n".join(buf).strip()))
            head, buf = line.strip().strip("*#_").strip().rstrip(":").strip(), []
        else:
            buf.append(line.rstrip())
    if buf or head:
        out.append((head, "\n".join(buf).strip()))
    return [(h, b) for h, b in out if b or h]


def _clip(text: str, limit: int) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(text) <= limit:
        return text
    cut = text[:limit]
    end = max(cut.rfind(". "), cut.rfind(".\n"))
    return (cut[:end + 1] if end > limit * 0.5 else cut).rstrip() + " …"


def _co(company: str) -> str:
    return re.escape(re.sub(r"\s*\(.*?\)", "", company or "").strip()) or "a^"


def company_about(text: str, company: str) -> str | None:
    head = re.compile(COMPANY_HEAD.pattern.format(co=_co(company)), re.I)
    for h, b in sections(text):
        if h and head.match(h) and len(b) > 80 and not TEAM_HEAD.match(h):
            return _clip(b, 900)
    first = sections(text)[:1]
    if first and not first[0][0]:                          # an opening paragraph like "Stripe is a financial ..."
        para = first[0][1].split("\n\n")[0]
        if re.match(rf"^(at )?{_co(company)}\b.{{0,40}}\b(is|are|builds|helps|makes|provides|was founded|we)\b", para, re.I) and len(para) > 80:
            return _clip(para, 900)
    return None


def team_about(text: str) -> tuple[str, str] | None:
    """(heading, text) of the posting's team section, if it has one."""
    for h, b in sections(text):
        if h and TEAM_HEAD.match(h) and len(b) > 60:
            return h, _clip(b, 1200)
    return None


def for_app(text: str) -> dict:
    """The job description for the app: legal boilerplate separated out, capped in length."""
    main, legal = [], []
    for h, b in sections(text):
        (legal if (h and LEGAL_HEAD.search(h)) else main).append((h, b))
    body = "\n\n".join((f"## {h}\n{b}" if h else b) for h, b in main).strip()
    legal_text = "\n\n".join((f"## {h}\n{b}" if h else b) for h, b in legal).strip()
    truncated = len(body) > MAX_TEXT
    return {"text": _clip(body, MAX_TEXT) if truncated else body, "legal": _clip(legal_text, 2500) if legal_text else "",
            "truncated": truncated}


def best_company_about(abouts: list[str], company: str) -> str | None:
    """Of a company's 'About us' texts across its postings, prefer one that says what the company is, then the most
    common (their standard boilerplate), then the longest."""
    abouts = [a for a in abouts if a]
    if not abouts:
        return None
    says = re.compile(rf"\b{_co(company)}\b[^.]{{0,40}}\b(is|are|builds|helps|makes|provides|powers)\b|^we (are|build|help|make)", re.I)
    count = {a: abouts.count(a) for a in abouts}
    return max(count, key=lambda a: (bool(says.search(a)), count[a], min(len(a), 900)))
