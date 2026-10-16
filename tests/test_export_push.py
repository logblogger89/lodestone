import unittest
from unittest import mock

from lodestone import appexport


class TestMarkPushed(unittest.TestCase):
    def test_unpushed_documents_stay_changed(self):
        state = {"export_hashes": {"jobs/b0": "old"}, "export_hashes_pending": {"jobs/b0": "new", "desc/d01": "x"}}
        with mock.patch.object(appexport.store, "load", lambda n, d: state.get(n, d)), \
             mock.patch.object(appexport.store, "save", lambda n, d: state.__setitem__(n, d)):
            self.assertEqual(appexport.mark_pushed(["jobs/b0"]), {"marked": 1})
            self.assertEqual(state["export_hashes"], {"jobs/b0": "new"})       # desc/d01 not pushed: still changed next time
            appexport.mark_pushed()
            self.assertEqual(state["export_hashes"]["desc/d01"], "x")


if __name__ == "__main__":
    unittest.main()
