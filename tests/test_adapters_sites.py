"""Offline checks for careers-site parsing helpers (no network)."""
import unittest
from unittest import mock

from lodestone.adapters.html_sites import AvatureAdapter, ICIMSAdapter
from lodestone.adapters.workday import WorkdayAdapter
from lodestone.adapters import enterprise
from lodestone.geo import classify

RSS = """<?xml version="1.0"?><rss xmlns:g="http://base.google.com/ns/1.0"><channel>
<item><title>Senior Product Manager (Toronto, ON, CA, M5J 2J5)</title><link>https://jobs.x.com/job/1/</link>
<g:id>1</g:id><description>&lt;p&gt;Own payments&lt;/p&gt;</description></item>
<item><title>Senior Product Manager (Toronto, ON, CA, M5J 2J5)</title><link>https://jobs.x.com/job/1/</link><g:id>1</g:id></item>
</channel></rss>"""


class TestSites(unittest.TestCase):
    def test_workday_canada_facet_nested(self):
        facets = [{"facetParameter": "locationMainGroup", "values": [
            {"facetParameter": "locationCountry", "descriptor": "Location Country", "values": [
                {"descriptor": "United States", "id": "us"}, {"descriptor": "Canada", "id": "ca-id"}]}]}]
        self.assertEqual(WorkdayAdapter._canada_facet(facets), ("locationCountry", "ca-id"))

    def test_icims_location(self):
        self.assertEqual(ICIMSAdapter._loc("CA-ON-Ottawa"), "Ottawa, ON, Canada")
        self.assertEqual(ICIMSAdapter._loc("CA-Remote"), "Remote, Canada")
        self.assertEqual(ICIMSAdapter._loc("JP-Tokyo"), "JP-Tokyo")

    def test_avature_locations(self):
        a = AvatureAdapter()
        card = '<div class="article__header__text__subtitle"><span>Canada · Ontario · Toronto</span></div>'
        self.assertEqual(a._location(card, "u"), "Toronto, Ontario, Canada")
        self.assertEqual(a._location("<td> Montreal </td>", "https://x/JobDetail/Montr-al-Quebec-Canada-T1/1"), "Montreal, Canada")

    def test_successfactors_feed(self):
        with mock.patch.object(enterprise, "fetch", return_value=RSS):
            ps = enterprise.SuccessFactorsAdapter().list_feed("X", {"host": "jobs.x.com", "mode": "feed"})
        self.assertEqual(len(ps), 1)                         # EN/FR duplicate removed
        self.assertEqual(ps[0].title, "Senior Product Manager")
        self.assertEqual(classify(ps[0]).region, "GTA")
        self.assertIn("Own payments", ps[0].description)


if __name__ == "__main__":
    unittest.main()
