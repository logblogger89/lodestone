import unittest

from lodestone.signals import norm, pathway_for

SIG = {"positions": 31, "tech_positions": 31, "streams": {"Global Talent Stream": 21, "High Wage": 10},
       "top_occupations": ["20012-Computer and information systems managers"], "quarters": ["2025Q4"]}


class TestSignals(unittest.TestCase):
    def test_norm_strips_legal_suffixes(self):
        self.assertEqual(norm("Amazon Development Centre Canada ULC"), "amazon development centre")
        self.assertEqual(norm("Royal Bank of Canada"), "royal bank")

    def test_lmia_employer_is_inferred_strong(self):
        p = pathway_for("RBC", {"subs": {"pathway": 45}, "reasons": {"pathway": "No information"}}, SIG, "2024Q1–2026Q1")
        self.assertEqual(p["score"], 80)
        self.assertEqual(p["signals"][0]["status"], "Inferred")
        self.assertIn("21 through the Global Talent Stream", p["signals"][0]["detail"])

    def test_posting_restriction_wins(self):
        p = pathway_for("RBC", {"subs": {"pathway": 15}, "reasons": {"pathway": "Posting says no sponsorship (stated)"}}, SIG, "w")
        self.assertEqual(p["score"], 15)
        self.assertEqual(p["signals"][0]["status"], "Stated")

    def test_ict_comes_from_the_users_employer_only(self):
        self.assertEqual(pathway_for("Google", None, None, "w")["score"], 45)          # nobody is special-cased
        self.assertEqual(pathway_for("Google", None, None, "w", current_employer="Google")["score"], 95)
        u = pathway_for("Microsoft", {"subs": {"pathway": 65}, "reasons": {"pathway": "Large multinational (inferred)"}}, None, "w")
        self.assertEqual((u["score"], u["signals"][0]["status"]), (45, "Unknown"))


if __name__ == "__main__":
    unittest.main()


class TestMatching(unittest.TestCase):
    def test_legal_name_variants(self):
        from lodestone.signals import _match
        keys = {"salesforce": "Salesforce", "okta": "Okta"}
        prefixes = {"salesforce": "Salesforce", "okta": "Okta"}
        self.assertEqual(_match(norm("Salesforce.com Canada Corp."), keys, prefixes), "Salesforce")
        self.assertEqual(_match(norm("Okta"), keys, prefixes), "Okta")
        self.assertIsNone(_match(norm("Salesforce Plumbing Supply Inc."), keys, prefixes))
