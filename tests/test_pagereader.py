import datetime as dt
import pathlib
import tempfile
import unittest
from unittest import mock

from lodestone import pagereader, store
from lodestone.adapters.page import PageAdapter

HTML = """<html><head><script>var x=1</script></head><body>
<a href=/position/pm/ ><h4>Senior Product Manager</h4><p>Toronto, Canada</p></a>
<li class='job' data-job-postings-url='https://x.com/job_posting/pm-2'>Product Lead</li>
<a href="#top">Top</a><a href="mailto:a@b.c">Email</a>
</body></html>"""


class TestPageReader(unittest.TestCase):
    def test_page_text_keeps_job_links(self):
        t = pagereader.page_text(HTML, "https://co.com/careers/")
        self.assertIn("[Senior Product Manager Toronto, Canada](https://co.com/position/pm/)", t)
        self.assertIn("[link](https://x.com/job_posting/pm-2)", t)
        self.assertNotIn("var x", t)
        self.assertNotIn("mailto", t)

    def test_save_and_adapter(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(store, "STATE", pathlib.Path(tmp)):
            pagereader.save("Co", [{"title": "PM", "url": "https://co.com/1", "location": "Toronto, ON"}])
            ps = PageAdapter().list_feed("Co", {"url": "https://co.com"})
            self.assertEqual((ps[0].title, ps[0].location_raw), ("PM", "Toronto, ON"))
            old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=3)).isoformat()
            store.save("page_reads", {"Co": {"read_at": old, "jobs": []}})
            with self.assertRaises(ValueError):          # stale read = failed source, not "all jobs closed"
                PageAdapter().list_feed("Co", {"url": "https://co.com"})

    def test_save_rejects_incomplete(self):
        with self.assertRaises(ValueError):
            pagereader.save("Co", [{"title": "PM"}])


if __name__ == "__main__":
    unittest.main()
