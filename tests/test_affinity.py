import tempfile
import unittest
from pathlib import Path
from unittest import mock

from lodestone import affinity, scoring


class TestAffinity(unittest.TestCase):
    def test_title_prior_until_read(self):
        self.assertEqual(affinity.prior("Senior Business Analyst"), {"ba": 85})
        self.assertEqual(affinity.prior("Barista"), {})

    def test_a_job_can_be_more_than_one_type(self):
        aff = {"program": 80, "pm": 70}           # "Program Manager, Payments" that is mostly product work
        self.assertEqual(affinity.relevance(aff, ["pm"], [])[0], 70)          # shown to a PM on its product side
        self.assertEqual(affinity.relevance(aff, ["program"], [])[0], 80)
        self.assertLess(affinity.relevance({"program": 40}, ["ba"], [])[0], affinity.SHOWN_AT)

    def test_related_and_stretch_count_a_little_less(self):
        self.assertEqual(affinity.relevance({"program": 80}, ["pm"], ["program"])[0], 68)   # related: x0.85
        self.assertEqual(affinity.relevance({"program": 80}, ["pm"], [])[0], 0)             # not asked to see it

    def test_ingest_rejects_unknown_families_and_bad_numbers(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(affinity.store, "STATE", Path(d)):
            saved = {}
            with mock.patch.object(affinity.store, "load", lambda n, dflt: saved.get(n, dflt)), \
                    mock.patch.object(affinity.store, "save", lambda n, v: saved.__setitem__(n, v)), \
                    mock.patch.object(affinity.store, "log_today", lambda *a: 1):
                out = affinity.ingest([{"id": "a", "fingerprint": "f", "aff": {"pm": 90, "program": 3}},
                                       {"id": "b", "fingerprint": "f", "aff": {"cooking": 90}},
                                       {"id": "c", "fingerprint": "f", "aff": {"pm": 120}}])
            self.assertEqual(out["stored"], 1)
            self.assertEqual(sorted(out["rejected"]), ["b", "c"])
            self.assertEqual(saved["affinity"]["a"]["aff"], {"pm": 90})      # tiny scores dropped


class TestProfileKey(unittest.TestCase):
    def test_app_side_changes_cost_no_rescoring(self):
        a = {"headline": "x", "preferences": {"domains_wanted": "AI", "locations": ["GTA"], "people_management": False}, "work_status": "needs_permit"}
        b = {"headline": "x", "preferences": {"domains_wanted": "AI", "locations": ["Calgary"], "people_management": True}, "work_status": "open_permit"}
        c = {"headline": "x", "preferences": {"domains_wanted": "fintech", "locations": ["GTA"]}}
        self.assertEqual(scoring.profile_key(a), scoring.profile_key(b))
        self.assertNotEqual(scoring.profile_key(a), scoring.profile_key(c))
        self.assertNotEqual(scoring.profile_key(a), scoring.legacy_key(a))


if __name__ == "__main__":
    unittest.main()
