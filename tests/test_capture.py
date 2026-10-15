import pathlib
import tempfile
import unittest
from unittest import mock

from lodestone import capture, dedup, store


class TestCapture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.p = mock.patch.object(store, "STATE", pathlib.Path(self.tmp.name))
        self.p.start()
        self.c = mock.patch.object(capture, "INBOX", pathlib.Path(self.tmp.name) / "capture_inbox")
        self.c.start()
        rec = {"key": "greenhouse:acme:1", "source": "greenhouse", "url": "https://boards.greenhouse.io/acme/jobs/1",
               "seen_at": "t0", "group": dedup.group_key("Acme", "Senior Product Manager", "GTA"),
               "company": "Acme", "title": "Senior Product Manager", "region": "GTA"}
        jobs = {}
        dedup.merge(jobs, rec)
        store.save("jobs", {"jobs": jobs})

    def tearDown(self):
        self.p.stop(); self.c.stop(); self.tmp.cleanup()

    def test_known_link_and_linkedin(self):
        out = capture.prepare([
            {"id": "a", "status": "new", "text": "https://boards.greenhouse.io/acme/jobs/1/?utm=x"},
            {"id": "b", "status": "new", "text": "https://www.linkedin.com/jobs/view/123/"},
            {"id": "c", "status": "added", "text": "already processed"}])
        kinds = {o["doc_id"]: o["links"][0][0] for o in out}
        self.assertEqual(kinds, {"a": "already_known", "b": "no_fetch"})

    def test_pasted_duplicate_merges_and_non_canada_skipped(self):
        res = capture.add([
            {"doc_id": "x", "url": "https://www.linkedin.com/jobs/view/9/", "title": "Sr Product Manager",
             "company": "Acme Inc.", "location": "Toronto, ON", "description": "Base salary $150,000 - $180,000 CAD"},
            {"doc_id": "y", "url": "https://example.com/j", "title": "PM", "company": "Z", "location": "Austin, TX"}])
        self.assertEqual([r["status"] for r in res], ["added", "not_canada"])
        self.assertIn("Matched an existing role", res[0]["result"])
        job = store.load("jobs", {})["jobs"]["greenhouse:acme:1"]
        self.assertEqual(len(job["sightings"]), 2)


if __name__ == "__main__":
    unittest.main()
