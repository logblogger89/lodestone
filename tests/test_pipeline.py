"""End-to-end refresh with a fake feed: Canada filter, dedup across runs, and liveness."""
import tempfile
import pathlib
import unittest
from unittest import mock

from lodestone import pipeline, store
from lodestone.models import Posting


class FakeAdapter:
    type = "fake"

    def __init__(self):
        self.ids = ["1", "2"]

    def list_jobs(self, company, slug):
        locs = {"1": "Toronto, ON", "2": "Austin, TX", "3": "Waterloo, ON"}
        return [Posting(source="fake", company=company, slug=slug, source_job_id=i,
                        title="Senior Product Manager", url=f"https://x/{i}", location_raw=locs[i])
                for i in self.ids]


class TestRefresh(unittest.TestCase):
    def test_refresh_and_liveness(self):
        fake = FakeAdapter()
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(store, "STATE", pathlib.Path(tmp)), \
                mock.patch.dict(pipeline.ADAPTERS, {"fake": fake}):
            store.save("companies", {"companies": [{"name": "Acme", "ats": "fake", "slug": "acme"}]})
            s = pipeline.refresh(log=lambda m: None)
            self.assertEqual((s["canada_postings"], s["candidates"]), (1, 1))
            fake.ids = ["3"]                              # job 1 disappears, job 3 appears
            pipeline.refresh(log=lambda m: None)
            self.assertTrue(store.load("jobs", {})["jobs"]["fake:acme:1"]["live"])   # one miss: still live
            s = pipeline.refresh(log=lambda m: None)
            jobs = store.load("jobs", {})["jobs"]
            self.assertFalse(jobs["fake:acme:1"]["live"])                           # two misses: closed
            self.assertTrue(jobs["fake:acme:3"]["live"])
            self.assertEqual(s["candidates"], 1)


if __name__ == "__main__":
    unittest.main()
