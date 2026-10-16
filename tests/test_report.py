import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from lodestone import report

GOOD = {"date": "2026-10-16", "headline": "6 new roles; 1 strong match", "stats": {"new": 6, "closed": 2},
        "top": [{"id": "abc", "company": "Shopify", "title": "Senior PM", "fit": 84, "pay": "CA$180K–220K", "why": "AI platform"}],
        "sections": [{"title": "Closed", "items": ["RBC Program Manager"]}], "actions": []}


class TestReport(unittest.TestCase):
    def test_validate(self):
        self.assertEqual(report.validate(GOOD), [])
        bad = {**GOOD, "date": "Oct 16", "stats": {"new": "six"}}
        self.assertEqual(len(report.validate(bad)), 2)

    def test_save_writes_and_lists_old_days(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(report, "DIR", Path(d)):
            (Path(d) / "2026-06-01.json").write_text("{}")
            out = report.save(GOOD, today=dt.date(2026, 10, 16))
            self.assertEqual(out["status"], "saved")
            self.assertEqual(out["delete_from_db"], ["reports/2026-06-01"])
            self.assertEqual(json.loads((Path(d) / "2026-10-16.json").read_text())["top"][0]["fit"], 84)

    def test_save_accepts_a_report_read_back_from_the_app(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(report, "DIR", Path(d)):
            out = report.save({"id": "2026-10-16", "data": GOOD, "version": 3}, today=dt.date(2026, 10, 16))
            self.assertEqual(out["status"], "saved")


if __name__ == "__main__":
    unittest.main()
