import unittest

from lodestone.pay import resolve

TR = """Eligible office location(s) for this role include one or more of the following: New York City, San Francisco, Los Angeles, and/or Irvine, CA; McLean, VA; Washington, DC. The base compensation range for the role in any of those locations is $137,900 USD - $256,100 USD.
For any eligible US locations, unless otherwise noted, the base compensation range for this role is $119,700 USD - $222,300 USD.
For Ontario, Canada, the base compensation range for this role is $126,000 CAD - $176,000 CAD."""


def ranges(text, region="GTA"):
    r = resolve(None, text, "Toronto, ON", region)
    return r and [(x["min"], x["max"], x["currency"], x["canada"]) for x in r["ranges"]], r and r["primary"]


class TestPay(unittest.TestCase):
    def test_thomson_reuters_multi_region(self):
        r = resolve(None, TR, "Toronto, ON", "GTA")
        self.assertEqual(len(r["ranges"]), 3)
        p = r["ranges"][r["primary"]]
        self.assertEqual((p["min"], p["max"], p["currency"], p["label"]), (126000, 176000, "CAD", "Ontario, Canada"))
        self.assertTrue(r["ranges"][0]["label"].startswith("New York"))
        self.assertEqual(r["ranges"][1]["label"], "Other US locations")

    def test_formats(self):
        self.assertEqual(ranges("Salary range: $140K–$175K CAD plus bonus.")[0], [(140000, 175000, "CAD", True)])
        self.assertEqual(ranges("Compensation: CA$160,000 to CA$200,000 annually")[0][0][:3], (160000, 200000, "CAD"))
        self.assertEqual(ranges("CAN, BC, Vancouver - 135,700.00 - 226,500.00 CAD annually")[0][0][:2], (135700, 226500))
        hourly = resolve(None, "Pay: $45.00 - $55.00 per hour", "", "GTA")["ranges"][0]
        self.assertEqual((hourly["min"], hourly["interval"]), (45, "hour"))

    def test_us_only_has_no_primary(self):
        rs, primary = ranges("For U.S.-based roles, we expect a starting base salary between $149,000 and $266,200.")
        self.assertEqual(rs[0][2], "USD")
        self.assertIsNone(primary)

    def test_ignores_non_pay_numbers(self):
        self.assertIsNone(resolve(None, "We have 10-15 engineers and need 3 to 5 years experience. Founded 2010-2015.", "", "GTA"))
        self.assertIsNone(resolve(None, "We raised $100,000,000 - $150,000,000 in funding.", "", "GTA"))

    def test_structured_tiers_prefer_city(self):
        tiers = {"ranges": [
            {"min": 250000, "max": 460000, "currency": "CAD", "interval": "1 YEAR", "label": "Canada"},
            {"min": 295000, "max": 535000, "currency": "CAD", "interval": "1 YEAR", "label": "Canada - Toronto (GTA), Montreal"},
            {"min": 205000, "max": 380000, "currency": "USD", "interval": "1 YEAR", "label": "USA - California"}]}
        r = resolve(tiers, "", "Toronto", "GTA")
        self.assertEqual(r["primary"], 1)
        self.assertEqual(r["source"], "field")


if __name__ == "__main__":
    unittest.main()
