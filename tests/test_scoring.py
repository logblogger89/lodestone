import tempfile
import unittest
from pathlib import Path
from unittest import mock

from lodestone import scoring
from lodestone.appexport import job_id

JOBS = {f"k{i}": {"title": f"PM {i}", "company": "A", "live": True, "role_tier": "Core", "description": "d",
                  "first_seen": f"2026-10-{10 + i:02d}"} for i in range(5)}


class TestScoringPrepare(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        rubric = scoring.config()["rubric_version"]
        self.scores = {job_id(k): {"fingerprint": scoring._fingerprint(j, rubric)} for k, j in JOBS.items()}
        for p in (mock.patch.object(scoring, "INBOX", Path(self.tmp.name) / "inbox"),
                  mock.patch.object(scoring.store, "load", lambda n, d: {"jobs": JOBS} if n == "jobs" else self.scores)):
            p.start()
            self.addCleanup(p.stop)

    def test_nothing_to_do_without_a_profile(self):
        self.assertEqual(scoring.prepare(), [])

    def test_profile_change_rescores_newest_first_within_the_cap(self):
        out = scoring.prepare(profile={"headline": "PM", "domains": ["AI"]}, max_rescore=2)
        self.assertEqual(out[0]["jobs"], 2)
        self.assertEqual(out[-1], {"profile_rescore_waiting": 3})
        import json
        batch = json.loads(Path(out[0]["file"]).read_text())
        self.assertEqual([b["title"] for b in batch], ["PM 4", "PM 3"])
        self.assertTrue(batch[0]["profile_key"])

    def test_rescore_cap_counts_earlier_runs_today(self):
        from lodestone import store
        log = {store.today(): ["a", "b", "c"]}
        with mock.patch.object(scoring.store, "load", lambda n, d: {"jobs": JOBS} if n == "jobs" else log if n == "rescore_log" else self.scores):
            out = scoring.prepare(profile={"headline": "PM", "domains": ["AI"]}, max_rescore=4)
        self.assertEqual(out[0]["jobs"], 1)
        self.assertEqual(out[-1], {"profile_rescore_waiting": 4})

    def test_profile_key_ignores_the_resume_file(self):
        a = scoring.profile_key({"headline": "x", "resume": {"asset_id": "1"}})
        b = scoring.profile_key({"headline": "x", "resume": {"asset_id": "2"}})
        self.assertEqual(a, b)


    def test_prepare_refuses_to_replace_batches_still_being_scored(self):
        scoring.prepare(profile={"headline": "PM", "domains": ["AI"]}, max_rescore=2)
        with self.assertRaises(RuntimeError):
            scoring.prepare(profile={"headline": "PM", "domains": ["AI"]}, max_rescore=2)
        self.assertTrue(scoring.prepare(profile={"headline": "PM", "domains": ["AI"]}, max_rescore=2, force=True))


if __name__ == "__main__":
    unittest.main()
