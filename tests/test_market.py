import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from lodestone import market

PAGE = """# Levels.fyi – Shopify Product Manager Salaries in Greater Toronto Area

**URL:** https://www.levels.fyi/companies/shopify/salaries/product-manager/locations/greater-toronto-area  
**Location:** Greater Toronto Area  
**Currency:** CAD (CA$)

- Last Updated: October 15, 2026

| Level | Median Total Compensation |
| --- | --- |
| L5 | CA$161,365 |
| L6 | CA$234,562 |
| L7 | CA$271,900 |
"""
US_PAGE = PAGE.replace("CAD (CA$)", "USD ($)").replace("CA$", "$")
JOBS = {"jobs": {"k1": {"company": "Shopify", "title": "Senior Product Manager", "region": "Waterloo Region",
                        "live": True, "role_tier": "Core"}}}


class TestMarket(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.state = {}
        patches = [mock.patch.object(market, "FETCHED", Path(self.tmp.name)),
                   mock.patch.object(market.store, "load", lambda n, d: JOBS if n == "jobs" else self.state.get(n, d)),
                   mock.patch.object(market.store, "save", lambda n, d: self.state.__setitem__(n, d))]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_parse_and_maps(self):
        p = market.parse(PAGE)
        self.assertEqual((p["currency"], p["location"], p["updated"]), ("CAD", "Greater Toronto Area", "October 15, 2026"))
        self.assertEqual(p["levels"][1], {"level": "L6", "median_total": 234562})
        self.assertEqual(market.slug("Thomson Reuters"), "thomson-reuters")
        self.assertEqual(market.family("Senior Technical Program Manager"), "technical-program-manager")
        self.assertEqual(market.family("Group Product Manager"), "product-manager")

    def test_us_fallback_page_is_rejected_then_canada_used(self):
        urls = []
        def getter(url, ua):
            urls.append(url)
            self.assertTrue(ua.startswith("Claude-User"))
            return US_PAGE if "waterloo-region" in url else PAGE
        out = market.fetch("shopify senior", getter=getter)
        self.assertEqual(out["status"], "ok")
        self.assertEqual([u.rsplit("/", 1)[1] for u in urls], ["waterloo-region.md", "canada.md"])

    def test_add_keeps_level_and_neighbours_only(self):
        market.fetch("shopify senior", getter=lambda u, a: PAGE)
        jid = market.find("shopify senior")[0][0]
        self.assertEqual(market.add(jid, "L9")["status"], "unknown_level")
        out = market.add(jid, "L6", "Senior PM ≈ L6 at Shopify")
        self.assertEqual((out["median_total"], [n["level"] for n in out["neighbours"]]), (234562, ["L5", "L7"]))
        self.assertIn(jid, self.state["market_checks"])


if __name__ == "__main__":
    unittest.main()
