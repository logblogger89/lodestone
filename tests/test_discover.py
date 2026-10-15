import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from lodestone import discover


class TestDiscover(unittest.TestCase):
    def setUp(self):
        self.state = {}
        self.seed = [{"company": "Shopify", "segment": "SaaS", "canada_locations": "Ottawa", "fit_tier": "A",
                      "why_relevant": "", "discovery_source": "claude-knowledge"}]
        self.rows = []
        ps = [mock.patch.object(discover.store, "load", lambda n, d: self.state.get(n, d)),
              mock.patch.object(discover.store, "save", lambda n, d: self.state.__setitem__(n, d)),
              mock.patch.object(discover.store, "read_seed", lambda: list(self.seed)),
              mock.patch.object(discover.sources, "load", lambda: list(self.rows)),
              mock.patch.object(discover.sources, "save", lambda r: setattr(self, "rows", r))]
        for p in ps:
            p.start()
            self.addCleanup(p.stop)
        discover.on_watchlist.__defaults__[0].clear()

    def test_watchlist_companies_are_never_candidates(self):
        d = discover._load()
        discover._merge(d, "Shopify Canada Inc.", "lmia", "x")
        discover._merge(d, "Caseware International Inc.", "lmia", "13 hires")
        discover._merge(d, "Caseware International Inc.", "search", "PM role")
        self.assertEqual(list(d["candidates"]), ["caseware-international"])
        self.assertEqual(set(d["candidates"]["caseware-international"]["routes"]), {"lmia", "search"})

    def test_review_export_and_apply(self):
        d = discover._load()
        discover._merge(d, "Caseware International Inc.", "lmia", "13 hires")
        discover._merge(d, "Some Consulting Inc.", "lmia", "9 hires")
        d["candidates"]["caseware-international"]["board"] = {"platform": "lever", "slug": "caseware", "confidence": "high"}
        discover._save(d)
        discover.review([{"key": "caseware-international", "verdict": "suggest", "brand": "Caseware", "segment": "SaaS", "why": "Audit software"},
                         {"key": "some-consulting", "verdict": "skip", "why": "staffing"}])
        s = discover.suggestions()
        self.assertEqual([x["name"] for x in s], ["Caseware"])
        with tempfile.TemporaryDirectory() as t, mock.patch.object(discover.store, "SEED", Path(t) / "seed.csv"):
            (Path(t) / "dec").mkdir()
            (Path(t) / "dec" / "caseware-international.json").write_text(json.dumps({"decision": "approve"}))
            out = discover.apply(str(Path(t) / "dec"))
            self.assertEqual(out["approved"], ["Caseware"])
            self.assertIn("Caseware", (Path(t) / "seed.csv").read_text())
        self.assertEqual(self.rows[0]["platform"], "lever")
        self.assertEqual(discover.suggestions(), [])           # approved: no longer suggested


if __name__ == "__main__":
    unittest.main()
