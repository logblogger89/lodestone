import unittest
from unittest import mock

from lodestone import payest


def _pay(lo, hi, cur="CAD", kind="base"):
    return {"ranges": [{"min": lo, "max": hi, "currency": cur, "interval": "year", "kind": kind}], "primary": 0}


def _job(company, title, pay=None):
    return {"company": company, "title": title, "live": True, "role_tier": "pm", "pay": pay}


class TestPayEstimates(unittest.TestCase):
    def test_level_of(self):
        self.assertEqual(payest.level_of("Senior Product Manager", None), 5)
        self.assertEqual(payest.level_of("Product Manager", "L5-L6"), 6)
        self.assertEqual(payest.level_of("Group Product Manager", None), 6)
        self.assertIsNone(payest.level_of("Product Manager", None))

    def test_only_clean_canadian_base_is_used(self):
        self.assertIsNotNone(payest._canadian_base(_pay(150000, 190000)))
        self.assertIsNone(payest._canadian_base(_pay(150000, 190000, cur="USD")))
        self.assertIsNone(payest._canadian_base(_pay(150000, 190000, kind="ote")))
        self.assertIsNone(payest._canadian_base(_pay(80000, 300000)))

    def _build(self, jobs):
        def load(name, default):
            return {"jobs": jobs} if name == "jobs" else {}
        with mock.patch.object(payest.store, "load", load), \
                mock.patch.object(payest.pipeline, "employers", lambda: [{"company": "A", "segment": "fintech"},
                                                                         {"company": "B", "segment": "fintech"}]):
            return payest.build()

    def test_same_company_same_level_is_high(self):
        jobs = {"a1": _job("A", "Senior Product Manager", _pay(150000, 180000)),
                "a2": _job("A", "Senior Product Manager, Payments")}
        est = self._build(jobs)[payest.job_id("a2")]
        self.assertEqual((est["min"], est["max"], est["confidence"]), (150000, 180000, "high"))
        self.assertNotIn(payest.job_id("a1"), self._build(jobs))   # posted roles get no estimate

    def test_one_level_away_is_adjusted(self):
        jobs = {"a1": _job("A", "Senior Product Manager", _pay(100000, 200000)),
                "a2": _job("A", "Staff Product Manager")}
        est = self._build(jobs)[payest.job_id("a2")]
        self.assertEqual((est["min"], est["max"], est["confidence"]), (115000, 230000, "medium"))

    def test_too_few_comparables_gives_nothing(self):
        jobs = {"b1": _job("B", "Senior Product Manager", _pay(150000, 180000)),
                "a2": _job("A", "Senior Product Manager")}
        self.assertEqual(self._build(jobs), {})


if __name__ == "__main__":
    unittest.main()
