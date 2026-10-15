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


from lodestone.pay import equity_from_text, pay_kind  # noqa: E402


class TestPayKindAndEquity(unittest.TestCase):
    def test_ratehub_bonus_inclusive(self):
        r = resolve(None, "The estimated compensation range for this position, inclusive of a annual performance bonus "
                          "is $125,000 - 175,000.", "Toronto", "GTA")["ranges"][0]
        self.assertEqual((r["kind"], r["estimated"], r["max"]), ("base_bonus", True, 175000))

    def test_kinds(self):
        self.assertEqual(pay_kind("The base salary range for this role is $1 - $2"), "base")
        self.assertEqual(pay_kind("On-target earnings (OTE) of $150,000 - $200,000"), "ote")
        self.assertEqual(pay_kind("$96,900 - $136,800 CAD"), "unspecified")
        r = resolve(None, "Base pay range\n$96,900 - $136,800 CAD", "Toronto", "GTA")["ranges"][0]
        self.assertEqual(r["kind"], "base")                      # heading on the line above

    def test_equity(self):
        self.assertIsNone(equity_from_text("We are committed to diversity, equity and inclusion. Pay equity matters."))
        self.assertIsNone(equity_from_text("Experience with equity research. Salary reflects internal equity."))
        self.assertEqual(equity_from_text("Competitive salary, bonus and equity.")["certainty"], "offered")
        self.assertEqual(equity_from_text("This role may be eligible for equity awards.")["certainty"], "possible")
        a = equity_from_text("You'll receive an RSU grant valued at $80,000 - $120,000 over four years.")["amounts"][0]
        self.assertEqual((a["min"], a["unit"]), (80000, "currency"))
        self.assertEqual(equity_from_text("Equity: 0.05% - 0.15% in stock options.")["amounts"][0]["unit"], "percent")

    def test_equity_grant_is_not_salary(self):
        r = resolve(None, "You'll receive an RSU grant valued at $80,000 - $120,000 over four years.", "Toronto", "GTA")
        self.assertEqual(r["ranges"], [])
        self.assertTrue(r["equity"]["offered"])

    def test_base_pay_sentence_mentioning_equity_is_not_an_equity_amount(self):
        r = resolve(None, "The expected base pay range for this position in the Toronto area is CAD $163,000 - CAD $203,750, "
                          "not inclusive of potential equity offering, bonus or benefits.", "Toronto", "GTA")
        self.assertEqual(r["ranges"][0]["max"], 203750)
        self.assertEqual(r["equity"]["amounts"], [])
